#!/usr/bin/env node

/**
 * Local LLM Agent Runner (Async Worker Mode)
 * 
 * This script runs as a background worker, watching the 'Inbox' folder for JSON tasks.
 * When a task is found, it processes it using the local Ollama instance and writes the result to 'Outbox'.
 * 
 * Usage: npx tsx .YBIS_Dev/30_INFRASTRUCTURE/Bridges/Ollama/local-agent-runner.ts [model_name]
 */

import fs from 'node:fs';
import path from 'node:path';
import { exec } from 'node:child_process';
import { promisify } from 'node:util';

const execAsync = promisify(exec);

// --- Configuration ---
const OLLAMA_BASE_URL = process.env.OLLAMA_BASE_URL || 'http://127.0.0.1:11434/v1';
const DEFAULT_MODEL = process.argv.includes('--model') ? process.argv[process.argv.indexOf('--model') + 1] : 'codellama:latest';
const AUTO_APPROVE = process.argv.includes('--auto');
const RUN_ONCE = process.argv.includes('--once');

// Paths
const YBIS_DEV_ROOT = path.resolve(process.cwd(), '.YBIS_Dev');
const INBOX_DIR = path.join(YBIS_DEV_ROOT, '40_KNOWLEDGE_BASE', 'Memory', 'Inbox');
const OUTBOX_DIR = path.join(YBIS_DEV_ROOT, '40_KNOWLEDGE_BASE', 'Memory', 'Outbox');
const LOGS_DIR = path.join(YBIS_DEV_ROOT, '40_KNOWLEDGE_BASE', 'Memory', 'logs');

// --- Tool Definitions ---
const tools = [
    {
        type: 'function',
        function: {
            name: 'read_file',
            description: 'Read the contents of a file.',
            parameters: {
                type: 'object',
                properties: { path: { type: 'string' } },
                required: ['path'],
            },
        },
    },
    {
        type: 'function',
        function: {
            name: 'write_file',
            description: 'Create or overwrite a file.',
            parameters: {
                type: 'object',
                properties: {
                    path: { type: 'string' },
                    content: { type: 'string' },
                },
                required: ['path', 'content'],
            },
        },
    },
    {
        type: 'function',
        function: {
            name: 'list_dir',
            description: 'List directory contents.',
            parameters: {
                type: 'object',
                properties: { path: { type: 'string' } },
            },
        },
    },
];

// --- Tool Implementations ---
async function executeTool(name: string, args: any): Promise<string> {
    try {
        switch (name) {
            case 'read_file': {
                const filePath = path.resolve(process.cwd(), args.path);
                if (!fs.existsSync(filePath)) return `Error: File not found at ${filePath}`;
                return fs.readFileSync(filePath, 'utf-8');
            }
            case 'write_file': {
                const filePath = path.resolve(process.cwd(), args.path);
                const dir = path.dirname(filePath);
                if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
                fs.writeFileSync(filePath, args.content, 'utf-8');
                return `Successfully wrote to ${filePath}`;
            }
            case 'list_dir': {
                const dirPath = path.resolve(process.cwd(), args.path || '.');
                if (!fs.existsSync(dirPath)) return `Error: Directory not found at ${dirPath}`;
                return fs.readdirSync(dirPath).join('\n');
            }
            default:
                return `Error: Unknown tool ${name}`;
        }
    } catch (error: any) {
        return `Error executing tool ${name}: ${error.message}`;
    }
}

