import { expect } from 'chai';
import PluginManager from '../src/core/Infrastructure';
import MyPlugin from '../src/plugins/MyPlugin';

describe('Plugin Architecture Tests', () => {
    let pluginManager: PluginManager;

    beforeEach(() => {
        pluginManager = new PluginManager();
        pluginManager.register(new MyPlugin());
    });

    it('should register a plugin successfully', () => {
        expect(pluginManager).to.have.property('plugins').with.lengthOf(1);
    });

    it('should execute the plugin and return expected result', async () => {
        const results = await pluginManager.executeAll({ key: 'value' });
        expect(results[0]).to.deep.equal({ success: true, data: { key: 'value' } });
    });

    it('should destroy all plugins successfully', () => {
        pluginManager.destroyAll();
        expect(pluginManager).to.have.property('plugins').with.lengthOf(0);
    });
});
import { PluginInterface } from '../src/plugins/PluginInterface';
import PluginManager from '../src/core/Infrastructure';

class MockPlugin implements PluginInterface {
    name = 'MockPlugin';
    version = '1.0.0';
    description = 'Bir test eklenti';
    permissions = ['execute'];

    init(): void {
        console.log(`${this.name} başlatıldı.`);
    }

    async execute(params: any): Promise<any> {
        return { success: true, data: params };
    }

    destroy(): void {
        console.log(`${this.name} sonlandırıldı.`);
    }
}

describe('PluginManager', () => {
    let pluginManager: PluginManager;

    beforeEach(() => {
        pluginManager = new PluginManager();
    });

    it('should register a valid plugin', () => {
        const mockPlugin = new MockPlugin();
        expect(() => pluginManager.register(mockPlugin)).not.toThrow();
    });

    it('should execute all registered plugins', async () => {
        const mockPlugin1 = new MockPlugin();
        const mockPlugin2 = new MockPlugin();

        pluginManager.register(mockPlugin1);
        pluginManager.register(mockPlugin2);

        const results = await pluginManager.executeAll({ key: 'value' });
        expect(results).toHaveLength(2);
        expect(results[0]).toEqual({ success: true, data: { key: 'value' } });
        expect(results[1]).toEqual({ success: true, data: { key: 'value' } });
    });

    it('should handle plugin execution errors', async () => {
        class FaultyPlugin implements PluginInterface {
            name = 'FaultyPlugin';
            version = '1.0.0';
            description = 'Hata veren bir eklenti';
            permissions = ['execute'];

            init(): void {}
            async execute(params: any): Promise<any> {
                throw new Error('Execution failed');
            }
            destroy(): void {}
        }

        const faultyPlugin = new FaultyPlugin();
        pluginManager.register(faultyPlugin);

        const results = await pluginManager.executeAll({ key: 'value' });
        expect(results).toHaveLength(1);
        expect(results[0]).toHaveProperty('success', false);
        expect(results[0]).toHaveProperty('error');
    });

    it('should destroy all registered plugins', () => {
        const mockPlugin1 = new MockPlugin();
        const mockPlugin2 = new MockPlugin();

        pluginManager.register(mockPlugin1);
        pluginManager.register(mockPlugin2);

        console.log = jest.fn(); // Suppress console output for this test
        pluginManager.destroyAll();
        expect(console.log).toHaveBeenCalledTimes(2);
    });
});
import { PluginInterface } from '../plugins/PluginInterface';
import PluginManager from '../core/Infrastructure';

class MockPlugin implements PluginInterface {
    name = 'MockPlugin';
    version = '1.0.0';
    description = 'Bir test eklenti';
    permissions = ['execute'];

    init(): void {
        console.log(`${this.name} başlatıldı.`);
    }

    async execute(params: any): Promise<any> {
        return { success: true, data: params };
    }

    destroy(): void {
        console.log(`${this.name} sonlandırıldı.`);
    }
}

class FaultyPlugin implements PluginInterface {
    name = 'FaultyPlugin';
    version = '1.0.0';
    description = 'Hata veren bir eklenti';
    permissions = ['execute'];

    init(): void {}
    async execute(params: any): Promise<any> {
        throw new Error('Execution failed');
    }
    destroy(): void {}
}

describe('PluginManager', () => {
    let pluginManager: PluginManager;

    beforeEach(() => {
        pluginManager = new PluginManager();
    });

    it('should register a valid plugin', () => {
        const mockPlugin = new MockPlugin();
        expect(() => pluginManager.register(mockPlugin)).not.toThrow();
    });

    it('should handle plugin execution errors', async () => {
        const faultyPlugin = new FaultyPlugin();
        pluginManager.register(faultyPlugin);
        const results = await pluginManager.executeAll({ key: 'value' });
        expect(results[0].success).toBe(false);
        expect(results[0].error.message).toBe('Execution failed');
    });

    it('should not execute a plugin without required permissions', async () => {
        class NoPermissionPlugin implements PluginInterface {
            name = 'NoPermissionPlugin';
            version = '1.0.0';
            description = 'İzinleri olmayan bir eklenti';
            permissions: string[] = [];

            init(): void {}
            async execute(params: any): Promise<any> {
                return { success: true, data: params };
            }
            destroy(): void {}
        }

        const noPermissionPlugin = new NoPermissionPlugin();
        pluginManager.register(noPermissionPlugin);
        await expect(pluginManager.executeAll({ key: 'value' }, ['execute'])).rejects.toThrow('Plugin NoPermissionPlugin does not have the required permissions.');
    });
});
````
