import { SupabaseAdapter } from '../packages/database/src/adapters/SupabaseAdapter';
import * as dotenv from 'dotenv';
import path from 'path';

import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load environment variables
dotenv.config({ path: path.resolve(__dirname, '../.env.local') });
dotenv.config({ path: path.resolve(__dirname, '../.env') });

async function verifySupabase() {
    console.log('🚀 Starting Supabase Verification...');

    const url = process.env.EXPO_PUBLIC_SUPABASE_URL;
    const key = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY;

    if (!url || !key) {
        console.error('❌ Missing environment variables!');
        console.error('EXPO_PUBLIC_SUPABASE_URL:', url ? 'Set' : 'Missing');
        console.error('EXPO_PUBLIC_SUPABASE_ANON_KEY:', key ? 'Set' : 'Missing');
        process.exit(1);
    }

    console.log('✅ Environment variables loaded.');

    const adapter = new SupabaseAdapter({
        url,
        anonKey: key,
    });

    try {
        console.log('📡 Connecting to Supabase...');
        await adapter.initialize();
        console.log('✅ Connection successful!');

        console.log('🩺 Running Health Check...');
        const healthy = await adapter.healthCheck();
        console.log(healthy ? '✅ Health Check Passed' : '❌ Health Check Failed');

        if (healthy) {
            console.log('📝 Testing CRUD (Notes)...');
            // Create
            const noteData = {
                title: 'Verification Note',
                content: 'This note was created by the verification script.',
                is_favorite: false
            };
            const createResult = await adapter.insert('notes', noteData);
            console.log('✅ Created Note:', createResult.id);

            // Read
            const note = await adapter.selectById('notes', createResult.id);
            console.log('✅ Read Note:', note ? 'Success' : 'Failed');

            // Update
            const updateResult = await adapter.update('notes', createResult.id, { title: 'Updated Verification Note' });
            console.log('✅ Updated Note:', updateResult.count > 0 ? 'Success' : 'Failed');

            // Delete
            const deleteResult = await adapter.delete('notes', createResult.id);
            console.log('✅ Deleted Note:', deleteResult.count > 0 ? 'Success' : 'Failed');
        }

    } catch (error) {
        console.error('❌ Verification Failed:', error);
    } finally {
        await adapter.close();
        console.log('👋 Verification Complete.');
    }
}

verifySupabase();
