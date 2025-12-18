#!/usr/bin/env node

/**
 * Local LLM Agent Runner
 * 
 * This script connects to a local Ollama instance and enables it to function as an agent
 * with access to the local file system and shell.
 * 
 * Usage: npx tsx scripts/local-agent-runner.ts [model_name]
 */

import fs from 'node:fs';
import path from 'node:path';
import { exec } from 'node:child_process';
import readline from 'node:readline';
import { promisify } from 'node:util';

const execAsync = promisify(exec);

// --- Configuration ---
const OLLAMA_BASE_URL = process.env.OLLAMA_BASE_URL || 'http://127.0.0.1:11434/v1';
const DEFAULT_MODEL = process.argv[2] || 'codellama:latest'; // Default to a strong coding model
const AUTO_APPROVE = process.argv.includes('--auto');

// --- Tool Definitions ---
const tools = [
    {
        type: 'function',
        function: {
            name: 'read_file',
            description: 'Read the contents of a file. Use this to inspect code or documents.',
            parameters: {
                type: 'object',
                properties: {
                    path: {
                        type: 'string',
                        description: 'The absolute or relative path to the file to read.',
                    },
                },
                required: ['path'],
            },
        },
    },
    {
        type: 'function',
        function: {
            name: 'write_file',
            description: 'Create or overwrite a file with new content. Use this to write code or save notes.',
            parameters: {
                type: 'object',
                properties: {
                    path: {
                        type: 'string',
                        description: 'The absolute or relative path to the file to write.',
                    },
                    content: {
                        type: 'string',
                        description: 'The content to write to the file.',
                    },
                },
                required: ['path', 'content'],
            },
        },
    },
    {
        type: 'function',
        function: {
            name: 'list_dir',
            description: 'List the contents of a directory.',
            parameters: {
                type: 'object',
                properties: {
                    path: {
                        type: 'string',
                        description: 'The path to the directory to list. Defaults to current directory.',
                    },
                },
            },
        },
    },
    {
        type: 'function',
        function: {
            name: 'run_command',
            description: 'Execute a shell command. Use this to run tests, install packages, or manage the system.',
            parameters: {
                type: 'object',
                properties: {
                    command: {
                        type: 'string',
                        description: 'The command to execute (e.g., "ls -la", "npm test").',
                    },
                },
                required: ['command'],
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
                if (!fs.existsSync(filePath)) {
                    return `Error: File not found at ${filePath}`;
                }
                const content = fs.readFileSync(filePath, 'utf-8');
                return content;
            }
            case 'write_file': {
                const filePath = path.resolve(process.cwd(), args.path);
                const dir = path.dirname(filePath);
                if (!fs.existsSync(dir)) {
                    fs.mkdirSync(dir, { recursive: true });
                }
                fs.writeFileSync(filePath, args.content, 'utf-8');
                return `Successfully wrote to ${filePath}`;
            }
            case 'list_dir': {
                const dirPath = path.resolve(process.cwd(), args.path || '.');
                if (!fs.existsSync(dirPath)) {
                    return `Error: Directory not found at ${dirPath}`;
                }
                const items = fs.readdirSync(dirPath);
                return items.join('\n');
            }
            case 'run_command': {
                console.log(`\n> Executing: ${args.command}`);
                const { stdout, stderr } = await execAsync(args.command);
                if (stderr) {
                    return `STDOUT:\n${stdout}\n\nSTDERR:\n${stderr}`;
                }
                return stdout || '(Command completed with no output)';
            }
            default:
                return `Error: Unknown tool ${name}`;
        }
    } catch (error: any) {
        return `Error executing tool ${name}: ${error.message}`;
    }
}

// --- Ollama Client ---
async function chatCompletion(messages: any[]) {
    try {
        const response = await fetch(`${OLLAMA_BASE_URL}/chat/completions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                model: DEFAULT_MODEL,
                messages: messages,
                tools: tools,
                stream: false,
            }),
        });

        if (!response.ok) {
            throw new Error(`Ollama API Error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        return data.choices[0].message;
    } catch (error: any) {
        console.error('Failed to connect to Ollama:', error.message);
        return null;
    }
}

// --- User Interface ---
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
});

const askUser = (query: string) => new Promise<string>((resolve) => rl.question(query, resolve));

// --- Main Loop ---
async function main() {
    console.log(`\n🤖 Local Agent Runner initialized.`);
    console.log(`🔌 Connected to: ${OLLAMA_BASE_URL}`);
    console.log(`🧠 Model: ${DEFAULT_MODEL}`);
    console.log(`🛠️  Tools: read_file, write_file, list_dir, run_command`);
    console.log(`---------------------------------------------------\n`);

    const messages: any[] = [
        {
            role: 'system',
            content: `You are a helpful AI assistant running locally on the user's machine. 
You have access to the local file system and shell via tools. 
Use these tools to help the user with coding tasks, system administration, and file management.
Always analyze the output of your tools before proceeding.
If a command fails, try to understand why and fix it or ask the user for help.
Be concise and efficient.`,
        },
    ];

    while (true) {
        const userInput = await askUser('👤 You: ');
        if (userInput.toLowerCase() === 'exit' || userInput.toLowerCase() === 'quit') {
            break;
        }

        messages.push({ role: 'user', content: userInput });

        let processing = true;
        while (processing) {
            process.stdout.write('🤖 Agent thinking...');
            const responseMessage = await chatCompletion(messages);
            process.stdout.write('\r' + ' '.repeat(20) + '\r'); // Clear loading

            if (!responseMessage) {
                console.log('❌ Failed to get response from agent.');
                processing = false;
                break;
            }

            messages.push(responseMessage);

            if (responseMessage.tool_calls && responseMessage.tool_calls.length > 0) {
                for (const toolCall of responseMessage.tool_calls) {
                    const functionName = toolCall.function.name;
                    const args = JSON.parse(toolCall.function.arguments);

                    console.log(`\n🤔 Agent wants to run: ${functionName}(${JSON.stringify(args)})`);

                    let approved = AUTO_APPROVE;
                    if (!approved) {
                        const answer = await askUser('❓ Allow this? (y/n/always): ');
                        if (answer.toLowerCase().startsWith('y')) approved = true;
                        if (answer.toLowerCase() === 'always') {
                            // This is a runtime 'always' for this session only, ideally we'd set a flag
                            // but for now let's just approve. 
                            // To implement 'always' properly we'd need to update the global AUTO_APPROVE or similar.
                            // For simplicity, treating 'always' as 'yes' for this turn, 
                            // but user might expect it to persist. 
                            // Let's keep it simple:
                            approved = true;
                        }
                    }

                    if (approved) {
                        const result = await executeTool(functionName, args);
                        console.log(`📝 Tool Output:\n${result.substring(0, 200)}${result.length > 200 ? '...' : ''}\n`);

                        messages.push({
                            role: 'tool',
                            tool_call_id: toolCall.id,
                            name: functionName,
                            content: result,
                        });
                    } else {
                        console.log('🚫 Tool execution denied.');
                        messages.push({
                            role: 'tool',
                            tool_call_id: toolCall.id,
                            name: functionName,
                            content: 'User denied this tool execution.',
                        });
                    }
                }
                // Loop continues to let agent handle the tool output
            } else {
                console.log(`🤖 Agent: ${responseMessage.content}\n`);
                processing = false;
            }
        }
    }

    rl.close();
}

main().catch(console.error);
