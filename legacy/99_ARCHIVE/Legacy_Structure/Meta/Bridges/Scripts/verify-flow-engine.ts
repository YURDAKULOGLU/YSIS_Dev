import { FlowEngine } from '../packages/core/src/services/FlowEngine';
import { Flow } from '../packages/core/src/types';

async function verifyFlowEngine() {
    console.log('🚀 Starting Flow Engine Verification...');

    const engine = new FlowEngine();

    // Register a custom step handler
    engine.registerStep('log', async (params, context) => {
        console.log(`[STEP LOG] ${params.message}`);
        return { logged: true };
    });

    // Define a sample flow
    // Define a sample flow
    const sampleFlow: Flow = {
        id: 'test-flow-1',
        name: 'Test Flow',
        description: 'A simple test flow',
        workspace_id: 'test-workspace',
        user_id: 'test-user',
        is_active: true,
        config: {
            trigger: { type: 'manual' },
            steps: [
                {
                    id: 'step-1',
                    type: 'action',
                    action: 'log',
                    params: { message: 'Hello from Step 1' },
                    next_step_id: 'step-2'
                },
                {
                    id: 'step-2',
                    type: 'delay',
                    action: 'delay',
                    params: { duration: 500 },
                    next_step_id: 'step-3'
                },
                {
                    id: 'step-3',
                    type: 'action',
                    action: 'log',
                    params: { message: 'Hello from Step 3 (after delay)' },
                }
            ]
        },
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
    };

    try {
        console.log('▶️ Executing Flow...');
        const execution = await engine.executeFlow(sampleFlow);

        console.log('✅ Flow Execution Completed');
        console.log('Status:', execution.status);
        console.log('Result:', JSON.stringify(execution.result, null, 2));

        if (execution.status === 'completed') {
            console.log('🎉 Verification PASSED');
        } else {
            console.error('❌ Verification FAILED');
            process.exit(1);
        }

    } catch (error) {
        console.error('❌ Verification Error:', error);
        process.exit(1);
    }
}

verifyFlowEngine();
