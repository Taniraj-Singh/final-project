-- Initialize database with extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Check if TimescaleDB is available and create extension
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_available_extensions WHERE name = 'timescaledb') THEN
        CREATE EXTENSION IF NOT EXISTS timescaledb;
    END IF;
END
$$;

