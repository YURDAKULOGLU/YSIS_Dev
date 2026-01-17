# Model warnings

## Unknown context window size and token costs

```
Model foobar: Unknown context window size and costs, using sane defaults.
```

If you specify a model that aider has never heard of, you will get
this warning.
This means aider doesn’t know the context window size and token costs
for that model.
Aider will use an unlimited context window and assume the model is free,
so this is not usually a significant problem.

See the docs on
[configuring advanced model settings](/docs/config/adv-model-settings.html)
for details on how to remove this warning.

You can probably ignore the unknown context window size and token costs warning.

## Did you mean?

If aider isn’t familiar with the model you’ve specified,
it will suggest similarly named models.
This helps
in the case where you made a typo or mistake when specifying the model name.

```
Model gpt-5o: Unknown context window size and costs, using sane defaults.
Did you mean one of these?
- gpt-4o
```

## Missing environment variables

You need to set the listed environment variables.
Otherwise you will get error messages when you start chatting with the model.

```
Model azure/gpt-4-turbo: Missing these environment variables:
- AZURE_API_BASE
- AZURE_API_VERSION
- AZURE_API_KEY
```

On Windows,
if you just set these environment variables using `setx` you may need to restart your terminal or
command prompt for the changes to take effect.

## Unknown which environment variables are required

```
Model gpt-5: Unknown which environment variables are required.
```

Aider is unable verify the environment because it doesn’t know
which variables are required for the model.
If required variables are missing,
you may get errors when you attempt to chat with the model.
You can look in the [aider’s LLM documentation](/docs/llms.html)
or the
[litellm documentation](https://docs.litellm.ai/docs/providers)
to see if the required variables are listed there.

## More help

If you need more help, please check our
[GitHub issues](https://github.com/Aider-AI/aider/issues)
and file a new issue if your problem isn’t discussed.
Or drop into our
[Discord](https://discord.gg/Y7X7bhMQFV)
to chat with us.

When reporting problems, it is very helpful if you can provide:

* Aider version
* LLM model you are using

Including the “announcement” lines that
aider prints at startup
is an easy way to share this helpful info.

```
Aider v0.37.1-dev
Models: gpt-4o with diff edit format, weak model gpt-3.5-turbo
Git repo: .git with 243 files
Repo-map: using 1024 tokens
```

Use `/help <question>` to
[ask for help about using aider](/docs/troubleshooting/support.html),
customizing settings, troubleshooting, using LLMs, etc.