Distributed XGBoost pipeline — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Distributed XGBoost pipeline[#](#distributed-xgboost-pipeline "Link to this heading")

[![](https://img.shields.io/badge/🚀 Run_on-Anyscale-9hf)](https://console.anyscale.com/) 
[![](https://img.shields.io/static/v1?label=&message=View%20On%20GitHub&color=586069&logo=github&labelColor=2f363d)](https://github.com/anyscale/e2e-xgboost)

![](https://raw.githubusercontent.com/anyscale/e2e-xgboost/refs/heads/main/images/overview.png)

These tutorials implement an end-to-end XGBoost application including:

* **Distributed data preprocessing and model training**: Ingest and preprocess data at scale using [Ray Data](https://docs.ray.io/en/latest/data/data.html). Then, train a distributed [XGBoost model](https://xgboost.readthedocs.io/en/stable/python/index.html) using [Ray Train](https://docs.ray.io/en/latest/train/train.html). See [Distributed training of an XGBoost model](notebooks/01-Distributed_Training.html).
* **Model validation using offline inference**: Evaluate the model using Ray Data offline batch inference. See [Model validation using offline batch inference](notebooks/02-Validation.html).
* **Online model serving**: Deploy the model as a scalable online service using [Ray Serve](https://docs.ray.io/en/latest/serve/index.html). See [Scalable online XGBoost inference with Ray Serve](notebooks/03-Serving.html).
* **Production deployment**: Create production batch [**Jobs**](https://docs.anyscale.com/platform/jobs/) for offline workloads including data prep, training, batch prediction, and potentially online [**Services**](https://docs.anyscale.com/platform/services/).

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/ray-overview/examples/e2e-xgboost/README.ipynb)