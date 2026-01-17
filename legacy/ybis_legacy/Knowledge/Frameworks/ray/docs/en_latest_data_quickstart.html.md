Ray Data Quickstart — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Ray Data Quickstart[#](#ray-data-quickstart "Link to this heading")

Get started with Ray Data’s [`Dataset`](api/dataset.html#ray.data.Dataset "ray.data.Dataset") abstraction for distributed data processing.

This guide introduces you to the core capabilities of Ray Data:

* [Loading data](#loading-key-concept)
* [Transforming data](#transforming-key-concept)
* [Consuming data](#consuming-key-concept)
* [Saving data](#saving-key-concept)

## Datasets[#](#datasets "Link to this heading")

Ray Data’s main abstraction is a [`Dataset`](api/dataset.html#ray.data.Dataset "ray.data.Dataset"), which
represents a distributed collection of data. Datasets are specifically designed for machine learning workloads
and can efficiently handle data collections that exceed a single machine’s memory.

## Loading data[#](#loading-data "Link to this heading")

Create datasets from various sources including local files, Python objects, and cloud storage services like S3 or GCS.
Ray Data seamlessly integrates with any [filesystem supported by Arrow](http://arrow.apache.org/docs/python/generated/pyarrow.fs.FileSystem.html).

```
import ray

# Load a CSV dataset directly from S3
ds = ray.data.read_csv("s3://anonymous@air-example-data/iris.csv")

# Preview the first record
ds.show(limit=1)
```

```
{'sepal length (cm)': 5.1, 'sepal width (cm)': 3.5, 'petal length (cm)': 1.4, 'petal width (cm)': 0.2, 'target': 0}
```

To learn more about creating datasets from different sources, read [Loading data](loading-data.html#loading-data).

## Transforming data[#](#transforming-data "Link to this heading")

Apply user-defined functions (UDFs) to transform datasets. Ray automatically parallelizes these transformations
across your cluster for better performance.

```
from typing import Dict
import numpy as np

# Define a transformation to compute a "petal area" attribute
def transform_batch(batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    vec_a = batch["petal length (cm)"]
    vec_b = batch["petal width (cm)"]
    batch["petal area (cm^2)"] = vec_a * vec_b
    return batch

# Apply the transformation to our dataset
transformed_ds = ds.map_batches(transform_batch)

# View the updated schema with the new column
# .materialize() will execute all the lazy transformations and
# materialize the dataset into object store memory
print(transformed_ds.materialize())
```

```
MaterializedDataset(
   num_blocks=...,
   num_rows=150,
   schema={
      sepal length (cm): double,
      sepal width (cm): double,
      petal length (cm): double,
      petal width (cm): double,
      target: int64,
      petal area (cm^2): double
   }
)
```

To explore more transformation capabilities, read [Transforming data](transforming-data.html#transforming-data).

## Consuming data[#](#consuming-data "Link to this heading")

Access dataset contents through convenient methods like [`take_batch()`](api/doc/ray.data.Dataset.take_batch.html#ray.data.Dataset.take_batch "ray.data.Dataset.take_batch") and
[`iter_batches()`](api/doc/ray.data.Dataset.iter_batches.html#ray.data.Dataset.iter_batches "ray.data.Dataset.iter_batches"). You can also pass datasets directly to Ray Tasks or Actors
for distributed processing.

```
# Extract the first 3 rows as a batch for processing
print(transformed_ds.take_batch(batch_size=3))
```

```
{'sepal length (cm)': array([5.1, 4.9, 4.7]),
    'sepal width (cm)': array([3.5, 3. , 3.2]),
    'petal length (cm)': array([1.4, 1.4, 1.3]),
    'petal width (cm)': array([0.2, 0.2, 0.2]),
    'target': array([0, 0, 0]),
    'petal area (cm^2)': array([0.28, 0.28, 0.26])}
```

For more details on working with dataset contents, see
[Iterating over Data](iterating-over-data.html#iterating-over-data) and [Saving Data](saving-data.html#saving-data).

## Saving data[#](#saving-data "Link to this heading")

Export processed datasets to a variety of formats and storage locations using methods
like [`write_parquet()`](api/doc/ray.data.Dataset.write_parquet.html#ray.data.Dataset.write_parquet "ray.data.Dataset.write_parquet"), [`write_csv()`](api/doc/ray.data.Dataset.write_csv.html#ray.data.Dataset.write_csv "ray.data.Dataset.write_csv"), and more.

```
import os

# Save the transformed dataset as Parquet files
transformed_ds.write_parquet("/tmp/iris")

# Verify the files were created
print(os.listdir("/tmp/iris"))
```

```
['..._000000.parquet', '..._000001.parquet']
```

For more information on saving datasets, see [Saving data](saving-data.html#saving-data).

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/data/quickstart.rst)