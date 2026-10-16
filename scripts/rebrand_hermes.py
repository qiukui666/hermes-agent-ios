#!/usr/bin/env python3
"""Rebrand the nanoMuse iOS tree (android/src/ios) to our own identity.

- bundle ids / app group / iCloud container / background-task ids: io.github.nanomuse -> store.hvgy.hermes
- display strings + URL schemes: nanoMuse -> Hermes, nanomuse:// -> hermes://
- agent persona default name: 小爱
Identifiers (NanoMuse*.swift classes/keys) are untouched — case-sensitive rules.
"""
import re
from pathlib import Path

IOS = Path(__file__).resolve().parents[1] / "android" / "src" / "ios"
TEXT = {".swift", ".plist", ".pbxproj", ".entitlements", ".xcstrings", ".storyboard",
        ".xcconfig", ".md", ".json", ".strings", ".yml"}

changed = 0
for f in IOS.rglob("*"):
    if not f.is_file() or f.suffix not in TEXT:
        continue
    try:
        s = f.read_text()
    except (UnicodeDecodeError, OSError):
        continue
    o = s
    s = s.replace("io.github.nanomuse", "store.hvgy.hermes")
    s = s.replace("nanoMuse", "Hermes")
    s = s.replace("nanomuse-mcp", "hermes-mcp")
    s = s.replace("nanomuse://", "hermes://")
    # URL scheme entries in Info.plist
    s = s.replace("<string>nanomuse</string>", "<string>hermes</string>")
    if s != o:
        f.write_text(s)
        changed += 1
        print("rebranded:", f.relative_to(IOS))

# Agent persona default name -> 小爱
soul = IOS / "Agent" / "Session" / "SoulStore.swift"
s = soul.read_text()
s = s.replace('name: "Hermes"', 'name: "小爱"')
soul.write_text(s)
print("soul persona -> 小爱")

print(f"\n{changed} files changed")
