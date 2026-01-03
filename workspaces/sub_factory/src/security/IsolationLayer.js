class IsolationLayer {
    constructor() {
        this.sandbox = {};
    }

    runInSandbox(plugin, params) {
        const context = { ...this.sandbox };
        return plugin.execute.call(context, params);
    }
}

module.exports = IsolationLayer;
