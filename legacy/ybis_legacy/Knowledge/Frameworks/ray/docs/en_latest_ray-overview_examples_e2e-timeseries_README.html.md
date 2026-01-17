Time-series forecasting — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Time-series forecasting[#](#time-series-forecasting "Link to this heading")

[![](https://img.shields.io/badge/🚀%20Run%20on-Anyscale-9hf)](https://console.anyscale.com/) 
[![](https://img.shields.io/static/v1?label=&message=View%20On%20GitHub&color=586069&logo=github&labelColor=2f363d)](https://github.com/anyscale/e2e-timeseries)

These tutorials implement an end-to-end time-series application including:

* **Distributed data preprocessing and model training**: Ingest and preprocess data at scale using [Ray Data](https://docs.ray.io/en/latest/data/data.html). Then, train a distributed [DLinear model](https://github.com/cure-lab/LTSF-Linear) using [Ray Train](https://docs.ray.io/en/latest/train/train.html).
* **Model validation using offline inference**: Evaluate the model using Ray Data offline batch inference.
* **Online model serving**: Deploy the model as a scalable online service using [Ray Serve](https://docs.ray.io/en/latest/serve/index.html).
* **Production deployment**: Create production batch Jobs for offline workloads including data prep, training, batch prediction, and potentially online Services.

## Setup[#](#setup "Link to this heading")

Run the following:

```
pip install -r requirements.txt && pip install -e .
```

## Acknowledgements[#](#acknowledgements "Link to this heading")

This repository is based on the official `DLinear` implementations:

* [`DLinear`](https://github.com/vivva/DLinear)
* [`LTSF-Linear`](https://github.com/cure-lab/LTSF-Linear)

And the original publication:

* [“Are Transformers Effective for Time Series Forecasting?”](https://arxiv.org/abs/2205.13504)

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/ray-overview/examples/e2e-timeseries/README.ipynb)