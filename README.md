# OSCP Roadmap part one --> Days 1–28 (Linux, Networking, Python & Lab Setup)

**Overview**
This README documents everything learned from **Day 1 → Day 28** during the 6‑month USA‑focused OSCP preparation roadmap.

---

## Month 1 --> Summary (Days 1–28)

**Focus:** ==> Linux fundamentals, basic networking, Python scripting, virtual lab setup, and hands‑on payload testing.

### Week 1 -> Linux CLI & Bash (Days 1–7)

**Day 1–2 --? Linux & file management**

(1) Commands: **==>** ls, -lah, cd, pwd, mkdir, touch, rm, cat, less, file

**Day 3–4  Permissions & Ownership**

* Commands: `chmod`, `chown`, `stat`, `ls -l`, `umask`
* Key concepts: owner / group / others;

* Practice: make executable `chmod +x backup.sh` and run in VM.

**Day 6  Process control**

* Commands: `ps aux`, `top`, `htop`,      `kill <PID>`, `kill -9 <PID>`, `jobs`, `fg`, `bg`, `disown`
* OSCP uses: find root processes, identify cron jobs, background reverse shells using `&` + `disown`.

**Day 7 Text parsing**

* Tools: `grep`, `awk`, `sed`.
* Useful patterns: `grep -Ri "pass" .`, `awk -F: '{print $1}' /etc/passwd`, `sed -i 's/old/new/' file`
* OSCP tips: extract creds, modify scripts for privilege escalation, clean logs with `sed` (lab only).

---

### Week 2 Networking Basics (Days 8–14)

**Day 8  OSI & TCP/IP models**

* OSI 7 layers mnemonic and mapping to attacks
**Day 9  IP addressing & CIDR**
**Day 10  ping, traceroute, nslookup, dig (practical)**

* `ping <ip>` (ICMP), `traceroute <host>`, `nslookup <domain>`, `dig <domain> ANY`.
**Day 11 deeper DNS & reachability**

* Differences: `dig` vs `nslookup`, DNS record types (`A`, `MX`, `TXT`, `NS`), DNS troubleshooting.

**Day 12 Open ports & protocols**

* Tools: `netstat -anp`, `ss -tuln`, `lsof -i`.
* Identify listening services and owning PIDs (e.g., `ss -tuln | grep :80`).

**Day 13  tcpdump packet capture**

* Example capture: `sudo tcpdump -i eth0 -c 20 port 80 -w capture.pcap`
* Save to `.pcap` and analyze later in Wireshark.

**Day 14 — Wireshark analysis (HTTP filters)**

* Open `.pcap` in Wireshark, filter `http`, `frame contains "password"`, `Follow -> TCP Stream`.
* Export objects: File > Export Objects > HTTP.

---

### Week 3  Python Scripting (Days 15–21)

**Day 15 — Python intro & control flow**

* Basics: `print()`, `input()`, variables, `if/elif/else`, `for` & `while` loops, lists & dicts, functions.
* Practice: small scripts to classify ports/service types.

**Day 16 CLI tools & argparse**

* `sys.argv` vs `argparse` for friendly CLI tools.
* Example : `python3 scan.py -t 10.10.10.10 -p 22,80`.

**Day 17 — Keylogger (pynput) [LAB ONLY]**

* Install: `pip install pynput`.
* Basic listener writes keystrokes to a file; handle `AttributeError` for special keys.

**Day 18 — Port scanner (basic + threaded)**

* Basic TCP connect scan using `socket.connect_ex()`.
* Multithreaded version using `threading.Thread` for speed; banner grabbing with `recv()`.
* Save results to `scan_results.txt`.

**Day 19 — Reverse shell (Python)**

* Attacker (listener) + target (connect back) example with `socket` and `subprocess.getoutput()`.
* Upgrade shell: `python3 -c 'import pty; pty.spawn("/bin/bash")'`.
* Add recon/persistence (auto-reconnect, SSL wrapping) for advanced labs.

**Day 20 Keylogger (OSCP-level)**

* Hidden logs, persistence (`~/.bashrc` or Windows Startup), network exfiltration options (sockets, SMTP), encryption before sending.

**Day 21  Python Port Scanner (refinement)**

* Add banner parsing, JSON/CSV output, UDP scanning, stealth, randomize order, sleep.

---

### Week 4 — Virtual Labs Setup & TryHackMe (Days 21–28)

**Day 21-22:** Continued tool refinement (port scanner + subdomain finder).

**Day 23  Dir/File brute-forcer (web fuzzing)**

* Use `requests` + SecLists wordlists; thread for speed; check status codes: 200/301/302/403 are mybe valuable.

**Day 24 — TryHackMe: Intro to OffSec (Lab Start)**

* VPN setup: `sudo openvpn <config>`; check `ifconfig tun0` and `ping <lab-IP>`.
* Workflow: `nmap -sC -sV -p- -oN nmap.txt`, gobuster/dirb, manual exploitation, capture `user.txt` & `root.txt`.

**Day 25 — TryHackMe Linux Fundamentals (Part 1)**

* Live practice of `find`, `grep`, `chmod`, `chown`, `ps`, `top`.

**Day 26 — Mirror backup script into VM**

* Run `backup.sh` in victim VM, enhance to collect enumeration data (`/etc/passwd`, `ps aux`, SUID list), push to GitHub.

**Day 27 — VM Networking Setup**

* VirtualBox modes: NAT, Bridged, Host‑Only  Configure Host‑Only and test with `ping` and `nmap`.

**Day 28 — Running scripts in the lab**

* Host payloads via `python3 -m http.server 8000` and download on victim. Add exfil (scp) or socket‑based sending for results.

---


## Next Steps (Days 29+)

* Day 29: Create & push README.md (this file) — done
* Day 30–56: Continue Months 2–3 topics (Recon, Web attacks, Buffer Overflow, Privesc)
* Regularly convert lab notes into full OSCP-style writeups and upload to `writeups/` folder

---