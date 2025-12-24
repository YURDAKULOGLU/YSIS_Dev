import { MemoryService, RAGMemory } from './base_memory_service';
import * as fs from 'fs';
import * as path from 'path';

export class RagRetriever {
    private ragMemory: RAGMemory;

    constructor(ragMemory: RAGMemory) {
        this.ragMemory = ragMemory;
    }

    async retrieve(query: string): Promise<string[]> {
        // Sorguyu RAGMemory ile işle ve sonuçları döndür
        return await this.ragMemory.query(query);
    }
}

export class YBISMemoryService extends MemoryService {
    private ragRetriever: RagRetriever;
    private ragMemory: RAGMemory;
    private config: any;

    constructor() {
        super();
        this.loadConfig();
        const ragConfig = this.config.memory.rag_config;
        this.ragMemory = new RAGMemory(ragConfig);
        this.ragRetriever = new RagRetriever(this.ragMemory);
    }

    private loadConfig(): void {
        const configPath = path.join(__dirname, '../../config/settings.json');
        const configFile = fs.readFileSync(configPath, 'utf8');
        this.config = JSON.parse(configFile);
    }

    async retrieve(query: string): Promise<string[]> {
        // RAGRetriever kullanarak sorguyu işle ve sonuçları döndür
        return await this.ragRetriever.retrieve(query);
    }

    async generateResponse(query: string, context?: string[]): Promise<string> {
        if (!context) {
            context = await this.retrieve(query);
        }
        const generativeModelConfig = this.config.generative_model;
        const prompt = `Context: ${context.join('\n')}\nQuery: ${query}\nAnswer:`;
        try {
            const response = await fetch(`https://api.openai.com/v1/engines/${generativeModelConfig.model_name}/completions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${generativeModelConfig.api_key}`
                },
                body: JSON.stringify({
                    prompt: prompt,
                    max_tokens: 150
                })
            });
            const data = await response.json();
            return data.choices[0].message.content.trim(); // Assuming the API returns a message object with content
        } catch (error) {
            console.error("Error generating response:", error);
            throw new Error("Failed to generate response");
        }
    }
}
import * as fs from 'fs';
import * as path from 'path';

export class RagRetriever {
    private ragMemory: RAGMemory;

    constructor(ragMemory: RAGMemory) {
        this.ragMemory = ragMemory;
    }

    async retrieve(query: string): Promise<string[]> {
        // Sorguyu RAGMemory ile işle ve sonuçları döndür
        return await this.ragMemory.query(query);
    }
}

export class YBISMemoryService extends MemoryService {
    private ragRetriever: RagRetriever;
    private ragMemory: RAGMemory;
    private config: any;

    constructor() {
        super();
        this.loadConfig();
        const ragConfig = this.config.memory.rag_config;
        this.ragMemory = new RAGMemory(ragConfig);
        this.ragRetriever = new RagRetriever(this.ragMemory);
    }

    private loadConfig(): void {
        const configPath = path.join(__dirname, '../../config/settings.json');
        const configFile = fs.readFileSync(configPath, 'utf8');
        this.config = JSON.parse(configFile);
    }

    async retrieve(query: string): Promise<string[]> {
        // RAGRetriever kullanarak sorguyu işle ve sonuçları döndür
        return await this.ragRetriever.retrieve(query);
    }

    async generateResponse(query: string, context?: string[]): Promise<string> {
        if (!context) {
            context = await this.retrieve(query);
        }
        const generativeModelConfig = this.config.generative_model;
        const prompt = `Context: ${context.join('\n')}\nQuery: ${query}\nAnswer:`;
        try {
            const response = await fetch(`https://api.openai.com/v1/engines/${generativeModelConfig.model_name}/completions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${generativeModelConfig.api_key}`
                },
                body: JSON.stringify({
                    prompt: prompt,
                    max_tokens: 150
                })
            });
            const data = await response.json();
            return data.choices[0].message.content.trim(); // Assuming the API returns a message object with content
        } catch (error) {
            console.error("Error generating response:", error);
            throw new Error("Failed to generate response");
        }
    }
}
import * as fs from 'fs';
import * as path from 'path';
import * as fs from 'fs';
import * as path from 'path';

export class RagRetriever {
    private ragMemory: RAGMemory;

    constructor(ragMemory: RAGMemory) {
        this.ragMemory = ragMemory;
    }

    async retrieve(query: string): Promise<string[]> {
        // Sorguyu RAGMemory ile işle ve sonuçları döndür
        return await this.ragMemory.query(query);
    }
}

export class YBISMemoryService extends MemoryService {
    private ragRetriever: RagRetriever;
    private ragMemory: RAGMemory;
    private config: any;

    constructor() {
        super();
        this.loadConfig();
        const ragConfig = this.config.memory.rag_config;
        this.ragMemory = new RAGMemory(ragConfig);
        this.ragRetriever = new RagRetriever(this.ragMemory);
    }

    private loadConfig(): void {
        const configPath = path.join(__dirname, '../../config/settings.json');
        const configFile = fs.readFileSync(configPath, 'utf8');
        this.config = JSON.parse(configFile);
    }

    async retrieve(query: string): Promise<string[]> {
        // RAGRetriever kullanarak sorguyu işle ve sonuçları döndür
        return await this.ragRetriever.retrieve(query);
    }

    async generateResponse(query: string, context?: string[]): Promise<string> {
        if (!context) {
            context = await this.retrieve(query);
        }
        const generativeModelConfig = this.config.generative_model;
        const prompt = `Context: ${context.join('\n')}\nQuery: ${query}\nAnswer:`;
        try {
            const response = await fetch(`https://api.openai.com/v1/engines/${generativeModelConfig.model_name}/completions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${generativeModelConfig.api_key}`
                },
                body: JSON.stringify({
                    prompt: prompt,
                    max_tokens: 150
                })
            });
            const data = await response.json();
            return data.choices[0].message.content.trim(); // Assuming the API returns a message object with content
        } catch (error) {
            console.error("Error generating response:", error);
            throw new Error("Failed to generate response");
        }
    }
}
}
