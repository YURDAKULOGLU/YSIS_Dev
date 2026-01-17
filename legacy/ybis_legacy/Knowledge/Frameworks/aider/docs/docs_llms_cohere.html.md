# Cohere

Cohere offers *free* API access to their models.
Their Command-R+ model works well with aider
as a *very basic* coding assistant.
You’ll need a [Cohere API key](https://dashboard.cohere.com/welcome/login).

First, install aider:

```
python -m pip install aider-install
aider-install
```

Then configure your API keys:

```
export COHERE_API_KEY=<key> # Mac/Linux
setx   COHERE_API_KEY <key> # Windows, restart shell after setx
```

Start working with aider and Cohere on your codebase:

```
# Change directory into your codebase
cd /to/your/project

aider --model command-r-plus-08-2024

# List models available from Cohere
aider --list-models cohere_chat/
```