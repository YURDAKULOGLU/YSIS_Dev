const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Configuration
const MOBILE_ROOT = path.resolve(__dirname, '../../../apps/mobile');
const SRC_DIR = path.join(MOBILE_ROOT, 'src');
const PACKAGE_JSON_PATH = path.join(MOBILE_ROOT, 'package.json');

console.warn('🛡️  Starting Native Dependency Reality Check...');

// 1. Load package.json dependencies
if (!fs.existsSync(PACKAGE_JSON_PATH)) {
    console.error(`❌ package.json not found at ${PACKAGE_JSON_PATH}`);
    process.exit(1);
}
const packageJson = require(PACKAGE_JSON_PATH);
const allDependencies = {
    ...packageJson.dependencies,
    ...packageJson.devDependencies
};
const installedPackages = Object.keys(allDependencies);

console.warn(`📦 Loaded ${installedPackages.length} dependencies from package.json`);

// 2. Scan source code for imports
// We look for patterns like:
// import ... from 'react-native-...'
// import ... from 'expo-...'
// import ... from '@react-native-...'
const NOTABLE_PREFIXES = ['react-native-', 'expo-', '@react-native-'];

function getAllFiles(dirPath, arrayOfFiles) {
    const files = fs.readdirSync(dirPath);
    arrayOfFiles = arrayOfFiles || [];

    files.forEach((file) => {
        const fullPath = path.join(dirPath, file);

        if (fs.statSync(fullPath).isDirectory()) {
            arrayOfFiles = getAllFiles(fullPath, arrayOfFiles);
        } else if (file.endsWith('.ts') || file.endsWith('.tsx') || file.endsWith('.js')) {
            arrayOfFiles.push(fullPath);
        }
    });

    return arrayOfFiles;
}

try {
    const files = getAllFiles(SRC_DIR);
    console.warn(`search 📄 Scanning ${files.length} source files...`);

    const missingDeps = new Set();

    files.forEach(file => {
        const content = fs.readFileSync(file, 'utf8');

        // Regex to find imports
        const importRegex = /from\s+['"]([^'"]+)['"]/g;
        let match;

        while ((match = importRegex.exec(content)) !== null) {
            const importPath = match[1];

            // Check if it's a native/expo package
            const isNativePackage = NOTABLE_PREFIXES.some(prefix => importPath.startsWith(prefix));

            if (isNativePackage) {
                // Extract package name (handle scoped packages)
                const parts = importPath.split('/');
                let packageName = parts[0];
                if (packageName.startsWith('@') && parts.length > 1) {
                    packageName = `${parts[0]}/${parts[1]}`;
                }

                // Check if listed in package.json
                if (!installedPackages.includes(packageName)) {
                    // Ignore internal expo stuff that sends to standard 'expo' package
                    if (packageName !== 'expo' && !packageName.startsWith('react-native') /* core */) {
                        missingDeps.add(`${packageName} (used in ${path.basename(file)})`);
                    }
                }
            }
        }
    });

    if (missingDeps.size > 0) {
        console.error('\n🚨 REALITY CHECK FAILED: Found ghost native dependencies!');
        console.error('These packages are imported but NOT in package.json (Monorepo Risk):\n');
        missingDeps.forEach(dep => console.error(`   - ${dep}`));
        console.error('\n👉 FIX: Run "npx expo install <package>" in apps/mobile/\n');
        process.exit(1);
    } else {
        console.warn('\n✅ Reality Check Passed: All native imports are accounted for.');
        process.exit(0);
    }

} catch (e) {
    console.error('💥 Script Error:', e);
    process.exit(1);
}
