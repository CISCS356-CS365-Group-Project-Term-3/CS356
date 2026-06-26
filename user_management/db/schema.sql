CREATE TABLE users (
    user_id       SERIAL PRIMARY KEY,
    user_name     VARCHAR(100) UNIQUE NOT NULL,
    user_email    VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    user_role     VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    updated_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_audit_logs (
    id             SERIAL PRIMARY KEY,
    actor_user_id  INTEGER NOT NULL REFERENCES users(id),
    target_user_id INTEGER REFERENCES users(id),
    action_type    VARCHAR(100) NOT NULL,
    created_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE password_reset_tokens (
    token         VARCHAR(64) PRIMARY KEY,
    user_email    VARCHAR(255) NOT NULL,
    expires_at    TIMESTAMP NOT NULL,
    used          BOOLEAN DEFAULT FALSE
);