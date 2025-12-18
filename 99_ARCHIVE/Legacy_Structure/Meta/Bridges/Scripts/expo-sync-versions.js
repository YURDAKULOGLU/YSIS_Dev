#!/usr/bin/env node
/**
 * Expo Version Syncer for PNPM
 *
 * Queries Expo CLI for SDK-compatible versions and updates package.json
 * BEFORE pnpm install runs. This ensures pnpm installs the correct versions.
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const MOBILE_DIR = path.join(__dirname, '..', 'apps', 'mobile');
const PACKAGE_JSON_PATH = path.join(MOBILE_DIR, 'package.json');

// Expo packages that need version checking
const EXPO_PACKAGES = [
  'expo-router',
  'react-native',
  'expo',
  // Add more as needed
];

console.log('🔍 Querying Expo for SDK-compatible versions...\n');

function getExpoRecommendedVersion(packageName) {
  try {
    // Use expo install --check to see recommended version
    const output = execSync(`npx expo install --check ${packageName}`, {
      cwd: MOBILE_DIR,
      encoding: 'utf-8',
      stdio: 'pipe',
    });

    // Parse output like: "expo-router should be ~6.0.14"
    const match = output.match(/should be\s+(.+?)(?:\s|$)/);
    if (match) {
      return match[1].trim();
    }
  } catch (error) {
    // Try alternative: query expo-doctor
    try {
      const doctorOutput = execSync('npx expo-doctor', {
        cwd: MOBILE_DIR,
        encoding: 'utf-8',
        stdio: 'pipe',
      });

      // Look for package-specific recommendations
      const lines = doctorOutput.split('\n');
      for (const line of lines) {
        if (line.includes(packageName)) {
          const match = line.match(/should be\s+(.+?)(?:\s|$)/);
          if (match) return match[1].trim();
        }
      }
    } catch (e) {
      // Ignore
    }
  }
  return null;
}

try {
  const packageJson = JSON.parse(fs.readFileSync(PACKAGE_JSON_PATH, 'utf-8'));
  let updated = false;
  const updates = [];

  // Check each Expo package
  for (const pkg of EXPO_PACKAGES) {
    const currentVersion =
      packageJson.dependencies?.[pkg] || packageJson.devDependencies?.[pkg];
    if (!currentVersion) continue;

    const recommendedVersion = getExpoRecommendedVersion(pkg);
    if (!recommendedVersion) continue;

    // Compare versions (simple string comparison for now)
    // If recommended is different from current, update
    if (recommendedVersion !== currentVersion) {
      if (packageJson.dependencies?.[pkg]) {
        packageJson.dependencies[pkg] = recommendedVersion;
      } else if (packageJson.devDependencies?.[pkg]) {
        packageJson.devDependencies[pkg] = recommendedVersion;
      }
      updated = true;
      updates.push({ pkg, from: currentVersion, to: recommendedVersion });
    }
  }

  if (updated) {
    fs.writeFileSync(
      PACKAGE_JSON_PATH,
      JSON.stringify(packageJson, null, 2) + '\n',
      'utf-8'
    );
    console.log('✅ Updated package.json with Expo-compatible versions:');
    updates.forEach(({ pkg, from, to }) => {
      console.log(`  - ${pkg}: ${from} → ${to}`);
    });
    console.log('\n💡 Run: pnpm install');
  } else {
    console.log('✅ All versions are Expo-compatible!');
  }
} catch (error) {
  console.error('❌ Error:', error.message);
  process.exit(1);
}
