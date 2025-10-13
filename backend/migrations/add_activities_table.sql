-- Migration: Add activities table
-- Date: 2025-10-13
-- Description: Create activities table for team meetings, seminars, studies, and projects

-- Create enum type for activity type
CREATE TYPE activity_type AS ENUM ('meeting', 'seminar', 'study', 'project');

-- Create activities table
CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    activity_date TIMESTAMP WITH TIME ZONE NOT NULL,
    type activity_type NOT NULL,
    participants INTEGER,
    location VARCHAR(200),
    images JSON DEFAULT '[]'::json,
    created_by INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create indexes for performance
CREATE INDEX idx_activities_title ON activities(title);
CREATE INDEX idx_activities_type ON activities(type);
CREATE INDEX idx_activities_activity_date ON activities(activity_date);
CREATE INDEX idx_activities_type_date ON activities(type, activity_date);
CREATE INDEX idx_activities_created_by ON activities(created_by);

-- Add comment
COMMENT ON TABLE activities IS 'Activities table for team meetings, seminars, studies, and projects';

-- To rollback this migration, run:
-- DROP INDEX idx_activities_created_by;
-- DROP INDEX idx_activities_type_date;
-- DROP INDEX idx_activities_activity_date;
-- DROP INDEX idx_activities_type;
-- DROP INDEX idx_activities_title;
-- DROP TABLE activities;
-- DROP TYPE activity_type;
