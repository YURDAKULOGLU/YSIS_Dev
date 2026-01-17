Installing Ray — Ray 2.53.0


[Skip to main content](#main-content)

Back to top





`Ctrl`+`K`

Try Ray with $100 credit — [Start now](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=banner)×

[Try Managed Ray](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=navbar)

# Installing Ray[#](#installing-ray "Link to this heading")

[![Run Quickstart on Anyscale](../_static/img/run-on-anyscale.svg)](https://console.anyscale.com/register/ha?render_flow=ray&utm_source=ray_docs&utm_medium=docs&utm_campaign=installing_ray&redirectTo=/v2/template-preview/workspace-intro)

Ray currently officially supports x86\_64, aarch64 (ARM) for Linux, and Apple silicon (M1) hardware.
Ray on Windows is currently in beta.

## Official Releases[#](#official-releases "Link to this heading")

### From Wheels[#](#from-wheels "Link to this heading")

You can install the latest official version of Ray from PyPI on Linux, Windows,
and macOS by choosing the option that best matches your use case.

Recommended

**For machine learning applications**

```
pip install -U "ray[data,train,tune,serve]"

# For reinforcement learning support, install RLlib instead.
# pip install -U "ray[rllib]"
```

**For general Python applications**

```
pip install -U "ray[default]"

# If you don't want Ray Dashboard or Cluster Launcher, install Ray with minimal dependencies instead.
# pip install -U "ray"
```


Advanced

| Command | Installed components |
| --- | --- |
| `pip install -U "ray"` | Core |
| `pip install -U "ray[default]"` | Core, Dashboard, Cluster Launcher |
| `pip install -U "ray[data]"` | Core, Data |
| `pip install -U "ray[train]"` | Core, Train |
| `pip install -U "ray[tune]"` | Core, Tune |
| `pip install -U "ray[serve]"` | Core, Dashboard, Cluster Launcher, Serve |
| `pip install -U "ray[serve-grpc]"` | Core, Dashboard, Cluster Launcher, Serve with gRPC support |
| `pip install -U "ray[rllib]"` | Core, Tune, RLlib |
| `pip install -U "ray[all]"` | Core, Dashboard, Cluster Launcher, Data, Train, Tune, Serve, RLlib. This option isn’t recommended. Specify the extras you need as shown below instead. |

Tip

You can combine installation extras.
For example, to install Ray with Dashboard, Cluster Launcher, and Train support, you can run:

```
pip install -U "ray[default,train]"
```

## Daily Releases (Nightlies)[#](#daily-releases-nightlies "Link to this heading")

You can install the nightly Ray wheels via the following links. These daily releases are tested via automated tests but do not go through the full release process. To install these wheels, use the following `pip` command and wheels:

```
# Clean removal of previous install
pip uninstall -y ray
# Install Ray with support for the dashboard + cluster launcher
pip install -U "ray[default] @ LINK_TO_WHEEL.whl"

# Install Ray with minimal dependencies
# pip install -U LINK_TO_WHEEL.whl
```

Linux

| Linux (x86\_64) | Linux (arm64/aarch64) |
| --- | --- |
| [Linux Python 3.10 (x86\_64)](https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-3.0.0.dev0-cp310-cp310-manylinux2014_x86_64.whl) | [Linux Python 3.10 (aarch64)](https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-3.0.0.dev0-cp310-cp310-manylinux2014_aarch64.whl) |
| [Linux Python 3.11 (x86\_64)](https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-3.0.0.dev0-cp311-cp311-manylinux2014_x86_64.whl) | [Linux Python 3.11 (aarch64)](https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-3.0.0.dev0-cp311-cp311-manylinux2014_aarch64.whl) |
| [Linux Python 3.12 (x86\_64)](https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-3.0.0.dev0-cp312-cp312-manylinux2014_x86_64.whl) | [Linux Python 3.12 (aarch64)](https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-3.0.0.dev0-cp312-cp312-manylinux2014_aarch64.whl) |
| [Linux Python 3.13 (x86\_64)](https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-3.0.0.dev0-cp313-cp313-manylinux2014_x86_64.whl) (beta) | [Linux Python 3.13 (aarch64)](https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-3.0.0.dev0-cp313-cp313-manylinux2014_aarch64.whl) (beta) |


MacOS

| MacOS (arm64) |
| --- |
| [MacOS Python 3.10 (arm64)](https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-3.0.0.dev0-cp310-cp310-macosx_12_0_arm64.whl) |
| [MacOS Python 3.11 (arm64)](https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-3.0.0.dev0-cp311-cp311-macosx_12_0_arm64.whl) |
| [MacOS Python 3.12 (arm64)](https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-3.0.0.dev0-cp312-cp312-macosx_12_0_arm64.whl) |
| [MacOS Python 3.13 (arm64)](https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-3.0.0.dev0-cp313-cp313-macosx_12_0_arm64.whl) (beta) |


Windows (beta)

| Windows (beta) |
| --- |
| [Windows Python 3.10 (amd64)](https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-3.0.0.dev0-cp310-cp310-win_amd64.whl) |
| [Windows Python 3.11 (amd64)](https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-3.0.0.dev0-cp311-cp311-win_amd64.whl) |
| [Windows Python 3.12 (amd64)](https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-3.0.0.dev0-cp312-cp312-win_amd64.whl) |

Note

On Windows, support for multi-node Ray clusters is currently experimental and untested.
If you run into issues please file a report at [ray-project/ray#issues](https://github.com/ray-project/ray/issues).

Note

[Usage stats](../cluster/usage-stats.html#ref-usage-stats) collection is enabled by default (can be [disabled](../cluster/usage-stats.html#usage-disable)) for nightly wheels including both local clusters started via `ray.init()` and remote clusters via cli.

## Installing from a specific commit[#](#installing-from-a-specific-commit "Link to this heading")

You can install the Ray wheels of any particular commit on `master` with the following template. You need to specify the commit hash, Ray version, Operating System, and Python version:

```
pip install https://s3-us-west-2.amazonaws.com/ray-wheels/master/{COMMIT_HASH}/ray-{RAY_VERSION}-{PYTHON_VERSION}-{PYTHON_VERSION}-{OS_VERSION}.whl
```

For example, here are the Ray 3.0.0.dev0 wheels for Python 3.10, MacOS for commit `4f2ec46c3adb6ba9f412f09a9732f436c4a5d0c9`:

```
pip install https://s3-us-west-2.amazonaws.com/ray-wheels/master/4f2ec46c3adb6ba9f412f09a9732f436c4a5d0c9/ray-3.0.0.dev0-cp310-cp310-macosx_12_0_arm64.whl
```

There are minor variations to the format of the wheel filename; it’s best to match against the format in the URLs listed in the [Nightlies section](#install-nightlies).
Here’s a summary of the variations:

* For MacOS x86\_64, commits predating August 7, 2021 will have `macosx_10_13` in the filename instead of `macosx_10_15`.
* For MacOS x86\_64, commits predating June 1, 2025 will have `macosx_10_15` in the filename instead of `macosx_12_0`.

## M1 Mac (Apple Silicon) Support[#](#m1-mac-apple-silicon-support "Link to this heading")

Ray supports machines running Apple Silicon (such as M1 macs).
Multi-node clusters are untested. To get started with local Ray development:

1. Install [miniforge](https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh).

   * `wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh`
   * `bash Miniforge3-MacOSX-arm64.sh`
   * `rm Miniforge3-MacOSX-arm64.sh # Cleanup.`
2. Ensure you’re using the miniforge environment (you should see (base) in your terminal).

   * `source ~/.bash_profile`
   * `conda activate`
3. Install Ray as you normally would.

   * `pip install ray`

## Windows Support[#](#windows-support "Link to this heading")

Windows support is in Beta. Ray supports running on Windows with the following caveats (only the first is
Ray-specific, the rest are true anywhere Windows is used):

* Multi-node Ray clusters are untested.
* Filenames are tricky on Windows and there still may be a few places where Ray
  assumes UNIX filenames rather than Windows ones. This can be true in downstream
  packages as well.
* Performance on Windows is known to be slower since opening files on Windows
  is considerably slower than on other operating systems. This can affect logging.
* Windows does not have a copy-on-write forking model, so spinning up new
  processes can require more memory.

Submit any issues you encounter to
[GitHub](https://github.com/ray-project/ray/issues/).

## Installing Ray on Arch Linux[#](#installing-ray-on-arch-linux "Link to this heading")

Note: Installing Ray on Arch Linux is not tested by the Project Ray developers.

Ray is available on Arch Linux via the Arch User Repository ([AUR](https://wiki.archlinux.org/index.php/Arch_User_Repository)) as
`python-ray`.

You can manually install the package by following the instructions on the
[Arch Wiki](https://wiki.archlinux.org/index.php/Arch_User_Repository#Installing_packages) or use an [AUR helper](https://wiki.archlinux.org/index.php/Arch_User_Repository#Installing_packages) like [yay](https://aur.archlinux.org/packages/yay) (recommended for ease of install)
as follows:

```
yay -S python-ray
```

To discuss any issues related to this package refer to the comments section
on the AUR page of `python-ray` [here](https://aur.archlinux.org/packages/python-ray).

## Installing From conda-forge[#](#installing-from-conda-forge "Link to this heading")

Ray can also be installed as a conda package on Linux and Windows.

```
# also works with mamba
conda create -c conda-forge python=3.10 -n ray
conda activate ray

# Install Ray with support for the dashboard + cluster launcher
conda install -c conda-forge "ray-default"

# Install Ray with minimal dependencies
# conda install -c conda-forge ray
```

To install Ray libraries, use `pip` as above or `conda`/`mamba`.

```
conda install -c conda-forge "ray-data"   # installs Ray + dependencies for Ray Data
conda install -c conda-forge "ray-train"  # installs Ray + dependencies for Ray Train
conda install -c conda-forge "ray-tune"   # installs Ray + dependencies for Ray Tune
conda install -c conda-forge "ray-serve"  # installs Ray + dependencies for Ray Serve
conda install -c conda-forge "ray-rllib"  # installs Ray + dependencies for Ray RLlib
```

For a complete list of available `ray` libraries on Conda-forge, have a look
at <https://anaconda.org/conda-forge/ray-default>

Note

Ray conda packages are maintained by the community, not the Ray team. While
using a conda environment, it is recommended to install Ray from PyPi using
`pip install ray` in the newly created environment.

## Building Ray from Source[#](#building-ray-from-source "Link to this heading")

Installing from `pip` should be sufficient for most Ray users.

However, should you need to build from source, follow [these instructions for building](../ray-contribute/development.html#building-ray) Ray.

## Docker Source Images[#](#docker-source-images "Link to this heading")

Users can pull a Docker image from the `rayproject/ray` [Docker Hub repository](https://hub.docker.com/r/rayproject/ray).
The images include Ray and all required dependencies. It comes with anaconda and various versions of Python.

Images are `tagged` with the format `{Ray version}[-{Python version}][-{Platform}]`. `Ray version` tag can be one of the following:

| Ray version tag | Description |
| --- | --- |
| latest | The most recent Ray release. |
| x.y.z | A specific Ray release, e.g. 2.31.0 |
| nightly | The most recent Ray development build (a recent commit from Github `master`) |

The optional `Python version` tag specifies the Python version in the image. All Python versions supported by Ray are available, e.g. `py310`, `py311` and `py312`. If unspecified, the tag points to an image of the lowest Python version that the Ray version supports.

The optional `Platform` tag specifies the platform where the image is intended for:

| Platform tag | Description |
| --- | --- |
| -cpu | These are based off of an Ubuntu image. |
| -cuXX | These are based off of an NVIDIA CUDA image with the specified CUDA version. They require the NVIDIA Docker Runtime. |
| -gpu | Aliases to a specific `-cuXX` tagged image. |
| <no tag> | Aliases to `-cpu` tagged images. |

Example: for the nightly image based on `Python 3.10` and without GPU support, the tag is `nightly-py310-cpu`.

If you want to tweak some aspects of these images and build them locally, refer to the following script:

```
cd ray
./build-docker.sh
```

Review images by listing them:

```
docker images
```

Output should look something like the following:

```
REPOSITORY                          TAG                 IMAGE ID            CREATED             SIZE
rayproject/ray                      dev                 7243a11ac068        2 days ago          1.11 GB
rayproject/base-deps                latest              5606591eeab9        8 days ago          512  MB
ubuntu                              22.04               1e4467b07108        3 weeks ago         73.9 MB
```

### Launch Ray in Docker[#](#launch-ray-in-docker "Link to this heading")

Start out by launching the deployment container.

```
docker run --shm-size=<shm-size> -t -i rayproject/ray
```

Replace `<shm-size>` with a limit appropriate for your system, for example
`512M` or `2G`. A good estimate for this is to use roughly 30% of your available memory (this is
what Ray uses internally for its Object Store). The `-t` and `-i` options here are required to support
interactive use of the container.

If you use a GPU version Docker image, remember to add `--gpus all` option. Replace `<ray-version>` with your target ray version in the following command:

```
docker run --shm-size=<shm-size> -t -i --gpus all rayproject/ray:<ray-version>-gpu
```

**Note:** Ray requires a **large** amount of shared memory because each object
store keeps all of its objects in shared memory, so the amount of shared memory
will limit the size of the object store.

You should now see a prompt that looks something like:

```
root@ebc78f68d100:/ray#
```

### Test if the installation succeeded[#](#test-if-the-installation-succeeded "Link to this heading")

To test if the installation was successful, try running some tests. This assumes
that you’ve cloned the git repository.

```
python -m pytest -v python/ray/tests/test_mini.py
```

### Installed Python dependencies[#](#installed-python-dependencies "Link to this heading")

Our docker images are shipped with pre-installed Python dependencies
required for Ray and its libraries.

We publish the dependencies that are installed in our `ray` Docker images for Python 3.9.

ray (Python 3.10)

Ray version: 2.53.0 ([0de2118](https://github.com/ray-project/ray/commit/0de211850589aea71f842873bc32574c702ab492))

```
adlfs==2023.8.0
aiohappyeyeballs==2.6.1
aiohttp==3.11.16
aiohttp-cors==0.7.0
aiosignal==1.3.1
amqp==5.3.1
annotated-doc==0.0.4
annotated-types==0.6.0
anyio==3.7.1
archspec @ file:///home/conda/feedstock_root/build_artifacts/archspec_1737352602016/work
async-timeout==4.0.3
attrs==25.1.0
azure-common==1.1.28
azure-core==1.29.5
azure-datalake-store==0.0.53
azure-identity==1.17.1
azure-storage-blob==12.22.0
billiard==4.2.1
boltons @ file:///home/conda/feedstock_root/build_artifacts/boltons_1733827268945/work
boto3==1.29.7
botocore==1.32.7
Brotli @ file:///home/conda/feedstock_root/build_artifacts/brotli-split_1764016952863/work
cachetools==5.5.2
celery==5.5.3
certifi==2025.1.31
cffi @ file:///home/conda/feedstock_root/build_artifacts/cffi_1725560520483/work
charset-normalizer==3.3.2
click==8.1.7
click-didyoumean==0.3.1
click-plugins==1.1.1.2
click-repl==0.3.0
cloudpickle==2.2.0
colorama @ file:///home/conda/feedstock_root/build_artifacts/colorama_1733218098505/work
colorful==0.5.5
conda @ file:///home/conda/feedstock_root/build_artifacts/conda_1765816446718/work/conda-src
conda-libmamba-solver @ file:///home/conda/feedstock_root/build_artifacts/conda-libmamba-solver_1764081326783/work/src
conda-package-handling @ file:///home/conda/feedstock_root/build_artifacts/conda-package-handling_1736345463896/work
conda_package_streaming @ file:///home/conda/feedstock_root/build_artifacts/conda-package-streaming_1729004031731/work
cryptography==44.0.3
cupy-cuda12x==13.4.0
Cython==0.29.37
distlib==0.3.7
distro @ file:///home/conda/feedstock_root/build_artifacts/distro_1734729835256/work
dm-tree==0.1.8
exceptiongroup==1.3.1
Farama-Notifications==0.0.4
fastapi==0.121.0
fastrlock==0.8.3
filelock==3.17.0
flatbuffers==23.5.26
frozendict @ file:///home/conda/feedstock_root/build_artifacts/frozendict_1763082794572/work
frozenlist==1.4.1
fsspec==2023.12.1
google-api-core==2.24.2
google-api-python-client==2.111.0
google-auth==2.23.4
google-auth-httplib2==0.1.1
google-cloud-core==2.4.1
google-cloud-storage==2.14.0
google-crc32c==1.5.0
google-oauth==1.0.1
google-resumable-media==2.6.0
googleapis-common-protos==1.61.0
grpcio==1.74.0
gymnasium==1.1.1
h11==0.16.0
h2 @ file:///home/conda/feedstock_root/build_artifacts/h2_1733298745555/work
hpack @ file:///home/conda/feedstock_root/build_artifacts/hpack_1733299205993/work
httplib2==0.20.4
httptools==0.7.1
hyperframe @ file:///home/conda/feedstock_root/build_artifacts/hyperframe_1733298771451/work
idna==3.7
importlib-metadata==6.11.0
isodate==0.6.1
Jinja2==3.1.6
jmespath==1.0.1
jsonpatch @ file:///home/conda/feedstock_root/build_artifacts/jsonpatch_1733814567314/work
jsonpointer @ file:///home/conda/feedstock_root/build_artifacts/bld/rattler-build_jsonpointer_1765026384/work
jsonschema==4.23.0
jsonschema-specifications==2024.10.1
kombu==5.5.4
libmambapy @ file:///home/conda/feedstock_root/build_artifacts/bld/rattler-build_libmambapy_1764158555/work/libmambapy
linkify-it-py==2.0.3
lz4==4.4.5
markdown-it-py==2.2.0
MarkupSafe==2.1.3
mdit-py-plugins==0.3.5
mdurl==0.1.2
memray==1.19.1
menuinst @ file:///home/conda/feedstock_root/build_artifacts/menuinst_1765733081264/work
msal==1.28.1
msal-extensions==1.2.0b1
msgpack==1.0.7
multidict==6.0.5
numpy==1.26.4
opencensus==0.11.4
opencensus-context==0.1.3
opentelemetry-api==1.34.1
opentelemetry-exporter-prometheus==0.55b1
opentelemetry-proto==1.27.0
opentelemetry-sdk==1.34.1
opentelemetry-semantic-conventions==0.55b1
ormsgpack==1.7.0
packaging @ file:///home/conda/feedstock_root/build_artifacts/packaging_1733203243479/work
pandas==1.5.3
platformdirs==3.11.0
pluggy @ file:///home/conda/feedstock_root/build_artifacts/pluggy_1733222765875/work
portalocker==2.8.2
prometheus-client==0.19.0
prompt-toolkit==3.0.41
propcache==0.3.0
proto-plus==1.22.3
protobuf==4.25.8
psutil==5.9.6
py-spy==0.4.0
pyarrow==19.0.1
pyasn1==0.5.1
pyasn1-modules==0.3.0
pycosat @ file:///home/conda/feedstock_root/build_artifacts/pycosat_1757744612102/work
pycparser==2.21
pydantic==2.12.4
pydantic_core==2.41.5
Pygments==2.18.0
PyJWT==2.8.0
pyOpenSSL==25.0.0
pyparsing==3.1.1
PySocks @ file:///home/conda/feedstock_root/build_artifacts/pysocks_1733217236728/work
python-dateutil==2.8.2
python-dotenv==1.2.1
pytz==2022.7.1
PyYAML==6.0.3
ray @ file:///home/ray/ray-2.53.0-cp310-cp310-manylinux2014_x86_64.whl#sha256=ec758f5aa71f01f090557a0fe8732689f7e2f8e49a1f39f4649ee9a7804c7514
referencing==0.36.2
requests==2.32.5
rich==13.7.1
rpds-py==0.22.3
rsa==4.7.2
ruamel.yaml @ file:///home/conda/feedstock_root/build_artifacts/ruamel.yaml_1761160605807/work
ruamel.yaml.clib @ file:///home/conda/feedstock_root/build_artifacts/ruamel.yaml.clib_1760564169911/work
s3transfer==0.8.0
scipy==1.11.4
six==1.16.0
smart-open==6.2.0
sniffio==1.3.1
starlette==0.49.1
tensorboardX==2.6.2.2
textual==4.0.0
tqdm @ file:///home/conda/feedstock_root/build_artifacts/tqdm_1735661334605/work
truststore @ file:///home/conda/feedstock_root/build_artifacts/truststore_1729762363021/work
typing-inspection==0.4.2
typing_extensions==4.15.0
tzdata==2025.2
uc-micro-py==1.0.3
uritemplate==4.1.1
urllib3==1.26.19
uvicorn==0.22.0
uvloop==0.21.0
vine==5.1.0
virtualenv==20.29.1
watchfiles==0.19.0
wcwidth==0.2.13
websockets==11.0.3
yarl==1.18.3
zipp==3.19.2
zstandard==0.25.0
```

## Install Ray Java with Maven[#](#install-ray-java-with-maven "Link to this heading")

Note

All Ray Java APIs are experimental and only supported by the community.

Before installing Ray Java with Maven, you should install Ray Python with `pip install -U ray` . Note that the versions of Ray Java and Ray Python must match.
Note that nightly Ray python wheels are also required if you want to install Ray Java snapshot version.

Find the latest Ray Java release in the [central repository](https://mvnrepository.com/artifact/io.ray). To use the latest Ray Java release in your application, add the following entries in your `pom.xml`:

```
<dependency>
  <groupId>io.ray</groupId>
  <artifactId>ray-api</artifactId>
  <version>${ray.version}</version>
</dependency>
<dependency>
  <groupId>io.ray</groupId>
  <artifactId>ray-runtime</artifactId>
  <version>${ray.version}</version>
</dependency>
```

The latest Ray Java snapshot can be found in [sonatype repository](https://oss.sonatype.org/#nexus-search;quick~io.ray). To use the latest Ray Java snapshot in your application, add the following entries in your `pom.xml`:

```
<!-- only needed for snapshot version of ray -->
<repositories>
  <repository>
    <id>sonatype</id>
    <url>https://oss.sonatype.org/content/repositories/snapshots/</url>
    <releases>
      <enabled>false</enabled>
    </releases>
    <snapshots>
      <enabled>true</enabled>
    </snapshots>
  </repository>
</repositories>

<dependencies>
  <dependency>
    <groupId>io.ray</groupId>
    <artifactId>ray-api</artifactId>
    <version>${ray.version}</version>
  </dependency>
  <dependency>
    <groupId>io.ray</groupId>
    <artifactId>ray-runtime</artifactId>
    <version>${ray.version}</version>
  </dependency>
</dependencies>
```

Note

When you run `pip install` to install Ray, Java jars are installed as well. The above dependencies are only used to build your Java code and to run your code in local mode.

If you want to run your Java code in a multi-node Ray cluster, it’s better to exclude Ray jars when packaging your code to avoid jar conflicts if the versions (installed Ray with `pip install` and maven dependencies) don’t match.

## Install Ray C++[#](#install-ray-c "Link to this heading")

Note

All Ray C++ APIs are experimental and only supported by the community.

You can install and use Ray C++ API as follows.

```
pip install -U ray[cpp]

# Create a Ray C++ project template to start with.
ray cpp --generate-bazel-project-template-to ray-template
```

Note

If you build Ray from source, remove the build option `build --cxxopt="-D_GLIBCXX_USE_CXX11_ABI=0"` from the file `cpp/example/.bazelrc` before running your application. The related issue is [this](https://github.com/ray-project/ray/issues/26031).

On this page

[Edit
on GitHub](https://github.com/ray-project/ray/edit/master/doc/source/ray-overview/installation.rst)