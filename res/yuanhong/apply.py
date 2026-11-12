#!/usr/bin/env python3
"""Apply Yuanhong branding to the hbb_common submodule at build time.

Usage: python3 res/yuanhong/apply.py <APP_NAME>
APP_NAME must be ASCII letters/digits/-/_ (RustDesk uses it for install paths,
service names and batch scripts). The on-screen name is set in the UI code.
"""
import re
import sys

SERVER = "rustdesk.yuanhong-automation.com"
KEY = "npTDJKlmK7icT1uuDBTk4gl5rEXPuWNrFN52Be2mX5w="

app_name = sys.argv[1]
if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_-]*", app_name):
    sys.exit(f"invalid app name: {app_name}")

path = "libs/hbb_common/src/config.rs"
src = open(path, encoding="utf-8").read()
subs = [
    (r'pub const RENDEZVOUS_SERVERS: &\[&str\] = &\[[^\]]*\];',
     f'pub const RENDEZVOUS_SERVERS: &[&str] = &["{SERVER}"];'),
    (r'pub const RS_PUB_KEY: &str = "[^"]*";',
     f'pub const RS_PUB_KEY: &str = "{KEY}";'),
    (r'pub static ref APP_NAME: RwLock<String> = RwLock::new\("RustDesk"\.to_owned\(\)\);',
     f'pub static ref APP_NAME: RwLock<String> = RwLock::new("{app_name}".to_owned());'),
]
for pattern, repl in subs:
    src, n = re.subn(pattern, repl, src)
    if n != 1:
        sys.exit(f"pattern not found exactly once: {pattern}")
open(path, "w", encoding="utf-8", newline="\n").write(src)
print(f"branded hbb_common: app={app_name} server={SERVER}")
