CREATE TABLE notifications (
    nid SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    pid INTEGER NOT NULL,
    notification_text VARCHAR(50) NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP
);