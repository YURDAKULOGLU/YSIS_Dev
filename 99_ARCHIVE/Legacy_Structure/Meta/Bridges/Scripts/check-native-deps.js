import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

console.log('🔍 Checking native dependencies for mobile app...\n');

// Mobile package.json
const mobilePkgPath = path.join(__dirname, '../../../../apps/mobile/package.json');
const mobilePkg = JSON.parse(fs.readFileSync(mobilePkgPath, 'utf-8'));
const mobileDeps = { ...mobilePkg.dependencies, ...mobilePkg.devDependencies };

// Known native modules that must be direct dependencies
const KNOWN_NATIVE_MODULES = [
  'react-native-svg',
  'react-native-reanimated',
  'react-native-safe-area-context',
  '@react-native-async-storage/async-storage',
  'react-native-gesture-handler',
  'react-native-screens',
  'expo-localization',
  'expo-secure-store',
  'expo-notifications',
  'expo-font',
  'expo-blur',
  'expo-image',
];

const missing = [];
const found = [];

// Check which known native modules are missing
for (const mod of KNOWN_NATIVE_MODULES) {
  if (!mobileDeps[mod]) {
    // Check if it's used as peer dependency by any installed package
    for (const [depName] of Object.entries(mobileDeps)) {
      try {
        const depPkgPath = path.join(__dirname, '../../../../node_modules', depName, 'package.json');
        if (fs.existsSync(depPkgPath)) {
          const depPkg = JSON.parse(fs.readFileSync(depPkgPath, 'utf-8'));
          const peers = depPkg.peerDependencies || {};
          if (peers[mod]) {
            missing.push({ module: mod, requiredBy: depName });
            break;
          }
        }
      } catch (e) {
        // Skip if can't read
      }
    }
  } else {
    found.push(mod);
  }
}

// Also scan src for direct imports of native modules
const srcDir = path.join(__dirname, '../../../../apps/mobile/src');

function scanImports(dir) {
  const imports = new Set();

  function walkDir(currentDir) {
    const files = fs.readdirSync(currentDir);
    for (const file of files) {
      const filePath = path.join(currentDir, file);
      const stat = fs.statSync(filePath);

      if (stat.isDirectory()) {
        walkDir(filePath);
      } else if (file.endsWith('.ts') || file.endsWith('.tsx')) {
        const content = fs.readFileSync(filePath, 'utf-8');
        // Match imports from react-native-* or @react-native/*
        const matches = content.matchAll(/from\s+['"](@react-native[^'"]+|react-native-[^'"]+)['"]/g);
        for (const match of matches) {
          const pkg = match[1].split('/')[0];
          if (pkg.startsWith('@react-native')) {
            imports.add(match[1].split('/').slice(0, 2).join('/'));
          } else {
            imports.add(pkg);
          }
        }
      }
    }
  }

  walkDir(dir);
  return imports;
}

const usedImports = scanImports(srcDir);

// Check if any used imports are missing from package.json
for (const imp of usedImports) {
  if (!mobileDeps[imp] && !missing.find(m => m.module === imp)) {
    missing.push({ module: imp, requiredBy: 'direct import in src/' });
  }
}

// Report
console.log('✅ Found native dependencies:');
found.forEach(m => console.log(`   - ${m}`));

if (missing.length > 0) {
  console.log('\n❌ Missing native dependencies in apps/mobile/package.json:');
  missing.forEach(m => console.log(`   - ${m.module} (required by: ${m.requiredBy})`));
  console.log('\nFix with:');
  console.log(`   cd apps/mobile && npx expo install ${missing.map(m => m.module).join(' ')}`);
  process.exit(1);
} else {
  console.log('\n✅ All native dependencies are properly declared!');
}
