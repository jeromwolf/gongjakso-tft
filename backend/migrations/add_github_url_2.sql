-- Migration: Add github_url_2 column to projects table
-- Date: 2025-10-09
-- Description: Add secondary GitHub repository URL field

-- Add github_url_2 column
ALTER TABLE projects
ADD COLUMN IF NOT EXISTS github_url_2 VARCHAR(500) NULL;

-- Add comment
COMMENT ON COLUMN projects.github_url_2 IS 'Secondary GitHub repository URL';
