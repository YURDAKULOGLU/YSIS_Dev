
import sharp from 'sharp';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const assetsDir = path.join(__dirname, '../apps/mobile/assets');
const files = ['icon', 'splash', 'adaptive-icon'];

async function convert() {
    console.log('🖼️  Converting assets to PNG...');

    for (const file of files) {
        const jpgPath = path.join(assetsDir, `${file}.jpg`);
        const pngPath = path.join(assetsDir, `${file}.png`);

        // Check if jpg exists (renamed in previous step)
        if (fs.existsSync(jpgPath)) {
            try {
                await sharp(jpgPath)
                    .toFormat('png')
                    .toFile(pngPath);
                console.log(`✅ Converted ${file}.jpg -> ${file}.png`);

                // Remove the source jpg to clean up
                fs.unlinkSync(jpgPath);
            } catch (err) {
                console.error(`❌ Failed to convert ${file}:`, err);
            }
        } else {
            // Maybe it's still named .png but has jpg content?
            // We generally expected them to be .jpg now because of my previous 'mv' command.
            // If not found, check if .png exists and convert it in-place?
            // Let's assume the previous 'mv' worked or check for .png with jpg signature?
            // For safety, let's just log.
            console.warn(`⚠️  Source file ${file}.jpg not found. Checking if it is mostly correct.`);
        }
    }
}

convert();
