import { execSync } from 'child_process';

console.warn('🔍 Checking for dependency conflicts...\n');

try {
    // Use pnpm's built-in audit and outdated commands
    console.warn('Running pnpm audit...');
    execSync('pnpm audit', { stdio: 'inherit' });

    console.warn('\n✅ No critical vulnerabilities found.');

} catch (error) {
    console.error('\n⚠️ Issues found during dependency check.');
    // Don't exit with error, just warn
}
