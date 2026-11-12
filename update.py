
"""Experimental Duolingo public-profile XP snapshots."""

import json
import datetime
import pathlib
import urllib.request
import urllib.parse
import time

ROOT = pathlib.Path(__file__).parent
PLAYERS = json.loads(
    (ROOT / "players.json").read_text(encoding="utf-8")
)

FILE = ROOT / "data" / "history.json"
FILE.parent.mkdir(parents=True, exist_ok=True)

try:
    history = json.loads(FILE.read_text(encoding="utf-8"))
except (OSError, ValueError):
    history = {"snapshots": []}

now = datetime.datetime.now(datetime.timezone.utc)
results = []

for player in PLAYERS:
    username = player["username"]

    url = (
        "https://www.duolingo.com/2017-06-30/users?"
        + urllib.parse.urlencode({"username": username})
    )

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            payload = json.load(resp)

        users = payload.get("users") or []

        matched = next(
            (
                u for u in users
                if u.get("username", "").lower() == username.lower()
            ),
            None,
        )

        if not matched or not isinstance(matched.get("totalXp"), int):
            raise ValueError("XP nejsou verejne dostupne")

        results.append({
            "username": username,
            "totalXp": matched["totalXp"],
        })

    except Exception as exc:
        print(f"{username}: {type(exc).__name__}: {exc}")

    time.sleep(1)

if not results:
    raise SystemExit(
        "Zadna data z Duolinga. Historie beze zmeny."
    )

snap = {
    "at": now.isoformat(timespec="seconds"),
    "players": results,
}

history["snapshots"].append(snap)

cutoff = now - datetime.timedelta(days=70)

history["snapshots"] = [
    s for s in history["snapshots"]
    if datetime.datetime.fromisoformat(s["at"]) >= cutoff
]

FILE.write_text(
    json.dumps(history, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

print(f"Ulozeno {len(results)} z {len(PLAYERS)} uctu.")
