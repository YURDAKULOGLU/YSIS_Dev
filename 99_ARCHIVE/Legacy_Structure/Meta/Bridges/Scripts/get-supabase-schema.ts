import { createClient } from '@supabase/supabase-js';
import * as dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../.env.local') });
dotenv.config({ path: path.resolve(__dirname, '../.env') });

const url = process.env['EXPO_PUBLIC_SUPABASE_URL'];
const key = process.env['EXPO_PUBLIC_SUPABASE_ANON_KEY'];

if (!url || !key) {
    console.error('❌ Missing Supabase credentials');
    process.exit(1);
}

const supabase = createClient(url, key);

async function getTableSchema() {
    console.log('📊 Fetching Supabase Schema...\n');

    // Get all tables
    const { data: tables, error: tablesError } = await supabase
        .from('information_schema.tables')
        .select('table_name')
        .eq('table_schema', 'public')
        .order('table_name');

    if (tablesError) {
        console.error('Error fetching tables:', tablesError);
        return;
    }

    console.log('📋 Tables found:', tables?.map(t => t.table_name).join(', '));
    console.log('\n' + '='.repeat(80) + '\n');

    // For each table, get columns
    for (const table of tables || []) {
        const tableName = table.table_name;

        const { data: columns, error: columnsError } = await supabase
            .from('information_schema.columns')
            .select('column_name, data_type, is_nullable, column_default')
            .eq('table_schema', 'public')
            .eq('table_name', tableName)
            .order('ordinal_position');

        if (columnsError) {
            console.error(`Error fetching columns for ${tableName}:`, columnsError);
            continue;
        }

        console.log(`\n📦 TABLE: ${tableName}`);
        console.log('-'.repeat(80));

        if (columns) {
            columns.forEach(col => {
                const nullable = col.is_nullable === 'YES' ? '(nullable)' : '(required)';
                const defaultVal = col.column_default ? ` [default: ${col.column_default}]` : '';
                console.log(`  ${col.column_name.padEnd(25)} ${col.data_type.padEnd(20)} ${nullable}${defaultVal}`);
            });
        }

        console.log('');
    }

    console.log('\n' + '='.repeat(80));
    console.log('✅ Schema export complete!');
}

getTableSchema().catch(console.error);
