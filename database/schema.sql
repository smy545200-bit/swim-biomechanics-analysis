CREATE TABLE IF NOT EXISTS athletes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    sex TEXT,
    event TEXT,
    level TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    athlete_id INTEGER,
    file_path TEXT NOT NULL,
    view_type TEXT,
    stroke_type TEXT,
    fps REAL,
    width INTEGER,
    height INTEGER,
    duration_seconds REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (athlete_id) REFERENCES athletes(id)
);

CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id INTEGER NOT NULL,
    frame_index INTEGER,
    metrics_json TEXT,
    diagnosis_text TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (video_id) REFERENCES videos(id)
);

CREATE TABLE IF NOT EXISTS technical_issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    athlete_id INTEGER,
    video_id INTEGER,
    issue_name TEXT NOT NULL,
    body_region TEXT,
    phase TEXT,
    severity TEXT,
    evidence TEXT,
    suggestion TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (athlete_id) REFERENCES athletes(id),
    FOREIGN KEY (video_id) REFERENCES videos(id)
);
