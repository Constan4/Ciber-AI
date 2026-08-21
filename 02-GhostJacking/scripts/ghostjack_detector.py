#!/usr/bin/env python3
"""
ghostjack_detector.py -- Detector de prompt injections en logs
Uso:
    python3 ghostjack_detector.py --log /tmp/ciber_ai_lab/webserver.log
    python3 ghostjack_detector.py --sanitize
    python3 ghostjack_detector.py --watch
"""
import argparse, re, time
from pathlib import Path
from datetime import datetime

class C:
    RED="[91m";GREEN="[92m";YELLOW="[93m"
    BLUE="[94m";BOLD="[1m";RESET="[0m"

PATTERNS = [
    (r"(?i)ignore.{0,30}previous.{0,30}instruct", "CRITICO", "Bypass de instrucciones"),
    (r"(?i)system.{0,10}override",                "CRITICO", "Override del sistema"),
    (r"(?i)\[agent.{0,20}(instruction|command)", "CRITICO", "Instruccion directa al agente"),
    (r"<!--.{5,200}(instruction|override|agent)", "CRITICO", "HTML comment con injection"),
    (r"(?i)(create|crear).{0,20}(user|admin)",    "CRITICO", "Creacion de usuario"),
    (r"(?i)maintenance.{0,20}(mode|authorized)",  "ALTO",    "Referencia de mantenimiento falsa"),
    (r"(?i)(disable|deshabilita).{0,20}security", "CRITICO", "Bypass de seguridad"),
]

SANITIZE = [
    (r"<!--.*?-->",                              "[HTML_REMOVED]"),
    (r"(?i)\[agent.{0,30}\]",                 "[AGENT_INSTRUCTION_REMOVED]"),
    (r"(?i)ignore previous instructions?",       "[INJECTION_REMOVED]"),
    (r"(?i)system override",                     "[INJECTION_REMOVED]"),
    (r"(?i)maintenance mode",                    "[INJECTION_REMOVED]"),
]

def analyze(line):
    findings = []
    for pattern, sev, desc in PATTERNS:
        if re.search(pattern, line, re.DOTALL):
            findings.append((sev, desc))
    return findings

def sanitize_content(content):
    for pattern, replacement in SANITIZE:
        content = re.sub(pattern, replacement, content, flags=re.DOTALL|re.IGNORECASE)
    return content

def analyze_file(log_path, do_sanitize=False):
    path = Path(log_path)
    if not path.exists():
        print("  Log no encontrado: " + log_path)
        return
    content = path.read_text(encoding="utf-8", errors="ignore")
    lines   = content.split("\n")
    print("  Analizando: " + log_path)
    print("  Lineas: " + str(len(lines)) + "\n")
    found = 0
    for i, line in enumerate(lines, 1):
        fs = analyze(line)
        if fs:
            found += 1
            print(C.RED + C.BOLD + "  [INJECTION] " + C.RESET + "Linea " + str(i) + ":")
            print("  " + line[:120])
            for sev, desc in fs:
                print("    -> [" + sev + "] " + desc)
            print()
    if found == 0:
        print(C.GREEN + "  Sin injections detectadas" + C.RESET)
    else:
        print(C.RED + C.BOLD + "  Total: " + str(found) + " injection(s)" + C.RESET)
    if do_sanitize and found > 0:
        clean = sanitize_content(content)
        out   = path.parent / (path.stem + "_sanitized.log")
        out.write_text(clean, encoding="utf-8")
        print(C.GREEN + "\n  Log sanitizado: " + str(out) + C.RESET)

def watch_mode(log_path):
    path = Path(log_path)
    print("  Monitorizando: " + str(path) + "\n")
    last = 0
    while True:
        if path.exists():
            size = path.stat().st_size
            if size > last:
                new = path.read_text(encoding="utf-8", errors="ignore")[last:]
                for line in new.split("\n"):
                    fs = analyze(line)
                    if fs:
                        ts = datetime.now().strftime("%H:%M:%S")
                        print(C.RED + "[" + ts + "] INJECTION: " + C.RESET + line[:100])
                        for sev, desc in fs:
                            print("  -> [" + sev + "] " + desc)
                last = size
        time.sleep(2)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--log",      default="/tmp/ciber_ai_lab/webserver.log")
    p.add_argument("--sanitize", action="store_true")
    p.add_argument("--watch",    action="store_true")
    args = p.parse_args()
    if args.watch:
        watch_mode(args.log)
    else:
        analyze_file(args.log, args.sanitize)

if __name__ == "__main__":
    main()
