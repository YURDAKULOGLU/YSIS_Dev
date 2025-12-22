# YBIS_Dev Plugin Onboarding Guide

## Giriş
Hoş geldiniz YBIS_Dev eklenti geliştirme kılavuzuna! Bu belge, kendi eklentilerinizi oluşturmayı, kaydetmeyi ve test etmeyi adım adım anlatacaktır.

## Adım 1: Eklentinizi Tanımlayın
`src/plugins` dizininde yeni bir TypeScript dosyası oluşturun. `../plugins/PluginInterface`'den `PluginInterface`'i uygulayın.

Örnek:
```typescript
import { PluginInterface } from '../plugins/PluginInterface';

class MyPlugin implements PluginInterface {
    name = 'MyPlugin';
    version = '1.0.0';
    description = 'YBIS_Dev için örnek bir eklenti';
    permissions = ['execute']; // Gerekli izinleri belirtin

    init(): void {
        console.log(`${this.name} başlatıldı.`);
    }

    async execute(params: any): Promise<any> {
        try {
            if (typeof this.sanitizeInputs === 'function') {
                this.sanitizeInputs.call(this, params);
            }
            // Ekleme mantığınızı buraya yazın
            return { success: true, data: params };
        } catch (error) {
            console.error(`Eklenti çalıştırılırken hata oluştu:`, error);
            return { success: false, error };
        }
    }

    destroy(): void {
        console.log(`${this.name} sonlandırıldı.`);
    }

    sanitizeInputs?(params: any): void {
        // Girdi verilerini temizleme mantığınızı buraya yazın
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
}

export default MyPlugin;
```

## Adım 2: Güvenlik İzni Tanımlayın
Eklentilerinizin çalıştırılması için gerekli izinleri `permissions` dizisinde belirtin. Birden fazla izin ekleyebilirsiniz.

Örnek:
```typescript
class MyPlugin implements PluginInterface {
    name = 'MyPlugin';
    version = '1.0.0';
    description = 'YBIS_Dev için örnek bir eklenti';
    permissions = ['execute', 'read']; // Gerekli izinleri belirtin

    init(): void {
        console.log(`${this.name} başlatıldı.`);
    }

    async execute(params: any): Promise<any> {
        try {
            // Ekleme mantığınızı buraya yazın
            return { success: true, data: params };
        } catch (error) {
            console.error(`Eklenti çalıştırılırken hata oluştu:`, error);
            return { success: false, error };
        }
    }

    destroy(): void {
        console.log(`${this.name} sonlandırıldı.`);
    }
}
```

## Adım 3: Güvenlik Ölçümleri
Eklentilerinizin çalıştırılması sırasında güvenlik önlemlerini sağlamak için `PluginManager` sınıfında gerekli kontrolleri uygulayın. Özellikle, eklentinin çalıştırabileceği komutları ve girdi parametrelerini kontrol edin.

Örnek:
```typescript
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
```

## Adım 4: Eklentinizi Kaydedin
Ana uygulama dosyanızda veya ayrı bir eklenti kaydetme dosyasında, `PluginManager` kullanarak eklentinizi içe aktarın ve kaydedin.

Örnek:
```typescript
import PluginManager from '../core/Infrastructure';
import MyPlugin from './plugins/MyPlugin';

const pluginManager = new PluginManager();
pluginManager.register(new MyPlugin());
```

## Adım 5: Eklentinizi Test Edin
Test ortamınızın ayarlandığından emin olun. `PluginManager`'ın `executeAll` yöntemini kullanarak eklentinizi test edebilirsiniz.

Örnek:
```typescript
(async () => {
    const results = await pluginManager.executeAll({ key: 'value' });
    console.log(results);
})();
```

## Adım 6: PluginManager'ı Kullanarak Eklentileri Yönetin
`PluginManager` sınıfını kullanarak eklentilerinizi kaydedebilir ve yönetebilirsiniz.

Örnek:
```typescript
import PluginManager from '../core/Infrastructure';
import MyPlugin from './plugins/MyPlugin';

const pluginManager = new Plugin0PluginManager();
pluginManager.register(new MyPlugin());

(async () => {
    const results = await pluginManager.executeAll({ key: 'value' }, ['execute', 'read']);
    console.log(results);
})();
```

## Ek Güvenlik Ölçümleri
Eklentilerinizin çalıştırılması sırasında güvenlik önlemlerini sağlamak için `PluginManager` sınıfında gerekli kontrolleri uygulayın. Özellikle, eklentinin çalıştırabileceği komutları ve girdi parametrelerini kontrol edin.

Örnek:
```typescript
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
```

## Sonuç
Artık YBIS_Dev'e eklenti geliştirebilir ve entegre edebilirsiniz. Mutlu kodlama!
