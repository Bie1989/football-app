import sqlite3
from contextlib import contextmanager


class FootballRepository:
    def __init__(self, db_path="football.db"):
        self.db_path = db_path

    @contextmanager
    def connect(self):
        con = sqlite3.connect(self.db_path)
        con.execute("PRAGMA foreign_keys=ON")
        con.row_factory = sqlite3.Row
        try:
            yield con
            con.commit()
        finally:
            con.close()

    def init_db(self, schema="schema.sql"):
        with self.connect() as con:
            con.executescript(open(schema, encoding="utf-8").read())

    def get_live_matches(self):
        with self.connect() as con:
            rows = con.execute(
                "SELECT * FROM matches WHERE status IN ('LIVE','IN_PLAY','PAUSED')"
            ).fetchall()
            return [dict(r) for r in rows]

    def get_fixtures(self, competition_code="PL"):
        with self.connect() as con:
            rows = con.execute(
                """SELECT m.external_id, c.code AS competition, m.utc_kickoff,
                m.status, h.name AS home_team, a.name AS away_team,
                m.home_score, m.away_score
                FROM matches m
                JOIN competitions c ON c.id=m.competition_id
                JOIN teams h ON h.id=m.home_team_id
                JOIN teams a ON a.id=m.away_team_id
                WHERE c.code=? ORDER BY m.utc_kickoff""",
                (competition_code,)
            ).fetchall()
            return [dict(r) for r in rows]