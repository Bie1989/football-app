from flask import Flask, render_template_string
from repository import FootballRepository

app = Flask(__name__)
repo = FootballRepository()

PAGE = """
<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<title>ผลบอลสด - Premier League</title>
<style>
body{font-family:Tahoma,Arial;background:#0e1a2b;color:#fff;margin:0;padding:20px}
h1{color:#4fc3f7}
.match{background:#16283f;border-radius:10px;padding:14px;margin:10px 0;display:flex;justify-content:space-between;align-items:center}
.team{font-size:18px}
.score{font-size:24px;font-weight:bold;color:#ffd54f}
.status{color:#81c784;font-size:14px}
.empty{color:#aaa}
</style>
</head>
<body>
<h1>⚽ ผลบอลสด - Premier League</h1>
<p>อัปเดตล่าสุดจาก football-data.org</p>
{% if matches %}
  {% for m in matches %}
  <div class="match">
    <div class="team">{{ m.home_team }}</div>
    <div class="score">{{ m.home_score if m.home_score is not none else '-' }} : {{ m.away_score if m.away_score is not none else '-' }}</div>
    <div class="team">{{ m.away_team }}</div>
  </div>
  <div class="status">สถานะ: {{ m.status }} | เวลาแข่ง: {{ m.utc_kickoff }}</div>
  {% endfor %}
{% else %}
  <p class="empty">ตอนนี้ยังไม่มีนัดที่กำลังแข่งสด</p>
{% endif %}
</body>
</html>
"""

@app.route("/")
def home():
    matches = repo.get_live_matches()
    return render_template_string(PAGE, matches=matches)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)