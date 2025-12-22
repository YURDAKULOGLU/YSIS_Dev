import { createClient } from '@supabase/supabase-js';
import * as dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

// Load environment variables
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
dotenv.config({ path: resolve(__dirname, '../.env') });

const supabaseUrl = process.env.EXPO_PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
    console.error('Error: EXPO_PUBLIC_SUPABASE_URL and EXPO_PUBLIC_SUPABASE_ANON_KEY must be set in .env');
    process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function inspectFlow(executionId: string): Promise<void> {
    console.log(`\n🔍 Inspecting Flow Execution: ${executionId}\n`);

    // 1. Fetch Execution Details
    const { data: execution, error: execError } = await supabase
        .from('flow_executions')
        .select('*, flows(name)')
        .eq('id', executionId)
        .single();

    if (execError) {
        console.error('❌ Failed to fetch execution:', execError.message);
        return;
    }

    const duration = execution.completed_at
        ? (new Date(execution.completed_at).getTime() - new Date(execution.started_at).getTime()) / 1000
        : 'Running...';

    console.log(`📋 Flow: ${execution.flows?.name ?? 'Unknown'}`);
    console.log(`Status: ${execution.status.toUpperCase()}`);
    console.log(`Duration: ${duration}s`);
    console.log(`Started: ${new Date(execution.started_at).toLocaleString()}`);
    console.log('----------------------------------------');

    // 2. Fetch Steps
    const { data: steps, error: stepsError } = await supabase
        .from('flow_execution_steps')
        .select('*')
        .eq('execution_id', executionId)
        .order('started_at', { ascending: true });

    if (stepsError) {
        console.error('❌ Failed to fetch steps:', stepsError.message);
        return;
    }

    if (!steps || steps.length === 0) {
        console.log('No steps recorded.');
        return;
    }

    // 3. Print Steps
    steps.forEach((step, index) => {
        const stepDuration = step.completed_at
            ? ((new Date(step.completed_at).getTime() - new Date(step.started_at).getTime()) / 1000).toFixed(2)
            : '...';

        console.log(`\n[${index + 1}] Step: ${step.step_id} (${step.step_type})`);
        console.log(`   Status: ${step.status} | Duration: ${stepDuration}s`);

        if (step.input) {
            console.log(`   📥 Input: ${JSON.stringify(step.input).substring(0, 100)}${JSON.stringify(step.input).length > 100 ? '...' : ''}`);
        }

        if (step.output) {
            // Check for AI processing details
            if (step.output.ai_processing) {
                const ai = step.output.ai_processing;
                console.log(`   🤖 AI Instruction: "${ai.instruction.substring(0, 80).replace(/\n/g, ' ')}..."`);
                console.log(`   🤖 AI Output: "${String(ai.output).substring(0, 80).replace(/\n/g, ' ')}..."`);
                if (ai.duration_ms) {
                    console.log(`   ⏱️ AI Latency: ${ai.duration_ms}ms`);
                }
            } else {
                console.log(`   out Output: ${JSON.stringify(step.output).substring(0, 100)}${JSON.stringify(step.output).length > 100 ? '...' : ''}`);
            }
        }

        if (step.error) {
            console.log(`   ❌ Error: ${step.error}`);
        }
    });
    console.log('\n----------------------------------------');
}

// Main
const args = process.argv.slice(2);
if (args.length === 0) {
    console.log('Usage: npx tsx scripts/inspect-flow.ts <execution_id>');
    // Optional: Fetch latest if no ID provided
    console.log('Fetching latest execution...');
    supabase
        .from('flow_executions')
        .select('id')
        .order('created_at', { ascending: false })
        .limit(1)
        .single()
        .then(({ data }) => {
            if (data) void inspectFlow(data.id);
            else console.log('No executions found.');
        });
} else {
    void inspectFlow(args[0]);
}
