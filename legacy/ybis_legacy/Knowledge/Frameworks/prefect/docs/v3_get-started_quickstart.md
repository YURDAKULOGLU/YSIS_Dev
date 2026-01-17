Quickstart - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Get started

Quickstart

[Getting Started](/v3/get-started)[Concepts](/v3/concepts)[How-to Guides](/v3/how-to-guides)[Advanced](/v3/advanced)[Examples](/v3/examples)[Integrations](/integrations/integrations)[API Reference](/v3/api-ref)[Contribute](/contribute)[Release Notes](/v3/release-notes)

##### Get started

* [Welcome](/v3/get-started)
* [Install Prefect](/v3/get-started/install)
* [Quickstart](/v3/get-started/quickstart)

Prefect is a workflow orchestration tool that helps you build, deploy, run, and monitor data pipelines. It makes complex workflows reliable by tracking dependencies and handling failures gracefully.
In this tutorial, you’ll deploy your first workflow to Prefect — by specifying what code should run, where it should run, and when it should run. Choose your preferred approach below:

* Cloud
* Open Source

1

Create and login to your Prefect Cloud account.

Prefect uses a database to store workflow metadata.
For the ease of getting started, we’ll use one hosted on Prefect Cloud. To create an account, we need to install `prefect-cloud`. We’ll leverage `uv`, a modern Python package manager, to do this. Run the following commands in your terminal, after which you’ll be prompted in your browser to create or login to your free Prefect Cloud account.

Copy

```
curl -LsSf https://astral.sh/uv/install.sh | sh # Install `uv`.
uvx prefect-cloud login # Installs `prefect-cloud` into a temporary virtual env.
```

2

What code should run?

