import { PluginInterface } from '../plugins/PluginInterface';

class PluginRegistry {
    private plugins: Map<string, PluginInterface>;

    constructor() {
        this.plugins = new Map();
    }

    register(plugin: PluginInterface): void {
        if (this.plugins.has(plugin.name)) {
            throw new Error(`Plugin already registered: ${plugin.name}`);
        }
        this.plugins.set(plugin.name, plugin);
        console.log(`Plugin registered: ${plugin.name}`);
    }

    get(name: string): PluginInterface | undefined {
        return this.plugins.get(name);
    }

    getAll(): Map<string, PluginInterface> {
        return this.plugins;
    }
}

export default PluginRegistry;
