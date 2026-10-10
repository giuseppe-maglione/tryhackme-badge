#!/usr/bin/env python3
import os
import sys
import json

try:
    from curl_cffi import requests
except ImportError:
    sys.stderr.write("[thm-badge] curl_cffi is not installed. Run: pip install curl_cffi\n")
    sys.exit(3)

IMPERSONATE_PROFILES = ["chrome", "chrome131", "safari", "chrome120"]
TIMEOUT = 25

def fetch_profile_data(username: str) -> dict:
    url = "https://tryhackme.com/api/v2/public-profile"
    last = "no attempt"
    for profile in IMPERSONATE_PROFILES:
        try:
            resp = requests.get(
                url,
                params={"username": username},
                impersonate=profile,
                headers={"accept": "application/json"},
                timeout=TIMEOUT,
            )
        except Exception as exc:
            last = f"{profile}: {type(exc).__name__}: {exc}"
            continue

        if resp.status_code == 200 and "json" in (resp.headers.get("content-type") or ""):
            return resp.json()

        mitigated = resp.headers.get("x-vercel-mitigated")
        last = f"{profile}: HTTP {resp.status_code}" + (f" (mitigated={mitigated})" if mitigated else "")

    raise RuntimeError(f"could not fetch profile via browser-TLS; last attempt: {last}")

def main() -> int:
    username = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("THM_USERNAME") or "").strip()
    if not username:
        sys.stderr.write("[thm-badge] usage: fetch_profile.py <username>\n")
        return 2

    try:
        data = fetch_profile_data(username)
        sys.stdout.write(json.dumps(data, indent=2))
        return 0
    except RuntimeError as e:
        sys.stderr.write(f"[thm-badge] {e}\n")
        sys.stderr.write("[thm-badge] (a datacenter/CI IP is always challenged — run from a residential connection)\n")
        return 3

if __name__ == "__main__":
    sys.exit(main())