Let’s start with a boring Python script that fetches a list of customer ids and processes them all in parallel. You can find this code and other examples hosted in our [quickstart repository](https://github.com/PrefectHQ/quickstart/blob/main/01_getting_started.py).

01\_getting\_started.py

Copy

```
from prefect import flow, task
import random

@task
def get_customer_ids() -> list[str]:
    # Fetch customer IDs from a database or API
    return [f"customer{n}" for n in random.choices(range(100), k=10)]

@task
def process_customer(customer_id: str) -> str:
    # Process a single customer
    return f"Processed {customer_id}"

@flow
def main() -> list[str]:
    customer_ids = get_customer_ids()
    # Map the process_customer task across all customer IDs
    results = process_customer.map(customer_ids)
    return results


if __name__ == "__main__":
    main()
```

See all 23 lines

This looks like the ordinary Python you’d write, except there is:

* a `@flow` decorator on the script’s entrypoint.
* a `@task` decorator on each function called within the flow.

When you run this `flow`, Prefect dynamically creates a graph of each `task` and the state of their upstream dependencies. This allows Prefect to execute each `task` in the right order and, in the case of failure, to recover the state of your workflow and resume from its point of failure.Let’s run this code locally on your computer. To do that, run the following command in your terminal.

Copy

```
git clone https://github.com/PrefectHQ/quickstart && cd quickstart
uv run 01_getting_started.py
```

If all went well, you’ll see a link to see its execution graph in the Prefect UI followed by a flurry of state changes and logs as Prefect dynamically discovers and executes your workflow.

Copy

```
00:30:53.633 | INFO    | Flow run 'airborne-ringtail' - Beginning flow run 'airborne-ringtail' for flow 'main'
00:30:53.638 | INFO    | Flow run 'airborne-ringtail' - View at https://app.prefect.cloud/account/...
00:30:53.685 | INFO    | Task run 'get_customer_ids-136' - Finished in state Completed()
00:30:54.512 | INFO    | Task run 'process_customer-d9b' - Finished in state Completed()
00:30:54.518 | INFO    | Task run 'process_customer-113' - Finished in state Completed()
00:30:54.519 | INFO    | Task run 'process_customer-1c6' - Finished in state Completed()
00:30:54.519 | INFO    | Task run 'process_customer-30d' - Finished in state Completed()
00:30:54.520 | INFO    | Task run 'process_customer-eaa' - Finished in state Completed()
00:30:54.523 | INFO    | Task run 'process_customer-b2b' - Finished in state Completed()
00:30:54.523 | INFO    | Task run 'process_customer-90a' - Finished in state Completed()
00:30:54.524 | INFO    | Task run 'process_customer-4af' - Finished in state Completed()
00:30:54.524 | INFO    | Task run 'process_customer-e66' - Finished in state Completed()
00:30:54.526 | INFO    | Task run 'process_customer-e7e' - Finished in state Completed()
00:30:54.527 | INFO    | Flow run 'airborne-ringtail' - Finished in state Completed('All states completed.')
```

See all 14 lines

3

Where should it run?

At this point, you’ve successfully run a Prefect `flow` locally. Let’s get it running off of your machine! Again, for simplicity,
we’ll deploy this workflow to Prefect’s Serverless Compute (so we don’t have to wrangle any infrastructure). We’ll tell Prefect to clone
`https://github.com/PrefectHQ/quickstart` and invoke `01_getting_started.py:main`.

Copy

```
uvx prefect-cloud deploy 01_getting_started.py:main \
--name my_first_deployment \
--from https://github.com/PrefectHQ/quickstart
```

If all went well, you’ve created your first deployed workflow.Since we now know what code to run and where to run it, this can now be invoked remotely.
To do that, run the following command and visit the returned link to see the run’s status in the Prefect UI:

Copy

```
uvx prefect-cloud run main/my_first_deployment
```

Congrats! You’ve just run your first Prefect workflow remotely.

4

When should it run?

Now that you’ve deployed and run your workflow remotely, you might want to schedule it to run automatically at specific times. Prefect makes this easy with the `prefect-cloud schedule` command.Let’s schedule our workflow to run every day at 8:00 AM with [`cron`](https://en.wikipedia.org/wiki/Cron) syntax.

Copy

```
uvx prefect-cloud schedule main/my_first_deployment "0 8 * * *"
```

After running the command, your workflow will automatically execute remotely according to the schedule you’ve set.You can view and manage all your scheduled runs in the Prefect UI.

1

Install Prefect and start the server

If you’re using Prefect Open Source, you’ll run a server that backs your workflows. [Install Prefect](/v3/get-started/install) and start your local server:

Copy

```
prefect server start
```

If you prefer to run your Prefect server in a Docker container, you can use the following command:

Copy

```
docker run -p 4200:4200 -d --rm prefecthq/prefect:3-python3.12 prefect server start --host 0.0.0.0
```

Both commands start a server at [`http://localhost:4200`](http://localhost:4200). Keep this process running for this tutorial.

2

What code should run?

Let’s start with a boring Python script that fetches a list of customer ids and processes them all in parallel. You can find this code and other examples hosted in our [quickstart repository](https://github.com/PrefectHQ/quickstart/blob/main/01_getting_started.py).

01\_getting\_started.py

Copy

```
from prefect import flow, task
import random

@task
def get_customer_ids() -> list[str]:
    # Fetch customer IDs from a database or API
    return [f"customer{n}" for n in random.choices(range(100), k=10)]

@task
def process_customer(customer_id: str) -> str:
    # Process a single customer
    return f"Processed {customer_id}"

@flow
def main() -> list[str]:
    customer_ids = get_customer_ids()
    # Map the process_customer task across all customer IDs
    results = process_customer.map(customer_ids)
    return results


if __name__ == "__main__":
    main()
```

See all 23 lines

This looks like the ordinary Python you’d write, except there is:

* a `@flow` decorator on the script’s entrypoint.
* a `@task` decorator on each function called within the flow.

When you run this `flow`, Prefect dynamically creates a graph of each `task` and the state of their upstream dependencies. This allows Prefect to execute each `task` in the right order and, in the case of failure, to recover the state of your workflow and resume from its point of failure.Let’s run this code locally on your computer. To do that, run the following command in your terminal (in a new terminal window, keeping the server running):

Copy

```
git clone https://github.com/PrefectHQ/quickstart && cd quickstart
python 01_getting_started.py
```

If all went well, you’ll see a link to see its execution graph in the Prefect UI followed by a flurry of state changes and logs as Prefect dynamically discovers and executes your workflow.

3

Where should it run?

At this point, you’ve successfully run a Prefect `flow` locally. Let’s set up a simple deployment by updating the file to use `.serve()`:

01\_getting\_started.py

Copy

```
from prefect import flow, task
import random

@task
def get_customer_ids() -> list[str]:
    # Fetch customer IDs from a database or API
    return [f"customer{n}" for n in random.choices(range(100), k=10)]

@task
def process_customer(customer_id: str) -> str:
    # Process a single customer
    return f"Processed {customer_id}"

@flow
def main() -> list[str]:
    customer_ids = get_customer_ids()
    # Map the process_customer task across all customer IDs
    results = process_customer.map(customer_ids)
    return results


if __name__ == "__main__":
    main.serve(name="my-first-deployment")
```

See all 23 lines

Now run the updated file:

Copy

```
python 01_getting_started.py
```

This starts a process listening for scheduled runs. You can now trigger the flow from the Prefect UI or programmatically.

4

When should it run?

Now let’s schedule your workflow to run automatically. Update the file to add a cron schedule:

01\_getting\_started.py

Copy

```
from prefect import flow, task
import random

@task
def get_customer_ids() -> list[str]:
    # Fetch customer IDs from a database or API
    return [f"customer{n}" for n in random.choices(range(100), k=10)]

@task
def process_customer(customer_id: str) -> str:
    # Process a single customer
    return f"Processed {customer_id}"

@flow
def main() -> list[str]:
    customer_ids = get_customer_ids()
    # Map the process_customer task across all customer IDs
    results = process_customer.map(customer_ids)
    return results


if __name__ == "__main__":
    main.serve(
        name="my-first-deployment",
        cron="0 8 * * *"  # Run every day at 8:00 AM
    )
```

See all 26 lines

Run the updated file:

Copy

```
python 01_getting_started.py
```

Your workflow will now run automatically according to the schedule while the serve process is running.

## [​](#next-steps) Next steps

Now that you’ve created your first workflow, explore Prefect’s features to enable more sophisticated workflows.

* Learn more about [flows](/v3/concepts/flows) and [tasks](/v3/concepts/tasks).
* Learn more about [deployments](/v3/concepts/deployments).
* Learn more about [work pools](/v3/concepts/work-pools).
* Learn how to [run work concurrently](/v3/how-to-guides/workflows/run-work-concurrently).

Was this page helpful?

YesNo

[Install Prefect](/v3/get-started/install)

⌘I