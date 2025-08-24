-- ==========================================
-- Fingerprint Crime Detection System Database Schema
-- ==========================================

-- Drop tables if they already exist (safety for re-init)
DROP TABLE IF EXISTS crime_records CASCADE;
DROP TABLE IF EXISTS fingerprints CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ==============================
-- USERS TABLE
-- ==============================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    gender VARCHAR(50),
    national_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==============================
-- FINGERPRINTS TABLE
-- ==============================
CREATE TABLE fingerprints (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    template JSONB,
    image_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==============================
-- CRIME RECORDS TABLE
-- ==============================
CREATE TABLE crime_records (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    crime_type VARCHAR(255),
    description TEXT,
    date_occurred TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- Indexes for performance
-- ==========================================
CREATE INDEX idx_users_name ON users(full_name);
CREATE INDEX idx_fingerprints_user_id ON fingerprints(user_id);
CREATE INDEX idx_crime_records_user_id ON crime_records(user_id);

-- ==========================================
-- Confirmation message
-- ==========================================
-- Run this script using:
--   psql -U postgres -d crime_detection -f init_db.sql
--
-- Database initialized successfully!
