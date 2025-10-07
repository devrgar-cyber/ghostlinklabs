#!/usr/bin/env python3
# gl_talk_cli.py — interactive CLI to talk to the local OpenAI bridge
# Modes:
#   chat:  free text → assistant reply
#   align: free text → structured command (JSON)
import socket, sys, json, os

HOST, PORT = "127.0.0.1", 7422

def send(msg):
    s = socket.create_connection((HOST,PORT), timeout=5)
    s.sendall((json.dumps(msg) + "\n").encode("utf-8"))
    out = s.recv(1_000_000).decode("utf-8").strip()
    s.close()
    return out

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("chat","align"):
        print("usage: gl_talk_cli.py chat|align [prompt...]")
        sys.exit(2)
    mode = sys.argv[1]
    prompt = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None

    if not prompt:
        try:
            while True:
                line = input(f"{mode}> ").strip()
                if not line: continue
                if mode == "chat":
                    print(send({"type":"chat","text": line}))
                else:
                    print(send({"type":"align","free_text": line, "context":{"roi_allow":["rack.core","rack.front"]}}))
        except (EOFError, KeyboardInterrupt):
            print(); return
    else:
        if mode == "chat":
            print(send({"type":"chat","text": prompt}))
        else:
            print(send({"type":"align","free_text": prompt, "context":{"roi_allow":["rack.core","rack.front"]}}))

if __name__ == "__main__":
    main()
