Persona Generation - Ragas







![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#personas-in-testset-generation)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# Persona Generation

## Persona's in Testset Generation

You can add different persona's to the testset generation process by defining the [Persona][ragas.testset.persona.Persona] class with the name and role description of the different persona's that might be relevant to your use case, and you want to generate testset for.

For example, for the [GitLab handbook](https://about.gitlab.com/handbook/) we might want to generate testset for different persona's like a new joinee, a manager, a senior manager, etc. And hence we will define them as follows:

1. New Joinee: Don't know much about the company and is looking for information on how to get started.
2. Manager: Wants to know about the different teams and how they collaborate with each other.
3. Senior Manager: Wants to know about the company vision and how it is executed.

Which we can define as follows:

```
from ragas.testset.persona import Persona

persona_new_joinee = Persona(
    name="New Joinee",
    role_description="Don't know much about the company and is looking for information on how to get started.",
)
persona_manager = Persona(
    name="Manager",
    role_description="Wants to know about the different teams and how they collaborate with each other.",
)
persona_senior_manager = Persona(
    name="Senior Manager",
    role_description="Wants to know about the company vision and how it is executed.",
)

personas = [persona_new_joinee, persona_manager, persona_senior_manager]
personas
```

```
[Persona(name='New Joinee', role_description="Don't know much about the company and is looking for information on how to get started."),
 Persona(name='Manager', role_description='Wants to know about the different teams and how they collaborate with each other.'),
 Persona(name='Senior Manager', role_description='Wants to know about the company vision and how it is executed.')]
```

And then you can use these personas in the testset generation process by passing them to the [TestsetGenerator][ragas.testset.generator.TestsetGenerator] class.

```
from openai import OpenAI
from ragas.testset import TestsetGenerator
from ragas.testset.graph import KnowledgeGraph
from ragas.llms import llm_factory

# Load the knowledge graph
kg = KnowledgeGraph.load("../../../../experiments/gitlab_kg.json")
# Initialize the Generator LLM
openai_client = OpenAI()
llm = llm_factory("gpt-4o-mini", client=openai_client)

# Initialize the Testset Generator
testset_generator = TestsetGenerator(knowledge_graph=kg, persona_list=personas, llm=llm)
# Generate the Testset
testset = testset_generator.generate(testset_size=10)
testset
```

```
testset.to_pandas().head()
```

|  | user\_input | reference\_contexts | reference | synthesizer\_name |
| --- | --- | --- | --- | --- |
| 0 | What the Director do in GitLab and how they wo... | [09db4f3e-1c10-4863-9024-f869af48d3e0\n\ntitle... | The Director at GitLab, such as the Director o... | single\_hop\_specifc\_query\_synthesizer |
| 1 | Wht is the rol of the VP in GitLab? | [56c84f1b-3558-4c80-b8a9-348e69a4801b\n\nJob F... | The VP, or Vice President, at GitLab is respon... | single\_hop\_specifc\_query\_synthesizer |
| 2 | What GitLab do for career progression? | [ead619a5-930f-4e2b-b797-41927a04d2e3\n\nGoals... | The Job frameworks at GitLab help team members... | single\_hop\_specifc\_query\_synthesizer |
| 3 | Wht is the S-grop and how do they work with ot... | [42babb12-b033-493f-b684-914e2b1b1d0f\n\nPeopl... | Members of the S-group are expected to demonst... | single\_hop\_specifc\_query\_synthesizer |
| 4 | How does Google execute its company vision? | [c3ed463d-1cdc-4ba4-a6ca-2c4ab12da883\n\nof mo... | To effectively execute the company vision, man... | single\_hop\_specifc\_query\_synthesizer |

## Automatic Persona Generation

If you want to automatically generate persona's from a knowledge graph, you can use the [generate\_personas\_from\_kg][ragas.testset.persona.generate\_personas\_from\_kg] function.

```
from ragas.testset.persona import generate_personas_from_kg
from ragas.testset.graph import KnowledgeGraph
from ragas.llms import llm_factory

kg = KnowledgeGraph.load("../../../../experiments/gitlab_kg.json")
llm = llm_factory("gpt-4o-mini")

personas = generate_personas_from_kg(kg=kg, llm=llm, num_personas=5)
```

```
personas
```

```
[Persona(name='Organizational Development Manager', role_description='Responsible for implementing job frameworks and career development strategies to enhance employee growth and clarify roles within the company.'),
 Persona(name='DevSecOps Product Manager', role_description='Responsible for overseeing the development and strategy of DevSecOps solutions, ensuring alignment with company goals and user needs.'),
 Persona(name='Product Pricing Analyst', role_description='Responsible for developing and analyzing pricing strategies that align with customer needs and market demands.'),
 Persona(name='Site Reliability Engineer', role_description='Responsible for maintaining service reliability and performance, focusing on implementing rate limits to prevent outages and enhance system stability.'),
 Persona(name='Security Operations Engineer', role_description="Works on enhancing security logging processes and ensuring compliance within GitLab's infrastructure.")]
```

November 28, 2025




November 28, 2025

Back to top