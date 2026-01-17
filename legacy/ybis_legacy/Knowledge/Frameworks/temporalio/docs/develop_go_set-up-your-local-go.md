Set up your local with the Go SDK | Temporal Platform Documentation



[Skip to main content](#__docusaurus_skipToContent_fallback)

Configure your local development environment to get started developing with Temporal.

## Install Go[​](#install-go "Direct link to Install Go")

Make sure you have Go installed. These tutorials were produced using Go 1.18. Check your version of Go with the following command:

This will return your installed Go version.

```
go version
```

```
go version go1.18.1 darwin/amd64
```

## Install the Temporal Go SDK[​](#install-the-temporal-go-sdk "Direct link to Install the Temporal Go SDK")

If you are creating a new project using the Temporal Go SDK, you can start by creating a new directory.

Next, switch to the new directory.

Then, initialize a Go project in that directory.

Finally, install the Temporal SDK with `go get`.

```
mkdir goproject
```

```
cd goproject
```

```
go mod init my-org/greeting
```

```
go get go.temporal.io/sdk
```

```
go get go.temporal.io/sdk/client
```

```
go mod tidy
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

The Temporal Web UI may be on a different port in some examples or tutorials. To change the port for the Web UI, use the `--ui-port` option when starting the server:

```
temporal server start-dev --ui-port 8080
```

The Temporal Web UI will now be available at http://localhost:8080.

## Run Hello World: Test Your Installation[​](#run-hello-world-test-your-installation "Direct link to Run Hello World: Test Your Installation")

Now let's verify your setup is working by creating and running a complete Temporal application with both a Workflow and Activity.

This test will confirm that:

* The Temporal Go SDK is properly installed
* Your local Temporal Service is running
* You can successfully create and execute Workflows and Activities
* The communication between components is functioning correctly

### 1. Create the Activity[​](#1-create-the-activity "Direct link to 1. Create the Activity")

An Activity is a normal function or method that executes a single, well-defined action (either short- or long-running) that is typically prone to failure.
Examples include any action that interacts with the outside world, such as sending emails, making network requests, writing to a database, or calling an API.
If an Activity fails, Temporal automatically retries it based on your configuration.

Create an Activity file (activity.go):

```
package greeting  
  
import (  
	"context"  
	"fmt"  
)  
  
func Greet(ctx context.Context, name string) (string, error) {  
	return fmt.Sprintf("Hello %s", name), nil  
}
```

### 2. Create the Workflow[​](#2-create-the-workflow "Direct link to 2. Create the Workflow")

Workflows orchestrate Activities and contain the application logic.
Temporal Workflows are resilient.
They can run—and keep running—for years, even if the underlying infrastructure fails.
If the application itself crashes, Temporal will automatically recreate its pre-failure state so it can continue right where it left off.

Create a Workflow file (workflow.go):

```
package greeting  
  
import (  
	"time"  
  
	"go.temporal.io/sdk/workflow"  
)  
  
func SayHelloWorkflow(ctx workflow.Context, name string) (string, error) {  
	ao := workflow.ActivityOptions{  
		StartToCloseTimeout: time.Second * 10,  
	}  
	ctx = workflow.WithActivityOptions(ctx, ao)  
  
	var result string  
	err := workflow.ExecuteActivity(ctx, Greet, name).Get(ctx, &result)  
	if err != nil {  
		return "", err  
	}  
  
	return result, nil  
}
```

### 3. Create and Run the Worker[​](#3-create-and-run-the-worker "Direct link to 3. Create and Run the Worker")

With your Activity and Workflow defined, you need a Worker to execute them. A Worker polls a Task Queue, that you configure it to poll, looking for work to do. Once the Worker dequeues a Workflow or Activity task from the Task Queue, it then executes that task.

Workers are a crucial part of your Temporal application as they're what actually execute the tasks defined in your Workflows and Activities.
For more information on Workers, see [Understanding Temporal](/evaluate/understanding-temporal#workers) and a [deep dive into Workers](/workers).

Create a Worker file (worker/main.go):

```
package main  
  
import (  
	"log"  
  
	"my-org/greeting"  
  
	"go.temporal.io/sdk/client"  
	"go.temporal.io/sdk/worker"  
)  
  
func main() {  
	c, err := client.Dial(client.Options{})  
	if err != nil {  
		log.Fatalln("Unable to create client", err)  
	}  
	defer c.Close()  
  
	w := worker.New(c, "my-task-queue", worker.Options{})  
  
	w.RegisterWorkflow(greeting.SayHelloWorkflow)  
	w.RegisterActivity(greeting.Greet)  
  
	err = w.Run(worker.InterruptCh())  
	if err != nil {  
		log.Fatalln("Unable to start worker", err)  
	}  
}
```

Run the Worker:

```
go run worker/main.go
```

### 4. Execute the Workflow[​](#4-execute-the-workflow "Direct link to 4. Execute the Workflow")

Now that your Worker is running, it's time to start a Workflow Execution.

Create a separate file called start/main.go:

```
package main  
  
import (  
	"context"  
	"log"  
	"os"  
  
	greeting "my-org/greeting"  
  
	"go.temporal.io/sdk/client"  
)  
  
func main() {  
	c, err := client.Dial(client.Options{})  
	if err != nil {  
		log.Fatalln("Unable to create client", err)  
	}  
	defer c.Close()  
  
	options := client.StartWorkflowOptions{  
		ID:        "greeting-workflow",  
		TaskQueue: "my-task-queue",  
	}  
  
	we, err := c.ExecuteWorkflow(context.Background(), options, greeting.SayHelloWorkflow, os.Args[1])  
	if err != nil {  
		log.Fatalln("Unable to execute workflow", err)  
	}  
	log.Println("Started workflow", "WorkflowID", we.GetID(), "RunID", we.GetRunID())  
  
	var result string  
	err = we.Get(context.Background(), &result)  
	if err != nil {  
		log.Fatalln("Unable get workflow result", err)  
	}  
	log.Println("Workflow result:", result)  
}
```

Then run:

```
go run start/main.go Temporal
```

### Verify Success[​](#verify-success "Direct link to Verify Success")

If everything is working correctly, you should see:

* Worker processing the workflow and activity
* Output: `Workflow result: Hello Temporal`
* Workflow Execution details in the [Temporal Web UI](http://localhost:8233)

[### Next: Run your first Temporal Application

Create a basic Workflow and run it with the Temporal Go SDK

→](https://learn.temporal.io/getting_started/go/first_program_in_go/)