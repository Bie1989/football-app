import json, os, sys
from repository import FootballRepository

FILE = "matches.json"
repo = FootballRepository()
repo.init_db()

if not os.path.exists(FILE):
    print("ไม่พบไฟล์ matches.json")
    sys.exit(1)

with open(FILE, encoding="utf-8") as f:
    data = json.load(f)

matches = data.get("matches", [])
print(f"พบ {len(matches)} นัด กำลังบันทึกลงฐานข้อมูล...")

with repo.connect() as con:
    for m in matches:
        comp = m["competition"]
        con.execute(
            "INSERT INTO competitions (external_id, code, name) VALUES (?,?,?) ON CONFLICT(code) DO UPDATE SET name=excluded.name",
            (str(comp.get("id")), comp["code"], comp["name"])
        )
        comp_id = con.execute("SELECT id FROM competitions WHERE code=?", (comp["code"],)).fetchone()[0]

        for side in ("homeTeam", "awayTeam"):
            t = m[side]
            con.execute(
                "INSERT INTO teams (external_id, name) VALUES (?,?) ON CONFLICT(external_id) DO UPDATE SET name=excluded.name",
                (str(t["id"]), t["name"])
            )

        home_id = con.execute("SELECT id FROM teams WHERE external_id=?", (str(m["homeTeam"]["id"]),)).fetchone()[0]
        away_id = con.execute("SELECT id FROM teams WHERE external_id=?", (str(m["awayTeam"]["id"]),)).fetchone()[0]

        ft = (m.get("score") or {}).get("fullTime") or {}
        con.execute(
            """INSERT INTO matches (external_id, competition_id, home_team_id, away_team_id, matchday, utc_kickoff, status, home_score, away_score)
            VALUES (?,?,?,?,?,?,?,?,?)
            ON CONFLICT(external_id) DO UPDATE SET status=excluded.status, home_score=excluded.home_score, away_score=excluded.away_score, updated_at=CURRENT_TIMESTAMP""",
            (str(m["id"]), comp_id, home_id, away_id, m.get("matchday"), m["utcDate"], m["status"], ft.get("home"), ft.get("away"))
        )

print("บันทึกเสร็จแล้ว")
live = repo.get_live_matches()
print(f"ผลบอลสดตอนนี้: {len(live)} นัด")