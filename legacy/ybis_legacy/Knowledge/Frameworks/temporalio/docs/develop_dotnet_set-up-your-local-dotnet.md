Set up your local with the .NET SDK | Temporal Platform Documentation



[Skip to main content](#__docusaurus_skipToContent_fallback)

Configure your local development environment to get started developing with Temporal.

## Install .NET[​](#install-net "Direct link to Install .NET")

The .NET SDK requires .NET 6.0 or later.
Install .NET by following the [official .NET instructions](https://dotnet.microsoft.com/download/dotnet/6.0).

The .NET SDK requires .NET 6.0 or later.

Install .NET by following the [official .NET instructions](https://dotnet.microsoft.com/download/dotnet/6.0).

## Install the Temporal .NET SDK[​](#install-the-temporal-net-sdk "Direct link to Install the Temporal .NET SDK")

Create a solution and the three projects used in this guide: `Workflow` (class library), `Worker` (console), and `Client` (console). Add them to the solution.

Tip: You can also centralize the `Temporalio` package for all projects using `Directory.Packages.props` and `Directory.Build.props` at the solution root.

```
# Create solution and projects  
mkdir TemporalioHelloWorld  
cd TemporalioHelloWorld  
  
dotnet new sln -n TemporalioHelloWorld  
  
dotnet new classlib -o Workflow  
dotnet new console -o Worker  
dotnet new console -o Client  
  
# Add projects to the solution  
dotnet sln TemporalioHelloWorld.sln add Workflow/Workflow.csproj Worker/Worker.csproj Client/Client.csproj  
  
# Add project references  
dotnet add Worker/Worker.csproj reference Workflow/Workflow.csproj  
dotnet add Client/Client.csproj reference Workflow/Workflow.csproj  
  
# Install Temporal SDK in each project  
dotnet add Workflow/Workflow.csproj package Temporalio  
dotnet add Worker/Worker.csproj package Temporalio  
dotnet add Client/Client.csproj package Temporalio
```

Build the solution:

```
dotnet build
```

## Install Temporal CLI and start the development server[​](#install-temporal-cli-and-start-the-development-server "Direct link to Install Temporal CLI and start the development server")

The fastest way to get a development version of the Temporal Service running on your local machine is to use [Temporal CLI](https://docs.temporal.io/cli).

Choose your operating system to install Temporal CLI:

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

The Temporal Web UI may be on a different port in some examples or tutorials. To change the `--ui-port` option when starting the server:

```
temporal server start-dev --ui-port 8080
```

The Temporal Web UI will now be available at http://localhost:8080.

## Run Hello World: Test Your Installation[​](#run-hello-world-test-your-installation "Direct link to Run Hello World: Test Your Installation")

Now let's verify your setup is working by creating and running a complete Temporal application with both a Workflow and Activity.

This test will confirm that:

* Your .NET SDK installation is working
* Your local Temporal Service is running
* You can successfully create and execute Workflows and Activities
* The communication between components is functioning correctly

Tip: Example Directory Structure

```
TemporalioHelloWorld/  
├── Client/  
│   ├── Client.csproj  
│   └── Program.cs              # Starts a workflow  
├── Worker/  
│   ├── Worker.csproj  
│   └── Program.cs              # Runs a worker  
├── Workflow/  
│   ├── Workflow.csproj  
│   ├── MyActivities.cs         # Activity definition  
│   └── SayHelloWorkflow.cs     # Workflow definition  
└── TemporalioHelloWorld.sln
```

### 1. Create the Activity and Workflow[​](#1-create-the-activity-and-workflow "Direct link to 1. Create the Activity and Workflow")

#### Create an Activity file (MyActivities.cs) in the Workflow project:[​](#create-an-activity-file-myactivitiescs-in-the-workflow-project "Direct link to Create an Activity file (MyActivities.cs) in the Workflow project:")

```
namespace MyNamespace;  
  
using Temporalio.Activities;  
  
public class MyActivities  
{  
    // Activities can be async and/or static too! We just demonstrate instance  
    // methods since many will use them that way.  
    [Activity]  
    public string SayHello(string name) => $"Hello, {name}!";  
}
```

An Activity is a normal function or method that executes a single, well-defined action (either short or long running), which often involve interacting with the outside world, such as sending emails, making network requests, writing to a database, or calling an API, which are prone to failure.
If an Activity fails, Temporal automatically retries it based on your configuration.

#### Create a Workflow file (SayHelloWorkflow.cs) in the Workflow project:[​](#create-a-workflow-file-sayhelloworkflowcs-in-the-workflow-project "Direct link to Create a Workflow file (SayHelloWorkflow.cs) in the Workflow project:")

```
namespace MyNamespace;  
  
using Temporalio.Workflows;  
  
[Workflow]  
public class SayHelloWorkflow  
{  
    [WorkflowRun]  
    public async Task<string> RunAsync(string name)  
    {  
        // This workflow just runs a simple activity to completion.  
        // StartActivityAsync could be used to just start and there are many  
        // other things that you can do inside a workflow.  
        return await Workflow.ExecuteActivityAsync(  
            // This is a lambda expression where the instance is typed. If this  
            // were static, you wouldn't need a parameter.  
            (MyActivities act) => act.SayHello(name),  
            new() { StartToCloseTimeout = TimeSpan.FromMinutes(5) }  
        );  
    }  
}
```

Workflows orchestrate Activities and contain the application logic.
Temporal Workflows are resilient.
They can run and keep running for years, even if the underlying infrastructure fails.
If the application itself crashes, Temporal will automatically recreate its pre-failure state so it can continue right where it left off.

### 2. Create the Worker[​](#2-create-the-worker "Direct link to 2. Create the Worker")

With your Activity and Workflow defined, you need a Worker to execute them.

#### Create a Worker file (Program.cs) in the Worker project:[​](#create-a-worker-file-programcs-in-the-worker-project "Direct link to Create a Worker file (Program.cs) in the Worker project:")

```
using MyNamespace;  
using Temporalio.Client;  
using Temporalio.Worker;  
  
// Create a client to localhost on "default" namespace  
var client = await TemporalClient.ConnectAsync(new("localhost:7233"));  
  
// Cancellation token to shutdown worker on ctrl+c  
using var tokenSource = new CancellationTokenSource();  
Console.CancelKeyPress += (_, eventArgs) =>  
{  
    tokenSource.Cancel();  
    eventArgs.Cancel = true;  
};  
  
// Create an activity instance since we have instance activities. If we had  
// all static activities, we could just reference those directly.  
var activities = new MyActivities();  
  
// Create worker with the activity and workflow registered  
using var worker = new TemporalWorker(  
    client,  
    new TemporalWorkerOptions("my-task-queue")  
        .AddActivity(activities.SayHello)  
        .AddWorkflow<SayHelloWorkflow>()  
);  
  
// Run worker until cancelled  
Console.WriteLine("Running worker");  
try  
{  
    await worker.ExecuteAsync(tokenSource.Token);  
}  
catch (OperationCanceledException)  
{  
    Console.WriteLine("Worker cancelled");  
}
```

Run the Worker:

```
dotnet run --project Worker/Worker.csproj
```

Keep this terminal running - you should see `Running worker` displayed.

A Worker polls a Task Queue, that you configure it to poll, looking for work to do.
Once the Worker dequeues the Workflow or Activity task from the Task Queue, it then executes that task.

Workers are a crucial part of your Temporal application as they're what actually execute the tasks defined in your Workflows and Activities.
For more information on Workers, see [Understanding Temporal](/evaluate/understanding-temporal#workers) and a [deep dive into Workers](/workers).

### 3. Execute the Workflow[​](#3-execute-the-workflow "Direct link to 3. Execute the Workflow")

Now that your Worker is running, it's time to start a Workflow Execution.
This final step will validate that everything is working correctly.

#### Create a Client file (Program.cs) in the Client project:[​](#create-a-client-file-programcs-in-the-client-project "Direct link to Create a Client file (Program.cs) in the Client project:")

```
using MyNamespace;  
using Temporalio.Client;  
  
// Create a client to localhost on "default" namespace  
var client = await TemporalClient.ConnectAsync(new("localhost:7233"));  
  
// Run workflow  
var result = await client.ExecuteWorkflowAsync(  
    (SayHelloWorkflow wf) => wf.RunAsync("Temporal"),  
    new(id: $"my-workflow-id-{Guid.NewGuid()}", taskQueue: "my-task-queue")  
);  
  
Console.WriteLine("Workflow result: {0}", result);
```

While the Worker is still running, run the Workflow:

```
dotnet run --project Client/Client.csproj
```

### Verify Success[​](#verify-success "Direct link to Verify Success")

If everything is working correctly, you should see:

* Worker processing the workflow and activity
* Output: `Workflow result: Hello Temporal`
* Workflow Execution details in the [Temporal Web UI](http://localhost:8233)

[### Next: Run your first Temporal Application

Create a basic Workflow and run it with the Temporal .NET SDK

→](https://learn.temporal.io/getting_started/dotnet/first_program_in_dotnet/)