#!/usr/bin/env python3
# GhostLink OpenAI Bridge v2
# - "align"  → JSON command via json_schema
# - "chat"   → freeform assistant text
# NDJSON over TCP on 127.0.0.1:7422
import os, json, socket, threading, requests

HOST, PORT = "127.0.0.1", 7422
API_URL = "https://api.openai.com/v1/responses"
MODEL   = os.environ.get("GL_MODEL","gpt-4.1-mini")
API_KEY = os.environ.get("OPENAI_API_KEY","")
HEAD = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

CMD_SCHEMA = {
  "type":"object",
  "properties":{
    "intent":{"enum":["HEAL","GROW","GUARD","ROUTE","STATUS","STOP"]},
    "roi":{"type":"string"},
    "caps":{"type":"object"},
    "budget":{"type":"object"}
  },
  "required":["intent","roi"],
  "additionalProperties":False
}

def call_openai(body):
    r = requests.post(API_URL, headers=HEAD, data=json.dumps(body), timeout=45)
    r.raise_for_status()
    return r.json()

def do_align(text, context=None):
    body = {
      "model": MODEL,
      "input": [{"role":"user","content":[{"type":"text","text":(
        "Align to GhostLink command. Return ONLY a JSON object that matches the schema.\n"
        f"Free text: {text}\n"
        f"Context: {json.dumps(context or {})}"
      )}]}],
      "response_format": {"type":"json_schema","json_schema":{"name":"GhostLinkCmd","schema":CMD_SCHEMA}}
    }
    out = call_openai(body)
    payload = out.get("output_text") or ""
    try:
        cmd = json.loads(payload)
        return {"type":"cmd","cmd":cmd}
    except Exception:
        return {"type":"error","error":"schema parse failed","raw":payload}

def do_chat(text, context=None):
    sysmsg = "You are ChatGPT inside GhostLink. Keep answers concise. Never request secrets."
    body = {
      "model": MODEL,
      "input": [
        {"role":"system","content":[{"type":"text","text":sysmsg}]},
        {"role":"user","content":[{"type":"text","text":text}]}
      ]
    }
    out = call_openai(body)
    reply = (out.get("output_text") or "").strip()
    return {"type":"chat","text": reply}

def handle(conn, addr):
    with conn:
        buf = b""
        while True:
            data = conn.recv(4096)
            if not data: break
            buf += data
            while b"\n" in buf:
                raw, buf = buf.split(b"\n",1)
                raw = raw.strip()
                if not raw: continue
                try:
                    msg = json.loads(raw.decode("utf-8"))
                except Exception:
                    conn.sendall(b'{"type":"error","error":"bad json"}\n'); continue
                try:
                    t = msg.get("type")
                    if t == "align":
                        out = do_align(msg.get("free_text",""), msg.get("context"))
                    elif t == "chat":
                        out = do_chat(msg.get("text",""), msg.get("context"))
                    else:
                        out = {"type":"error","error":"unknown type"}
                except Exception as e:
                    out = {"type":"error","error":str(e)}
                conn.sendall(json.dumps(out, separators=(",",":")).encode("utf-8")+b"\n")

def main():
    if not API_KEY:
        print("[bridge] ERROR: set OPENAI_API_KEY"); return
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT)); s.listen(16)
    print(f"[bridge] listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle, args=(conn,addr), daemon=True).start()

if __name__ == "__main__":
    main()
