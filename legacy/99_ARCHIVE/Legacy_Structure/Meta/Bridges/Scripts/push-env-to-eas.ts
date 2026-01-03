
import * as dotenv from 'dotenv';
import path from 'path';
import { execSync } from 'child_process';

// Load envs
const rootDir = process.cwd();
dotenv.config({ path: path.resolve(rootDir, '.env.local') });
dotenv.config({ path: path.resolve(rootDir, '.env') });

const keysToSync = [
    'EXPO_PUBLIC_SUPABASE_URL',
    'EXPO_PUBLIC_SUPABASE_ANON_KEY',
    'EXPO_PUBLIC_OPENAI_API_KEY'
];

console.log('🔒 Starting secure secret sync to EAS...');

keysToSync.forEach(key => {
    const value = process.env[key];
    if (!value) {
        console.warn(`⚠️  Missing value for ${key}, skipping.`);
        return;
    }

    try {
        console.log(`Uploading ${key}...`);
        // --force overrides if it exists
        // --scope project limits it to this specific project
        const cmd = `npx eas-cli secret:create --scope project --name ${key} --value "${value}" --type string --force`;

        // stdio: 'pipe' prevents the command from printing the command itself (with secrets) to the parent console if we managed it manually,
        // but execSync doesn't print by default unless we used 'inherit'.
        // However, we want to capture output to check for success but hide input.
        execSync(cmd, { stdio: 'inherit', cwd: path.resolve(rootDir, 'apps/mobile') });
        console.log(`✅ ${key} set successfully.`);
    } catch (error: any) {
        console.error(`❌ Failed to set ${key}.`);
        // Only print stderr to avoid leaking secret in error message if possible
        if (error.stderr) {
            console.error(error.stderr.toString());
        } else {
            console.error(error.message);
        }
    }
});

console.log('\n✨ All secrets synced!');
