Distributed RAG pipeline — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Distributed RAG pipeline[#](#distributed-rag-pipeline "Link to this heading")

This tutorial covers end-to-end Retrieval-Augmented Generation (RAG) pipelines using [Ray](https://docs.ray.io/), from data ingestion and LLM deployment to prompt engineering, evaluation and scaling out all workloads in the application.

![](https://images.ctfassets.net/xjan103pcp94/4PX0l1ruKqfH17YvUiMFPw/c60a7a665125cb8056bebcc146c23b76/image8.png)

## Notebooks[#](#notebooks "Link to this heading")

1. [01\_(Optional)\_Regular\_Document\_Processing\_Pipeline.ipynb](https://github.com/ray-project/ray/blob/master/doc/source/ray-overview/examples/e2e-rag/notebooks/01_(Optional)_Regular_Document_Processing_Pipeline.ipynb)  
   Demonstrates a baseline document processing workflow for extracting, cleaning, and indexing text prior to RAG.
2. [02\_Scalable\_RAG\_Data\_Ingestion\_with\_Ray\_Data.ipynb](https://github.com/ray-project/ray/blob/master/doc/source/ray-overview/examples/e2e-rag/notebooks/02_Scalable_RAG_Data_Ingestion_with_Ray_Data.ipynb)  
   Shows how to build a high-throughput data ingestion pipeline for RAG using Ray Data.
3. [03\_Deploy\_LLM\_with\_Ray\_Serve.ipynb](https://github.com/ray-project/ray/blob/master/doc/source/ray-overview/examples/e2e-rag/notebooks/03_Deploy_LLM_with_Ray_Serve.ipynb)  
   Guides you through containerizing and serving a large language model at scale with Ray Serve.
4. [04\_Build\_Basic\_RAG\_Chatbot](https://github.com/ray-project/ray/blob/master/doc/source/ray-overview/examples/e2e-rag/notebooks/04_Build_Basic_RAG_Chatbot.ipynb)  
   Combines your indexed documents and served LLM to create a simple, interactive RAG chatbot.
5. [05\_Improve\_RAG\_with\_Prompt\_Engineering](https://github.com/ray-project/ray/blob/master/doc/source/ray-overview/examples/e2e-rag/notebooks/05_Improve_RAG_with_Prompt_Engineering.ipynb)  
   Explores prompt-engineering techniques to boost relevance and accuracy in RAG responses.
6. [06\_(Optional)\_Evaluate\_RAG\_with\_Online\_Inference](https://github.com/ray-project/ray/blob/master/doc/source/ray-overview/examples/e2e-rag/notebooks/06_(Optional)_Evaluate_RAG_with_Online_Inference.ipynb)  
   Provides methods to assess RAG quality in real time through live queries and metrics tracking.
7. [07\_Evaluate\_RAG\_with\_Ray\_Data\_LLM\_Batch\_inference](https://github.com/ray-project/ray/blob/master/doc/source/ray-overview/examples/e2e-rag/notebooks/07_Evaluate_RAG_with_Ray_Data_LLM_Batch_inference.ipynb)  
   Implements large-scale batch evaluation of RAG outputs using Ray Data + LLM batch inference.

---

> **Note:** Notebooks marked “(Optional)” cover complementary topics and can be skipped if you prefer to focus on the core RAG flow.

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/ray-overview/examples/e2e-rag/README.ipynb)