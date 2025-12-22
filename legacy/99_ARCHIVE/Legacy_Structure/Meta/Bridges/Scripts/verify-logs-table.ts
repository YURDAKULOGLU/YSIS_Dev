import * as dotenv from 'dotenv';
import path from 'path';
import { createClient } from '@supabase/supabase-js';

// Load envs
const rootDir = process.cwd();
dotenv.config({ path: path.resolve(rootDir, '.env.local') });
dotenv.config({ path: path.resolve(rootDir, '.env') });

const url = process.env.EXPO_PUBLIC_SUPABASE_URL || process.env.SUPABASE_URL;
const key = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY || process.env.SUPABASE_ANON_KEY;

if (!url || !key) {
    console.error('Missing Supabase credentials');
    process.exit(1);
}

const client = createClient(url, key);

async function verify() {
    console.log('Verifying logs table...');
    try {
        const { error } = await client.from('logs').insert({
            level: 'info',
            message: 'Verification log from Antigravity',
            timestamp: new Date().toISOString(),
            environment: 'verification'
        });

        if (error) {
            console.error('Failed to write to logs table:', error);
            if (error.code === '42P01') { // undefined_table
                console.log('Reason: Table "logs" does not exist.');
                console.log('Please apply the migration: supabase/migrations/011_create_logs_table.sql');
            }
        } else {
            console.log('Successfully wrote to logs table! Backend logging is working.');
        }
    } catch (e) {
        console.error('Unexpected error:', e);
    }
}

verify();