// --- Ollama Client ---
async function chatCompletion(messages: any[], enableTools: boolean = true) { // Added enableTools flag
    try {
        const body: any = {
            model: DEFAULT_MODEL,
            messages: messages,
            stream: false,
        };

        if (enableTools) { // Only send tools if explicitly enabled
            body.tools = tools;
        }

        const response = await fetch(`${OLLAMA_BASE_URL}/chat/completions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });

        if (!response.ok) {
            const errorText = await response.text(); // Read error response
            throw new Error(`Ollama API Error: ${response.status} - ${errorText}`);
        }
        const data = await response.json();
        return data.choices[0].message;
    } catch (error: any) {
        log(`Ollama connection failed: ${error.message}`, 'ERROR');
        return null;
    }
}


// --- Logging ---
function log(message: string, level = 'INFO') {
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] [${level}] ${message}`;
    console.log(logEntry);
    
    // Ensure logs dir exists
    if (!fs.existsSync(LOGS_DIR)) fs.mkdirSync(LOGS_DIR, { recursive: true });
    fs.appendFileSync(path.join(LOGS_DIR, 'agent_node.log'), logEntry + '\n');
}

// --- Task Processing ---
async function processTask(taskPath: string) {
    try {
        log(`Processing task: ${path.basename(taskPath)}`);
        const taskContent = fs.readFileSync(taskPath, 'utf-8');
        const task = JSON.parse(taskContent);

        const messages: any[] = [
            { role: 'system', content: 'You are an autonomous AI agent. You have file system access. Execute the user request strictly.' },
            { role: 'user', content: task.instruction || 'No instruction provided.' }
        ];

        log(`Sending instruction to Ollama: ${task.instruction}`);
        
        // Decide whether to enable tools based on task type or instruction content
        const requiresTools = task.instruction.includes('read_file') || task.instruction.includes('write_file') || task.instruction.includes('list_dir') || task.instruction.includes('run_command');
        
        let responseMessage = await chatCompletion(messages, requiresTools); // Pass requiresTools flag
        let finalResult = '';

        if (responseMessage) {
            messages.push(responseMessage);

            if (responseMessage.tool_calls && responseMessage.tool_calls.length > 0) {
                // If native tool_calls are present, process them (Standard OpenAI way)
                // ... (existing tool processing logic) ...
            } else if (responseMessage.content) { // Check content if tool_calls array is empty
                // Attempt to find and parse JSON within the content
                const contentText = responseMessage.content;
                const jsonStartIndex = contentText.indexOf('{');
                const jsonEndIndex = contentText.lastIndexOf('}');
                
                if (jsonStartIndex !== -1 && jsonEndIndex !== -1 && jsonEndIndex > jsonStartIndex) {
                    const jsonString = contentText.substring(jsonStartIndex, jsonEndIndex + 1);
                    try {
                        const toolCallInContent = JSON.parse(jsonString);
                        if (toolCallInContent.name && toolCallInContent.parameters) {
                            log(`Executing tool from content (parsed JSON): ${toolCallInContent.name} with args: ${JSON.stringify(toolCallInContent.parameters)}`);
                            const result = await executeTool(toolCallInContent.name, toolCallInContent.parameters);
                            
                            messages.push({
                                role: 'tool',
                                name: toolCallInContent.name,
                                content: result,
                            });
                            // Get final response after tool execution
                            const followUp = await chatCompletion(messages, false);
                            finalResult = followUp ? followUp.content : 'Tool execution from content completed.';
                        } else {
                            finalResult = responseMessage.content; // Not a tool, just JSON content
                        }
                    } catch (e) {
                        log(`Content contains JSON but not a valid tool call: ${e.message}`, 'DEBUG');
                        finalResult = responseMessage.content; // Not a tool, just plain content
                    }
                } else {
                    finalResult = responseMessage.content;
                }


        // Save Result
        const resultFile = path.join(OUTBOX_DIR, `result_${path.basename(taskPath)}`);
        fs.writeFileSync(resultFile, JSON.stringify({
            task_id: task.id,
            status: 'COMPLETED',
            agent: 'Node_Agent_v1',
            result: finalResult
        }, null, 2));

        log(`Task completed. Result: ${path.basename(resultFile)}`);
        
        // Rename task to .done
        fs.renameSync(taskPath, taskPath + '.done');

    } catch (error) { // Changed from error: any
        log(`Error processing task: ${error.message}`, 'ERROR');
        fs.renameSync(taskPath, taskPath + '.error');
    }
}

// --- Main Loop ---
async function main() {
    log(`Starting with model: ${DEFAULT_MODEL}`);
    log(`🚀 Node Agent Worker ONLINE. Watching: ${INBOX_DIR} (RunOnce: ${RUN_ONCE})`);
    
    // Ensure dirs exist
    if (!fs.existsSync(INBOX_DIR)) fs.mkdirSync(INBOX_DIR, { recursive: true });
    if (!fs.existsSync(OUTBOX_DIR)) fs.mkdirSync(OUTBOX_DIR, { recursive: true });

    while (true) {
        try {
            // Filter: Must end with .json AND NOT start with 'trigger_'
            const files = fs.readdirSync(INBOX_DIR).filter(f => f.endsWith('.json') && !f.startsWith('trigger_'));
            
            for (const file of files) {
                await processTask(path.join(INBOX_DIR, file));
            }
            
            if (RUN_ONCE) {
                log('Run once completed. Exiting.');
                break;
            }
            
            // Sleep 2 seconds
            await new Promise(resolve => setTimeout(resolve, 2000));
        } catch (e) {
            console.error('Main loop error:', e);
            if (RUN_ONCE) break;
            await new Promise(resolve => setTimeout(resolve, 5000));
        }
    }
}

main();