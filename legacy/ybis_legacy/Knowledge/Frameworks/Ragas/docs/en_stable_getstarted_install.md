Installation - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#installation)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# Installation

To get started, install Ragas using `pip` with the following command:

```
pip install ragas
```

If you'd like to experiment with the latest features, install the most recent version from the main branch:

```
pip install git+https://github.com/vibrantlabsai/ragas.git
```

If you're planning to contribute and make modifications to the code, ensure that you clone the repository and set it up as an [editable install](https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs).

```
git clone https://github.com/vibrantlabsai/ragas.git 
pip install -e .
```

LangChain OpenAI dependency versions

If you use `langchain_openai` (e.g., `ChatOpenAI`), install `langchain-core` and `langchain-openai` explicitly to avoid version mismatches. You can adjust bounds to match your environment, but installing both explicitly helps prevent strict dependency conflicts.

```
pip install -U "langchain-core>=0.2,<0.3" "langchain-openai>=0.1,<0.2" openai
```

November 28, 2025




November 28, 2025




GitHub

Back to top