
FILE.parent.mkdir(parents=True, exist_ok=True)
"""Experimental public-profile XP snapshots; no credentials required."""
import json, datetime, pathlib, urllib.request, urllib.parse, time
from zoneinfo import ZoneInfo
ROOT=pathlib.Path(__file__).parent
PLAYERS=json.loads((ROOT/'players.json').read_text(encoding='utf-8'))
FILE=ROOT/'data'/'history.json'
try: history=json.loads(FILE.read_text(encoding='utf-8'))
except (OSError,ValueError): history={'snapshots':[]}
now=datetime.datetime.now(datetime.timezone.utc)
results=[]
for player in PLAYERS:
    username=player['username']
    url='https://www.duolingo.com/2017-06-30/users?'+urllib.parse.urlencode({'username':username})
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; DuolingoFriendsLeague/1.0)','Accept':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=12) as resp: payload=json.load(resp)
        users=payload.get('users') or []
        matched=next((u for u in users if u.get('username','').lower()==username.lower()),None)
        if not matched or not isinstance(matched.get('totalXp'),int): raise ValueError('Účet nebo totalXp není veřejně dostupný')
        results.append({'username':username,'totalXp':matched['totalXp']})
    except Exception as exc:
        print(f'{username}: {type(exc).__name__}: {exc}')
    time.sleep(1)
if not results:
    raise SystemExit('Žádná data z Duolinga; historie zůstává beze změny.')
# Append immutable snapshots; old samples are not treated as total XP.
snap={'at':now.isoformat(timespec='seconds'),'players':results}
history['snapshots'].append(snap)
# Keep a reasonable 10-week history, including weekly baselines.
cutoff=now-datetime.timedelta(days=70)
history['snapshots']=[s for s in history['snapshots'] if datetime.datetime.fromisoformat(s['at'])>=cutoff]
FILE.write_text(json.dumps(history,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Uloženo {len(results)} z {len(PLAYERS)} účtů.')
