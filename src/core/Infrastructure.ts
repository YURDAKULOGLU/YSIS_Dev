import { PluginInterface } from '../plugins/PluginInterface';

interface PluginConfig {
    name: string;
    version: string;
    description: string;
    permissions: string[];
}

class PluginManager {
    private plugins: PluginInterface[] = [];

    register(plugin: PluginInterface): void {
        if (!this.validatePlugin(plugin)) {
            throw new Error(`Eklenti ${plugin.name} geçerli değil.`);
        }
        this.plugins.push(plugin);
        plugin.init();
    }

    async executeAll(params: any, requiredPermissions: string[] = ['execute']): Promise<any[]> {
        const results: any[] = [];
        for (const plugin of this.plugins) {
            try {
                if (!this.checkPermissions(plugin, requiredPermissions)) {
                    throw new Error(`Eklenti ${plugin.name} gerekli izinlere sahip değil.`);
                }
                if (!this.isSafeEnvironment()) {
                    throw new Error(`Eklenti ${plugin.name}, güvenli bir ortamda çalıştırılamıyor.`);
                }
                this.enforceSandbox(plugin);
                if (typeof plugin.sanitizeInputs === 'function') {
                    plugin.sanitizeInputs.call(plugin, params);
                }
                const result = await plugin.execute(params);
                results.push(result);
            } catch (error) {
                console.error(`Eklenti ${plugin.name} çalıştırılırken hata oluştu:`, error);
                results.push({ success: false, error });
            }
        }
        return results;
    }

    destroyAll(): void {
        for (const plugin of this.plugins) {
            try {
                plugin.destroy();
            } catch (error) {
                console.error(`Eklenti ${plugin.name} sonlandırılırken hata oluştu:`, error);
            }
        }
    }

    private validatePlugin(plugin: PluginInterface): boolean {
        // Temel doğrulama, genişletilebilir
        if (!plugin.name || !plugin.version || !plugin.description) {
            return false;
        }
        return true;
    }

    private checkPermissions(plugin: PluginInterface, requiredPermissions: string[]): boolean {
        // İzin kontrolü mantığı burada uygulanır
        if (!plugin.permissions || !Array.isArray(plugin.permissions)) {
            console.error(`Eklenti ${plugin.name} geçersiz izinler içeriyor.`);
            return false;
        }

        for (const perm of requiredPermissions) {
            if (typeof perm !== 'string' || !plugin.permissions.includes(perm)) {
                console.error(`Eklenti ${plugin.name}, '${perm}' iznine sahip değil.`);
                return false;
            }
        }
        return true;
    }

    // Güvenlik önlemleri için ek metotlar
    private enforceSandbox(plugin: PluginInterface): void {
        if (!this.isSafeEnvironment()) {
            throw new Error(`Eklenti ${plugin.name}, güvenli bir ortamda çalıştırılamıyor.`);
        }
        console.log(`Eklenti ${plugin.name} sandbox içinde çalıştırılıyor.`);

        // Sandbox kısıtlamalarını uygula
        this.applySandboxConstraints(plugin);
    }

    private applySandboxConstraints(plugin: PluginInterface): void {
        // Örnek olarak, belirli komutların çalıştırılmasını engelle
        const restrictedCommands = ['rm', 'shutdown'];
        if (plugin.execute.toString().includes(restrictedCommands.join('||'))) {
            throw new Error(`Eklenti ${plugin.name}, yasal olmayan komutları içeriyor.`);
        }
    }

    private sanitizeInputs(plugin: PluginInterface, params: any): void {
        // Girdi verilerini temizle ve doğrula
        if (typeof params !== 'object' || params === null) {
            throw new Error('Geçersiz girdi parametreleri.');
        }
        for (const key in params) {
            if (params.hasOwnProperty(key)) {
                const value = params[key];
                if (typeof value === 'string') {
                    // Örnek olarak, SQL enjeksiyonu önleme
                    if (/[\';]/.test(value)) {
                        throw new Error('Potansiyel güvenlik ihlali tespit edildi.');
                    }
                }
            }
        }
        console.log(`Girdi verileri temizleniyor.`);
    }

    private isSafeEnvironment(): boolean {
        // Güvenli ortam kontrolü
        return process.env.NODE_ENV === 'production' || process.env.SANDBOX_ENABLED === 'true';
    }
}

export default PluginManager;
