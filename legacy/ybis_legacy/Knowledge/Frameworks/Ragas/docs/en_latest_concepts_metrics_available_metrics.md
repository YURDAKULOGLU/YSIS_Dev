List of available metrics - Ragas








![](https://static.scarf.sh/a.png?x-pxid=f4040c26-97ff-4975-bcbb-8db47063d472)
















[Skip to content](#list-of-available-metrics)

**Ragas Office Hours** - If you need help setting up Evals for your AI application, sign up for our
Office Hours [here](https://cal.com/team/vibrantlabs/office-hours).

# List of available metrics

Ragas provides a set of evaluation metrics that can be used to measure the performance of your LLM application. These metrics are designed to help you objectively measure the performance of your application. Metrics are available for different applications and tasks, such as RAG and Agentic workflows.

Each metric are essentially paradigms that are designed to evaluate a particular aspect of the application. LLM Based metrics might use one or more LLM calls to arrive at the score or result. One can also modify or write your own metrics using ragas.

## Retrieval Augmented Generation

* [Context Precision](context_precision/)
* [Context Recall](context_recall/)
* [Context Entities Recall](context_entities_recall/)
* [Noise Sensitivity](noise_sensitivity/)
* [Response Relevancy](answer_relevance/)
* [Faithfulness](faithfulness/)
* [Multimodal Faithfulness](multi_modal_faithfulness/)
* [Multimodal Relevance](multi_modal_relevance/)

## Nvidia Metrics

* [Answer Accuracy](nvidia_metrics/#answer-accuracy)
* [Context Relevance](nvidia_metrics/#context-relevance)
* [Response Groundedness](nvidia_metrics/#response-groundedness)

## Agents or Tool use cases

* [Topic adherence](agents/#topic-adherence)
* [Tool call Accuracy](agents/#tool-call-accuracy)
* [Tool Call F1](agents/#tool-call-f1)
* [Agent Goal Accuracy](agents/#agent-goal-accuracy)

## Natural Language Comparison

* [Factual Correctness](factual_correctness/)
* [Semantic Similarity](semantic_similarity/)
* [Non LLM String Similarity](traditional/#non-llm-string-similarity)
* [BLEU Score](traditional/#bleu-score)
* [CHRF Score](traditional/#chrf-score)
* [ROUGE Score](traditional/#rouge-score)
* [String Presence](traditional/#string-presence)
* [Exact Match](traditional/#exact-match)

## SQL

* [Execution based Datacompy Score](sql/#execution-based-metrics)
* [SQL query Equivalence](sql/#sql-query-semantic-equivalence)

## General purpose

* [Aspect critic](general_purpose/#aspect-critic)
* [Simple Criteria Scoring](general_purpose/#simple-criteria-scoring)
* [Rubrics based scoring](general_purpose/#rubrics-based-scoring)
* [Instance specific rubrics scoring](general_purpose/#instance-specific-rubrics-scoring)

## Other tasks

* [Summarization](summarization_score/)

December 4, 2025




December 4, 2025




GitHub

Back to top