# Aider in your browser

[![

[Aider browser UI demo video](/assets/aider-browser-social.mp4)
](/assets/browser.jpg)](/assets/aider-browser-social.mp4)

Use aider’s new experimental browser UI to collaborate with LLMs
to edit code in your local git repo.
Aider will directly edit the code in your local source files,
and [git commit the changes](https://aider.chat/docs/git.html)
with sensible commit messages.
You can start a new project or work with an existing git repo.
Aider works well with
GPT-4o, Sonnet 3.7, and DeepSeek Chat V3 & R1.
It also supports [connecting to almost any LLM](https://aider.chat/docs/llms.html).

Use the `--browser` switch to launch the browser version of aider:

```
python -m pip install -U aider-chat

export OPENAI_API_KEY=<key> # Mac/Linux
setx   OPENAI_API_KEY <key> # Windows, restart shell after setx

aider --browser
```