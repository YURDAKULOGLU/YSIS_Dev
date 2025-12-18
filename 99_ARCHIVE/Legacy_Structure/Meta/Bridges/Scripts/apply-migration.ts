import { createClient } from '@supabase/supabase-js';
import * as dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';
import { readFileSync } from 'fs';

// Load environment variables
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
dotenv.config({ path: resolve(__dirname, '../.env') });

const supabaseUrl = process.env.EXPO_PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
    console.error('Error: EXPO_PUBLIC_SUPABASE_URL and EXPO_PUBLIC_SUPABASE_ANON_KEY must be set in .env');
    process.exit(1);
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const _supabase = createClient(supabaseUrl, supabaseKey);

async function applyMigration(migrationFile: string): Promise<void> {
    console.log(`\n🚀 Applying migration: ${migrationFile}\n`);

    const migrationPath = resolve(__dirname, '../supabase/migrations', migrationFile);
    const sql = readFileSync(migrationPath, 'utf-8');

    console.log('📄 Migration SQL:');
    console.log('----------------------------------------');
    console.log(sql);
    console.log('----------------------------------------\n');

    console.log('⚠️  NOTE: RLS policy changes require admin/service role key.');
    console.log('📋 Please copy the SQL above and run it in Supabase Dashboard > SQL Editor\n');
    console.log('Or set SUPABASE_SERVICE_ROLE_KEY in .env to auto-apply.\n');
}

// Main
const args = process.argv.slice(2);
if (args.length === 0) {
    console.log('Usage: npx tsx scripts/apply-migration.ts <migration_file>');
    console.log('Example: npx tsx scripts/apply-migration.ts 016_fix_flow_executions_rls.sql');
    process.exit(1);
}

void applyMigration(args[0]);
