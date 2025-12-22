import * as dotenv from 'dotenv';
import path from 'path';
import fs from 'fs';
import { createClient } from '@supabase/supabase-js';

// Load envs
const rootDir = process.cwd();
dotenv.config({ path: path.resolve(rootDir, '.env.local') });
dotenv.config({ path: path.resolve(rootDir, '.env') });

const url = process.env.EXPO_PUBLIC_SUPABASE_URL || process.env.SUPABASE_URL;
const key =
  process.env.SUPABASE_SERVICE_ROLE_KEY ||
  process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY ||
  process.env.SUPABASE_ANON_KEY;

if (!url || !key) {
  console.error('Missing Supabase credentials (URL or KEY)');
  process.exit(1);
}

const client = createClient(url, key);

async function fetchLogs() {
  console.log('Fetching logs from Supabase...');

  // Check arguments
  const args = process.argv.slice(2);
  const fetchAll = args.includes('--all');

  let allLogs: any[] = [];
  let page = 0;
  const pageSize = 1000;
  let hasMore = true;

  try {
    const startTime = Date.now();

    while (hasMore) {
      process.stdout.write(`Fetching page ${page + 1}... `);

      const query = client
        .from('logs')
        .select('*')
        .order('timestamp', { ascending: false })
        .range(page * pageSize, (page + 1) * pageSize - 1);

      const { data, error, count } = await query;

      if (error) {
        console.error('\nFailed to fetch logs:', error);
        process.exit(1);
      }

      if (!data || data.length === 0) {
        console.log('Done.');
        hasMore = false;
        break;
      }

      allLogs = allLogs.concat(data);
      console.log(`Received ${data.length} logs.`);

      if (!fetchAll) {
        // If not fetching all, stop after first page (default behavior)
        console.log(
          'Default limit reached (1000). Use --all to fetch everything.'
        );
        hasMore = false;
      } else {
        if (data.length < pageSize) {
          hasMore = false;
        } else {
          page++;
        }
      }
    }

    if (allLogs.length === 0) {
      console.log('No logs found.');
      return;
    }

    // 1. Save JSON
    const jsonPath = path.resolve(rootDir, 'logs_dump.json');
    fs.writeFileSync(jsonPath, JSON.stringify(allLogs, null, 2));

    // 2. Save Text (formatted)
    const txtPath = path.resolve(rootDir, 'logs_dump.txt');
    const textContent = allLogs
      .map((log) => {
        const time = log.timestamp || new Date().toISOString();
        const level = (log.level || 'INFO').toUpperCase();
        const msg = log.message || '';
        const meta = log.metadata ? ` ${JSON.stringify(log.metadata)}` : '';
        return `[${time}] ${level}: ${msg}${meta}`;
      })
      .join('\n');
    fs.writeFileSync(txtPath, textContent);

    const duration = (Date.now() - startTime) / 1000;
    console.log(
      `\n✅ Successfully fetched ${allLogs.length} logs in ${duration}s.`
    );
    console.log(`📁 JSON: ${jsonPath}`);
    console.log(`📄 Text: ${txtPath}`);
  } catch (e) {
    console.error('Unexpected error:', e);
    process.exit(1);
  }
}

fetchLogs();
