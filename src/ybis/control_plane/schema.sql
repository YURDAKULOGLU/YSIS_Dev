-- Control Plane Database Schema
-- SQLite schema for tasks, runs, leases, and workers coordination

-- Tasks table
CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    objective TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    priority TEXT DEFAULT 'MEDIUM',
    protected INTEGER DEFAULT 0,
    schema_version INTEGER DEFAULT 1,
    workspace_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Runs table
CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    workflow TEXT DEFAULT 'build',
    status TEXT NOT NULL DEFAULT 'pending',
    risk_level TEXT DEFAULT 'low',
    run_path TEXT NOT NULL,
    schema_version INTEGER DEFAULT 1,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    metadata TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
);

-- Leases table (for multi-worker coordination)
CREATE TABLE IF NOT EXISTS leases (
    lease_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL UNIQUE,
    worker_id TEXT NOT NULL,
    ttl_seconds INTEGER NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
);

-- Workers table
CREATE TABLE IF NOT EXISTS workers (
    worker_id TEXT PRIMARY KEY,
    status TEXT DEFAULT 'active',
    heartbeat_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Messages table (for inter-agent messaging)
CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    from_agent TEXT NOT NULL,
    to_agent TEXT NOT NULL,
    type TEXT NOT NULL DEFAULT 'direct',
    subject TEXT NOT NULL,
    content TEXT NOT NULL,
    reply_to TEXT,
    priority TEXT DEFAULT 'NORMAL',
    tags TEXT,
    status TEXT DEFAULT 'unread',
    seen_by TEXT,
    metadata TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agents table (for agent registration)
CREATE TABLE IF NOT EXISTS agents (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    capabilities TEXT,
    allowed_tools TEXT,
    status TEXT DEFAULT 'ACTIVE',
    last_heartbeat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_runs_task_id ON runs(task_id);
CREATE INDEX IF NOT EXISTS idx_runs_status ON runs(status);
CREATE INDEX IF NOT EXISTS idx_leases_task_id ON leases(task_id);
CREATE INDEX IF NOT EXISTS idx_leases_expires_at ON leases(expires_at);
CREATE INDEX IF NOT EXISTS idx_workers_heartbeat ON workers(heartbeat_at);
CREATE INDEX IF NOT EXISTS idx_messages_to_agent ON messages(to_agent);
CREATE INDEX IF NOT EXISTS idx_messages_status ON messages(status);
CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);

