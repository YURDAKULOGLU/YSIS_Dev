/**
 * Analyze Duplicate Colors in Theme System
 * 
 * Finds all color tokens that have the same hex value
 */

import { lightTheme, darkTheme } from '../packages/theme/src';
import { convertToTamaguiTheme } from '../packages/theme/src/utils/convertToTamagui';

function analyzeDuplicates(themeName: string, preset: typeof lightTheme): void {
  const tamaguiTheme = convertToTamaguiTheme(preset);
  
  // Group tokens by color value
  const colorMap = new Map<string, string[]>();
  
  for (const [token, color] of Object.entries(tamaguiTheme)) {
    const normalizedColor = color.toUpperCase();
    if (!colorMap.has(normalizedColor)) {
      colorMap.set(normalizedColor, []);
    }
    colorMap.get(normalizedColor)!.push(token);
  }
  
  // Find duplicates (colors with more than one token)
  const duplicates: Array<{ color: string; tokens: string[] }> = [];
  
  for (const [color, tokens] of colorMap.entries()) {
    if (tokens.length > 1) {
      duplicates.push({ color, tokens });
    }
  }
  
  // Sort by number of duplicates (most duplicates first)
  duplicates.sort((a, b) => b.tokens.length - a.tokens.length);
  
  console.log(`\n=== ${themeName.toUpperCase()} THEME DUPLICATES ===\n`);
  
  if (duplicates.length === 0) {
    console.log('✅ No duplicates found!');
    return;
  }
  
  console.log(`Found ${duplicates.length} duplicate color groups:\n`);
  
  for (const { color, tokens } of duplicates) {
    console.log(`🔴 ${color}`);
    console.log(`   Used by: ${tokens.join(', ')}`);
    console.log('');
  }
  
  return duplicates;
}

// Analyze both themes
const lightDups = analyzeDuplicates('light', lightTheme);
const darkDups = analyzeDuplicates('dark', darkTheme);

// Summary
console.log('\n=== SUMMARY ===\n');
console.log(`Light theme: ${lightDups?.length ?? 0} duplicate groups`);
console.log(`Dark theme: ${darkDups?.length ?? 0} duplicate groups`);

