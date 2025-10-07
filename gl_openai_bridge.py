#!/usr/bin/env python3
import os, json, socket, threading, requests
HOST, PORT = "127.0.0.1", 7422
API_URL = "https://api.openai.com/v1/responses"
MODEL   = os.environ.get("GL_MODEL","gpt-4.1-mini")
API_KEY = os.environ.get("OPENAI_API_KEY","")
HEAD = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
CMD_SCHEMA = {"type":"object","properties":{"intent":{"enum":["HEAL","GROW","GUARD","ROUTE","STATUS","STOP"]},"roi":{"type":"string"},"caps":{"type":"object"},"budget":{"type":"object"}}, "required":["intent","roi"],"additionalProperties":False}

def align_free_text(free_text, context=None):
    body = {"model": MODEL,"input":[{"role":"user","content":[{"type":"text","text":f"Align to GhostLink command. Return ONLY a JSON object matching schema.\nFree text: {free_text}\nContext: {json.dumps(context or {})}"}]}],
            "response_format":{"type":"json_schema","json_schema":{"name":"GhostLinkCmd","schema":CMD_SCHEMA}}}
    r = requests.post(API_URL, headers=HEAD, data=json.dumps(body), timeout=30)
    r.raise_for_status()
    out = r.json()
    text = (out.get("output_text") or "").strip()
    return json.loads(text) if text else {"intent":"STATUS","roi":"rack.core","caps":{},"budget":{}}

def handle(conn, addr):
    with conn:
        buf=b""
        while True:
            data=conn.recv(4096)
            if not data: break
            buf+=data
            while b"\n" in buf:
                line, buf = buf.split(b"\n",1)
                line=line.strip()
                if not line: continue
                try: msg=json.loads(line.decode("utf-8"))
                except: continue
                if msg.get("type")!="align": continue
                try: cmd = align_free_text(msg.get("free_text",""), msg.get("context"))
                except Exception as e: cmd = {"intent":"STATUS","roi":"rack.core","caps":{},"budget":{},"error":str(e)}
                conn.sendall(json.dumps({"type":"cmd","cmd":cmd}, separators=(",",":")).encode("utf-8")+b"\n")

def main():
    if not API_KEY: print("[bridge] OPENAI_API_KEY not set; exiting."); return
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST,PORT)); s.listen(10); print(f"[bridge] listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle, args=(conn,addr), daemon=True).start()

if __name__=="__main__": main()
