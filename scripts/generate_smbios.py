#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))
from amessage_core.anisette.generator import generate_hardware_profile

def main():
    profile = generate_hardware_profile()
    print("=" * 60)
    print(" Apple SMBIOS Hardware Profile Generated")
    print("=" * 60)
    for k, v in profile.to_dict().items():
        print(f" {k:<25}: {v}")
    print("=" * 60)

if __name__ == "__main__":
    main()
