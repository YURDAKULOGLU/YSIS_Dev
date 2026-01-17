class RAGMemory {
    private persistPath: string;

    constructor() {
        this.persistPath = "path/to/chroma/db"; // Bu deeri uygun ekilde ayarlayn

        // st dizinin var olduundan emin olun
        const parentDir = path.dirname(this.persistPath);
        if (!fs.existsSync(parentDir)) {
            fs.mkdirSync(parentDir, { recursive: true });
        }

        console.log(`[RAGMemory] Balatlyor: ${this.persistPath}`);
    }

    public query(query: string, nResults: number = 5): any[] {
        // Sorgu ilemini burada gerekletirin
        return [];
    }
}
