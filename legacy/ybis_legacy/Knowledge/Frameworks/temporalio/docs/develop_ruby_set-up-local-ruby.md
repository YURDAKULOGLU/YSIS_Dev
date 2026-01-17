Set up your local with the Ruby SDK | Temporal Platform Documentation



[Skip to main content](#__docusaurus_skipToContent_fallback)

This guide walks you through setting up the Temporal Ruby SDK and running your first Workflow.
In just a few steps, you'll install the SDK and start a local development server.
To validate that your local environment is correctly installed, we will execute a Workflow that will output "Hello, Temporal".

## Installation[​](#installation "Direct link to Installation")

This step sets up a new Ruby project using Bundler and installs the Temporal Ruby SDK.

We recommend using [Bundler](https://bundler.io/) to manage your Ruby project dependencies, including the Temporal SDK. These tutorials assume Ruby 3.4.3 or higher.

Follow the steps to create a directory, initialize the project with a `Gemfile`, and add the Temporal SDK.

**Note:**

* Only macOS ARM/x64 and Linux ARM/x64 are supported.
* Source gem is published but **cannot be built directly**.
* Windows (MinGW) is not supported.
* `fibers`/`async` are only supported on Ruby **3.3+**.
* See [Platform Support](#) for full details.

**1. Check your Ruby version:**

```
ruby -v
```

You should see output like `ruby 3.4.3`. Ruby 3.2+ is required. We recommend Ruby 3.4.3.

**2. Create your project folder:**

```
mkdir temporal-project cd temporal-project
```

**3. Initialize with Bundler:**

```
bundle init
```

**4. Add the Temporal Ruby SDK:**

```
bundle add temporalio
```

You should see output like:

```
Fetching gem metadata from https://rubygems.org/... Resolving dependencies... Installing temporalio 0.4.0 (arm64-darwin) Bundle complete! 1 Gemfile dependency, 6 gems now installed.
```

**5. Install dependencies:**

```
bundle install
```

## Install Temporal CLI[​](#install-temporal-cli "Direct link to Install Temporal CLI")

The fastest way to get a development version of the Temporal Service running on your local machine is to use [Temporal CLI](https://docs.temporal.io/cli).

Choose your operating system to install Temporal CLI.

* macOS* Windows* Linux

Install the Temporal CLI using Homebrew:

```
brew install temporal
```

Download the Temporal CLI archive for your architecture:

* [Windows amd64](https://temporal.download/cli/archive/latest?platform=windows&arch=amd64)* [Windows arm64](https://temporal.download/cli/archive/latest?platform=windows&arch=arm64)

Extract it and add `temporal.exe` to your PATH.

Download the Temporal CLI for your architecture:

* [Linux amd64](https://temporal.download/cli/archive/latest?platform=linux&arch=amd64)* [Linux arm64](https://temporal.download/cli/archive/latest?platform=linux&arch=arm64)

Extract the archive and move the `temporal` binary into your PATH, for example:

```
sudo mv temporal /usr/local/bin
```

## Start the development server[​](#start-the-development-server "Direct link to Start the development server")

Once you've installed Temporal CLI and added it to your PATH, open a new Terminal window and run the following command.

This command starts a local Temporal Service. It starts the Web UI, creates the default Namespace, and uses an in-memory database.

The Temporal Service will be available on localhost:7233.
The Temporal Web UI will be available at <http://localhost:8233>.

Leave the local Temporal Service running as you work through tutorials and other projects. You can stop the Temporal Service at any time by pressing CTRL+C.

Once you have everything installed, you're ready to build apps with Temporal on your local machine.

After installing, open a new Terminal window and start the development server:

```
temporal server start-dev
```

#### Change the Web UI port

The Temporal Web UI may be on a different port in some examples or tutorials. To change the port for the Web UI, use the `--ui-port` option when starting the server:

```
temporal server start-dev --ui-port 8080
```

The Temporal Web UI will now be available at http://localhost:8080.

## Run Hello World: Test Your Installation[​](#run-hello-world-test-your-installation "Direct link to Run Hello World: Test Your Installation")

Now let's verify your setup is working by creating and running a complete Temporal application with both a Workflow and Activity.

This test will confirm that:

* The Temporal Ruby SDK is properly installed
* Your local Temporal Service is running
* You can successfully create and execute Workflows and Activities
* The communication between components is functioning correctly

### 1. Create the Activity[​](#1-create-the-activity "Direct link to 1. Create the Activity")

Create an Activity file (say\_hello\_activity.rb):

```
require 'temporalio/activity'  
  
# Implementation of a simple activity  
class SayHelloActivity < Temporalio::Activity::Definition  
  def execute(name)  
    "Hello, #{name}!"  
  end  
end
```

### 2. Create the Workflow[​](#2-create-the-workflow "Direct link to 2. Create the Workflow")

Create a Workflow file (say\_hello\_workflow.rb):

```
require 'temporalio/workflow'  
require_relative 'say_hello_activity'  
  
class SayHelloWorkflow < Temporalio::Workflow::Definition  
  def execute(name)  
    Temporalio::Workflow.execute_activity(  
      SayHelloActivity,  
      name,  
      schedule_to_close_timeout: 300  
    )  
  end  
end
```

### 3. Create and Run the Worker[​](#3-create-and-run-the-worker "Direct link to 3. Create and Run the Worker")

With your Activity and Workflow defined, you need a Worker to execute them.
Workers are a crucial part of your Temporal application as they're what actually execute the tasks defined in your Workflows and Activities.
For more information on Workers, see [Understanding Temporal](/evaluate/understanding-temporal#workers) and a [deep dive into Workers](/workers).

Create a Worker file (worker.rb):

```
require 'temporalio/client'  
require 'temporalio/worker'  
require_relative 'say_hello_activity'  
require_relative 'say_hello_workflow'  
  
# Create a client  
client = Temporalio::Client.connect('localhost:7233', 'default')  
  
# Create a worker with the client, activities, and workflows  
worker = Temporalio::Worker.new(  
  client:,  
  task_queue: 'my-task-queue',  
  workflows: [SayHelloWorkflow],  
  # There are various forms an activity can take, see "Activities" section for details  
  activities: [SayHelloActivity]  
)  
  
# Run the worker until SIGINT. This can be done in many ways, see "Workers" section for details.  
worker.run(shutdown_signals: ['SIGINT'])
```

Run the Worker:

```
ruby worker.rb
```

### 4. Execute the Workflow[​](#4-execute-the-workflow "Direct link to 4. Execute the Workflow")

Now that your Worker is running, it's time to start a Workflow Execution.

Create a separate file called starter.rb:

```
require 'temporalio/client'  
require_relative 'say_hello_workflow'  
  
# Create a client  
client = Temporalio::Client.connect('localhost:7233', 'default')  
  
# Run workflow  
result = client.execute_workflow(  
  SayHelloWorkflow,  
  'Temporal', # This is the input to the workflow  
  id: 'my-workflow-id',  
  task_queue: 'my-task-queue'  
)  
puts "Result: #{result}"
```

Then run:

```
ruby starter.rb
```

### Verify Success[​](#verify-success "Direct link to Verify Success")

If everything is working correctly, you should see:

* Worker processing the workflow and activity
* Output: `Workflow result: Hello, Temporal!`
* Workflow Execution details in the [Temporal Web UI](http://localhost:8233)

[### Next: Run your first Temporal Application

Create a basic Workflow and run it with the Temporal Ruby SDK

→](https://learn.temporal.io/getting_started/ruby/first_program_in_ruby/)