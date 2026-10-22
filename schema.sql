PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS competitions (
  id INTEGER PRIMARY KEY,
  external_id TEXT UNIQUE,
  code TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  country TEXT,
  season TEXT,
  source TEXT DEFAULT 'football-data.org',
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS teams (
  id INTEGER PRIMARY KEY,
  external_id TEXT UNIQUE,
  name TEXT NOT NULL,
  short_name TEXT,
  crest_url TEXT,
  country TEXT,
  source TEXT DEFAULT 'football-data.org',
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS matches (
  id INTEGER PRIMARY KEY,
  external_id TEXT UNIQUE NOT NULL,
  competition_id INTEGER NOT NULL REFERENCES competitions(id),
  home_team_id INTEGER NOT NULL REFERENCES teams(id),
  away_team_id INTEGER NOT NULL REFERENCES teams(id),
  matchday INTEGER,
  utc_kickoff TEXT NOT NULL,
  status TEXT DEFAULT 'SCHEDULED',
  home_score INTEGER,
  away_score INTEGER,
  source TEXT DEFAULT 'football-data.org',
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS api_sync_log (
  id INTEGER PRIMARY KEY,
  source TEXT,
  endpoint TEXT,
  status TEXT,
  records_upserted INTEGER DEFAULT 0,
  error_message TEXT,
  started_at TEXT DEFAULT CURRENT_TIMESTAMP,
  finished_at TEXT
);