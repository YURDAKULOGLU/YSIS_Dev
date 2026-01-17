# xAI

You’ll need a [xAI API key](https://console.x.ai.).

First, install aider:

```
python -m pip install aider-install
aider-install
```

Then configure your API keys:

```
export XAI_API_KEY=<key> # Mac/Linux
setx   XAI_API_KEY <key> # Windows, restart shell after setx
```

Start working with aider and xAI on your codebase:

```
# Change directory into your codebase
cd /to/your/project

# Grok 3
aider --model xai/grok-3-beta

# Grok 3 fast (faster, more expensive)
aider --model xai/grok-3-fast-beta

# Grok 3 Mini
aider --model xai/grok-3-mini-beta

# Grok 3 Mini fast (faster, more expensive)
aider --model xai/grok-3-mini-fast-beta

# List models available from xAI
aider --list-models xai/
```

The Grok 3 Mini models support the `--reasoning-effort` flag.
See the [reasoning settings documentation](/docs/config/reasoning.html) for details.
Example:

```
aider --model xai/grok-3-mini-beta --reasoning-effort high
```