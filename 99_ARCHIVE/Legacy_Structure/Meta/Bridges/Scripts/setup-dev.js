import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🚀 Setting up YBIS development environment...\n');

try {
    // 1. Check Node.js version
    const nodeVersion = process.version;
    console.log(`📦 Node.js version: ${nodeVersion}`);
    const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0]);
    if (majorVersion < 20) {
        console.error('❌ Node.js 20+ is required.');
        process.exit(1);
    }

    // 2. Install dependencies
    console.log('\n📦 Installing dependencies...');
    execSync('pnpm install', { stdio: 'inherit' });

    // 3. Build shared packages
    console.log('\n🏗️ Building shared packages...');
    execSync('pnpm run prebuild', { stdio: 'inherit' });

    // 4. Check environment variables
    console.log('\nChecking environment variables...');
    const envExample = path.join(__dirname, '..', '.env.example');
    const envLocal = path.join(__dirname, '..', '.env.local');

    if (fs.existsSync(envExample) && !fs.existsSync(envLocal)) {
        console.log('⚠️ .env.local not found. Creating from .env.example...');
        fs.copyFileSync(envExample, envLocal);
        console.log('✅ .env.local created. Please update it with your keys.');
    } else if (fs.existsSync(envLocal)) {
        console.log('✅ .env.local exists.');
    }

    console.log('\n✅ Setup complete! Run "pnpm run dev" to start development.');

} catch (error) {
    console.error('\n❌ Setup failed:', error.message);
    process.exit(1);
}
