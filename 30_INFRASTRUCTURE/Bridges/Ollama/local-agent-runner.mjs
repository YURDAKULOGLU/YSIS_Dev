#!/usr/bin/env node

/**
 * Local LLM Agent Runner (Async Worker Mode - ES Module)
 * 
 * This script runs as a background worker, watching the 'Inbox' folder for JSON tasks.
 * When a task is found, it processes it using the local Ollama instance and writes the result to 'Outbox'.
 * 
 * Usage: node .YBIS_Dev/30_INFRASTRUCTURE/Bridges/Ollama/local-agent-runner.mjs [--model <model_name>] [--once]
 */

import * as fs from 'node:fs';
import * as path from 'node:path';
import { exec } from 'node:child_process';
import { promisify } from 'node:util';

const execAsync = promisify(exec);

// --- Configuration ---
const OLLAMA_BASE_URL = process.env.OLLAMA_BASE_URL || 'http://127.0.0.1:11434/v1';

// Parse arguments correctly
const args = process.argv.slice(2);
let DEFAULT_MODEL = 'qwen2.5-coder:14b'; // Upgraded to Qwen 2.5 Coder 14B
let RUN_ONCE = false;

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--model' && args[i + 1]) {
        DEFAULT_MODEL = args[i + 1];
        i++; // Skip next arg as it's the value
    } else if (args[i] === '--once') {
        RUN_ONCE = true;
    }
}

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
async function executeTool(name, args) {
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
    } catch (error) {
        return `Error executing tool ${name}: ${error.message}`;
    }
}

// --- Ollama Client ---
async function chatCompletion(messages, enableTools = true) {
    try {
        const body = {
            model: DEFAULT_MODEL,
            messages: messages,
            stream: false,
        };

        if (enableTools) {
            body.tools = tools;
        }

        const response = await fetch(`${OLLAMA_BASE_URL}/chat/completions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Ollama API Error: ${response.status} - ${errorText}`);
        }
        const data = await response.json();
        return data.choices[0].message;
    } catch (error) {
        log(`Ollama connection failed: ${error.message}`, 'ERROR');
        return null;
    }
}

// --- Logging ---
function log(message, level = 'INFO') {
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] [${level}] ${message}`;
    console.log(logEntry);
    
    // Ensure logs dir exists
    if (!fs.existsSync(LOGS_DIR)) fs.mkdirSync(LOGS_DIR, { recursive: true });
    fs.appendFileSync(path.join(LOGS_DIR, 'agent_node.log'), logEntry + '\n');
}

// --- Task Processing ---
async function processTask(taskPath) {
    try {
        log(`Processing task: ${path.basename(taskPath)}`);
        const taskContent = fs.readFileSync(taskPath, 'utf-8');
        const task = JSON.parse(taskContent);

        const messages = [
            { role: 'system', content: 'You are an autonomous AI agent. You have file system access. Execute the user request strictly.' },
            { role: 'user', content: task.instruction || 'No instruction provided.' }
        ];

        log(`Sending instruction to Ollama: ${task.instruction}`);
        
        const requiresTools = task.instruction.includes('read_file') || task.instruction.includes('write_file') || task.instruction.includes('list_dir') || task.instruction.includes('run_command');
        
        let responseMessage = await chatCompletion(messages, requiresTools);
        let finalResult = '';

        if (responseMessage) {
            // Check for native tool_calls first
            if (responseMessage.tool_calls && responseMessage.tool_calls.length > 0) {
                log(`Executing tool(s) from native tool_calls array.`);
                for (const toolCall of responseMessage.tool_calls) {
                    const functionName = toolCall.function.name;
                    const args = JSON.parse(toolCall.function.arguments);
                    
                    log(`Executing tool: ${functionName} with args: ${JSON.stringify(args)}`);
                    const result = await executeTool(functionName, args);
                    
                    messages.push({
                        role: 'tool',
                        tool_call_id: toolCall.id,
                        name: functionName,
                        content: result,
                    });
                }
                // Get final response after tools
                const followUp = await chatCompletion(messages, false);
                finalResult = followUp ? followUp.content : 'Tool execution completed.';
            } else if (responseMessage.content) { // If no native tool_calls, check content for JSON tool call
                let contentText = responseMessage.content;
                
                // Strip Markdown code blocks if present
                contentText = contentText.replace(/```json/g, '').replace(/```/g, '').trim();

                const jsonStartIndex = contentText.indexOf('{');
                const jsonEndIndex = contentText.lastIndexOf('}');
                
                if (jsonStartIndex !== -1 && jsonEndIndex !== -1 && jsonEndIndex > jsonStartIndex) {
                    const jsonString = contentText.substring(jsonStartIndex, jsonEndIndex + 1);
                    try {
                        let toolCallInContent = JSON.parse(jsonString);
                        
                        // Handle array format (e.g. Qwen returns [ {name: ...} ])
                        if (Array.isArray(toolCallInContent) && toolCallInContent.length > 0) {
                            toolCallInContent = toolCallInContent[0];
                        }

                        if (toolCallInContent.name && toolCallInContent.arguments) { // Qwen uses 'arguments', OpenAI 'parameters'
                             // Normalize arguments/parameters
                             const args = toolCallInContent.arguments || toolCallInContent.parameters;
                             
                            log(`Executing tool from content (parsed JSON): ${toolCallInContent.name} with args: ${JSON.stringify(args)}`);
                            const result = await executeTool(toolCallInContent.name, args);
                            
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
                    finalResult = responseMessage.content; // Plain content
                }
            }
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
        
        fs.renameSync(taskPath, taskPath + '.done');

    } catch (error) {
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
    if (!fs.existsSync(LOGS_DIR)) fs.mkdirSync(LOGS_DIR, { recursive: true });

    while (true) {
        try {
            const files = fs.readdirSync(INBOX_DIR).filter(f => f.endsWith('.json') && !f.startsWith('trigger_'));
            
            for (const file of files) {
                await processTask(path.join(INBOX_DIR, file));
            }
            
            if (RUN_ONCE) {
                log('Run once completed. Exiting.');
                break;
            }
            
            await new Promise(resolve => setTimeout(resolve, 2000));
        } catch (e) {
            log(`Main loop error: ${e.message}`, 'ERROR');
            if (RUN_ONCE) break;
            await new Promise(resolve => setTimeout(resolve, 5000));
        }
    }
}

main();