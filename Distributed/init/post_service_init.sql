CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    post_text TEXT NOT NULL,
    image_url VARCHAR(255),
    created_at TIMESTAMP,
    username VARCHAR(100) NOT NULL
);