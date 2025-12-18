import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🧹 Cleaning all build artifacts and caches...\n');

try {
    // 1. Clean packages
    console.log('Cleaning packages...');
    execSync('pnpm -r run clean', { stdio: 'inherit' });

    // 2. Remove node_modules/.cache
    console.log('Removing node_modules/.cache...');
    const cacheDir = path.join(__dirname, '..', 'node_modules', '.cache');
    if (fs.existsSync(cacheDir)) {
        fs.rmSync(cacheDir, { recursive: true, force: true });
    }

    // 3. Remove dist folders if any remain
    // This is handled by pnpm -r run clean usually, but good to be sure

    console.log('\n✨ All clean!');

} catch (error) {
    console.error('\n❌ Clean failed:', error.message);
    process.exit(1);
}
