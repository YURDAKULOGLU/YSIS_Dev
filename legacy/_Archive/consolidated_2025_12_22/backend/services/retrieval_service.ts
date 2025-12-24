import { RagModel } from 'some-rag-library'; // Uygun RAG kütüphanesini import edin

class RetrievalService {
    private ragModel: RagModel;

    constructor() {
        this.ragModel = new RagModel(); // RAG modelini başlatın
    }

    async retrieve(query: string): Promise<string[]> {
        return await this.ragModel.retrieve(query); // RAG modeli ile veri çekin
    }
}

export const retrievalService = new RetrievalService();
