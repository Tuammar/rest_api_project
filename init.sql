CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY,
    created_ad DATE,
    login VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL,
    project_id UUID,
    env VARCHAR,
    domain VARCHAR,
    locktime FLOAT
);
