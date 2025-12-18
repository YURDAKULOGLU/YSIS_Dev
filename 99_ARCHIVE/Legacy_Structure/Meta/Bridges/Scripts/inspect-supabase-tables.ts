import { createClient } from '@supabase/supabase-js';
import * as dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config({ path: path.resolve(__dirname, '../.env.local') });
dotenv.config({ path: path.resolve(__dirname, '../.env') });

const url = process.env['EXPO_PUBLIC_SUPABASE_URL'];
const key = process.env['EXPO_PUBLIC_SUPABASE_ANON_KEY'];

if (!url || !key) {
    console.error('❌ Missing Supabase credentials');
    process.exit(1);
}

const supabase = createClient(url, key);

async function inspectSchema() {
    console.log('📊 Inspecting Supabase Tables...\n');

    const tables = ['workspaces', 'profiles', 'notes', 'tasks', 'flows', 'flow_executions', 'documents', 'chunks'];

    for (const tableName of tables) {
        console.log(`\n📦 TABLE: ${tableName}`);
        console.log('-'.repeat(80));

        try {
            // Try to fetch one row to see structure
            const { data, error } = await supabase
                .from(tableName)
                .select('*')
                .limit(1);

            if (error) {
                console.log(`  ❌ Error: ${error.message}`);
                if (error.code === 'PGRST116') {
                    console.log(`  ⚠️  Table might not exist or RLS is blocking access`);
                }
            } else {
                if (data && data.length > 0) {
                    const sample = data[0];
                    console.log(`  ✅ Columns found:`);
                    Object.keys(sample).forEach(key => {
                        const value = sample[key];
                        const type = typeof value;
                        console.log(`    - ${key.padEnd(25)} (${type})`);
                    });
                } else {
                    console.log(`  ✅ Table exists but is empty. Trying insert to see required fields...`);

                    // Try a dummy insert to see what fields are required
                    const { error: insertError } = await supabase
                        .from(tableName)
                        .insert({});

                    if (insertError) {
                        console.log(`  📋 Required fields hint: ${insertError.message}`);
                    }
                }
            }
        } catch (err) {
            console.log(`  ❌ Unexpected error: ${err}`);
        }
    }

    console.log('\n' + '='.repeat(80));
    console.log('✅ Inspection complete!');
}

inspectSchema().catch(console.error);
