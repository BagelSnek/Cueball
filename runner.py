#! /usr/bin/env python3.6
import subprocess
import sys


def start_cue():
    cmd = (sys.executable, "cueball.py")

    while True:
        code = subprocess.call(cmd)
        if code == 0:
            print("\nRestarting Cueball...\n")
            continue
        else:
            break

    print(f"Cue dead, code: {code}")


start_cue()
