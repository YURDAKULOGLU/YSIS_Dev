import { Mem0Bridge } from "src/agentic/bridges/mem0_bridge";

const mem0 = new Mem0Bridge();

export function retrieveMemory(query: string): string {
    // Use Mem0Bridge to retrieve memory based on query
    const relevantInfo = mem0.add(query, {});
    return `Relevant information for query: ${relevantInfo}`;
}

export function storeMemory(data: string, metadata: any = {}): void {
    // Store data in Mem0Bridge with optional metadata
    mem0.add(data, metadata);
}
