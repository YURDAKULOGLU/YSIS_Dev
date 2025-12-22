export interface PluginInterface {
    name: string;
    version: string;
    description: string;
    permissions: string[]; // Güvenlik izinleri zorunlu hale getirildi

    init(): void;
    execute(params: any): Promise<any>;
    destroy(): void;

    sanitizeInputs?(params: any): void; // Girdi verilerini temizleme metodu
    communicate(message: string, recipient: string): void; // Yeni iletişim protokolu yöntemi
}
}
