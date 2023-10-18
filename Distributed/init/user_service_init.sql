-- Create the users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password_hashed VARCHAR
);

-- You can include other schema definitions and initial data as required by your application