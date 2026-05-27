CREATE TABLE users (
    user_id       SERIAL PRIMARY KEY,
    user_name     VARCHAR(100) UNIQUE NOT NULL,
    user_email    VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    user_role     VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);