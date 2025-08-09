-- Migration: Add username column to user_profiles table

ALTER TABLE user_profiles
ADD COLUMN username TEXT NOT NULL DEFAULT '';

CREATE UNIQUE INDEX IF NOT EXISTS idx_user_profiles_username ON user_profiles(username);