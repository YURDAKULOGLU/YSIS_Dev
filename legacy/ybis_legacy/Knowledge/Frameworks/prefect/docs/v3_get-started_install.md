Install Prefect - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Get started

Install Prefect

[Getting Started](/v3/get-started)[Concepts](/v3/concepts)[How-to Guides](/v3/how-to-guides)[Advanced](/v3/advanced)[Examples](/v3/examples)[Integrations](/integrations/integrations)[API Reference](/v3/api-ref)[Contribute](/contribute)[Release Notes](/v3/release-notes)

##### Get started

* [Welcome](/v3/get-started)
* [Install Prefect](/v3/get-started/install)
* [Quickstart](/v3/get-started/quickstart)

On this page

* [Windows installation](#windows-installation)
* [Minimal Prefect installation](#minimal-prefect-installation)
* [Next steps](#next-steps)

Prefect is published as a Python package, which requires Python 3.10 or newer. We recommend installing Prefect in a Python virtual environment.
To install Prefect, run:

pip

uv

Copy

```
pip install -U prefect
```

To confirm that Prefect was installed successfully, run:

pip

uv

Copy

```
prefect version
```

You should see output similar to:

Copy

```
Version:              3.4.24
API version:          0.8.4
Python version:       3.12.8
Git commit:           2428894e
Built:                Mon, Oct 13, 2025 07:16 PM
OS/Arch:              darwin/arm64
Profile:              local
Server type:          server
Pydantic version:     2.11.7
Server:
  Database:           sqlite
  SQLite version:     3.47.1
```

More commands for power users

### [​](#if-you-use-uv) If you use `uv`

start an `ipython` shell with python 3.12 and `prefect` installed:

Copy

```
uvx --python 3.12 --with prefect ipython
```

install prefect into a `uv` virtual environment:

Copy

```
uv venv --python 3.12
source .venv/bin/activate
uv add prefect
```

add prefect to a project:

Copy

```
uv add prefect
```

run prefect server in an ephemeral python environment with `uvx`:

Copy

```
uvx prefect server start
```

### [​](#if-you-use-docker) If you use `docker`

run prefect server in a container port-forwarded to your local machine’s 4200 port:

Copy

```
docker run -d -p 4200:4200 prefecthq/prefect:3-latest -- prefect server start --host 0.0.0.0
```

## [​](#windows-installation) Windows installation

You can install and run Prefect via Windows PowerShell, the Windows Command Prompt, or [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html). After installation, you may need to manually add the Python local packages `Scripts` folder to your `Path` environment variable.
The `Scripts` folder path looks something like:

Copy

```
C:\Users\MyUserNameHere\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts
```

Review the `pip install` output messages for the `Scripts` folder path on your system.

## [​](#minimal-prefect-installation) Minimal Prefect installation

The `prefect-client` library is a minimal installation of Prefect designed for interacting with Prefect Cloud or a remote self-hosted Prefect server instance.
`prefect-client` enables a subset of Prefect’s capabilities with a smaller installation size, making it ideal for use in lightweight, resource-constrained, or ephemeral environments.
It omits all CLI and server components found in the `prefect` library.
To install the latest release of `prefect-client`, run:

Copy

```
pip install -U prefect-client
```

## [​](#next-steps) Next steps

You also need an API server, either:

* [Prefect Cloud](/v3/how-to-guides/cloud/connect-to-cloud), a managed solution that provides strong scaling, performance, and security, or
* [Self-hosted Prefect server](/v3/concepts/server), an API server that you run on your own infrastructure where you are responsible for scaling and any authentication and authorization.

Now that you have Prefect installed, go through the [quickstart](/v3/get-started/quickstart) to try it out.
See the full history of [Prefect releases](https://github.com/PrefectHQ/prefect/releases) on GitHub.
See our [Contributing docs](/contribute/dev-contribute) for instructions on installing Prefect for development.

Was this page helpful?

YesNo

[Welcome](/v3/get-started)[Quickstart](/v3/get-started/quickstart)

⌘I