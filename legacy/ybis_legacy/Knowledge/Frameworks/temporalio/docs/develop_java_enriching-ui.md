Enriching the User Interface - Java SDK | Temporal Platform Documentation



[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

Temporal supports adding context to Workflows and Events with metadata.
This helps users identify and understand Workflows and their operations.

## Adding Summary and Details to Workflows[​](#adding-summary-and-details-to-workflows "Direct link to Adding Summary and Details to Workflows")

### Starting a Workflow[​](#starting-a-workflow "Direct link to Starting a Workflow")

When starting a workflow, you can provide a static summary and details to help identify the Workflow in the UI:

```
import io.temporal.client.WorkflowClient;  
import io.temporal.client.WorkflowOptions;  
import io.temporal.serviceclient.WorkflowServiceStubs;  
  
public class Main {  
    public static void main(String[] args) {  
        // Create service stubs and workflow client  
        WorkflowServiceStubs service = WorkflowServiceStubs.newLocalServiceStubs();  
        WorkflowClient workflowClient = WorkflowClient.newInstance(service);  
          
        // Create workflow options with static summary and details  
        WorkflowOptions options = WorkflowOptions.newBuilder()  
                .setWorkflowId("your-workflow-id")  
                .setTaskQueue("your-task-queue")  
                .setStaticSummary("Order processing for customer #12345")  
                .setStaticDetails("Processing premium order with expedited shipping")  
                .build();  
          
        // Create the workflow stub  
        YourWorkflow workflow = workflowClient.newWorkflowStub(YourWorkflow.class, options);  
          
        // Start the workflow  
        String result = workflow.yourWorkflowMethod("workflow input");  
    }  
}
```

`setStaticSummary()` sets a single-line description that appears in the Workflow list view, limited to 200 bytes.
`setStaticDetails()` sets multi-line comprehensive information that appears in the Workflow details view, with a larger limit of 20K bytes.

The input format is standard Markdown excluding images, HTML, and scripts.

You can also use `WorkflowClient.start()` for async execution:

```
// Start workflow asynchronously  
WorkflowExecution execution = WorkflowClient.start(workflow::yourWorkflowMethod, "workflow input");
```

### Inside the Workflow[​](#inside-the-workflow "Direct link to Inside the Workflow")

Within a Workflow, you can get and set the *current workflow details*.
Unlike static summary/details set at Workflow start, this value can be updated throughout the life of the Workflow.
Current Workflow details also takes Markdown format (excluding images, HTML, and scripts) and can span multiple lines.

```
import io.temporal.workflow.Workflow;  
  
public class YourWorkflowImpl implements YourWorkflow {  
    @Override  
    public String yourWorkflowMethod(String input) {  
        // Get the current details  
        String currentDetails = Workflow.getCurrentDetails();  
        Workflow.getLogger(YourWorkflowImpl.class).info("Current details: " + currentDetails);  
          
        // Set/update the current details  
        Workflow.setCurrentDetails("Updated workflow details with new status");  
          
        return "Workflow completed";  
    }  
}
```

### Adding Summary to Activities and Timers[​](#adding-summary-to-activities-and-timers "Direct link to Adding Summary to Activities and Timers")

You can attach a `setSummary()` to Activities when starting them from within a Workflow:

```
import io.temporal.activity.ActivityOptions;  
import io.temporal.workflow.Workflow;  
import java.time.Duration;  
  
public class YourWorkflowImpl implements YourWorkflow {  
    private final YourActivities activities =   
        Workflow.newActivityStub(YourActivities.class,  
            ActivityOptions.newBuilder()  
                .setStartToCloseTimeout(Duration.ofSeconds(10))  
                .setSummary("Processing user data")  
                .build());  
      
    @Override  
    public String yourWorkflowMethod(String input) {  
        // Execute the activity with the summary  
        String result = activities.yourActivity(input);  
        return result;  
    }  
}
```

Similarly, you can attach a `setSummary()` to timers within a Workflow:

```
import io.temporal.workflow.Workflow;  
import io.temporal.workflow.TimerOptions;  
import java.time.Duration;  
  
public class YourWorkflowImpl implements YourWorkflow {  
    @Override  
    public String yourWorkflowMethod(String input) {  
        // Create a timer with a summary  
        Workflow.newTimer(Duration.ofMinutes(5),   
            TimerOptions.newBuilder()  
                .setSummary("Waiting for payment confirmation")  
                .build())  
            .get(); // Wait for the timer to fire  
          
        return "Timer completed";  
    }  
}
```

The input format for `setSummary()` is a string, and limited to 200 bytes.

## Viewing Summary and Details in the UI[​](#viewing-summary-and-details-in-the-ui "Direct link to Viewing Summary and Details in the UI")

Once you've added summaries and details to your Workflows, Activities, and Timers, you can view this enriched information in the Temporal Web UI.
Navigate to your Workflow's details page to see the metadata displayed in two key locations:

### Workflow Overview Section[​](#workflow-overview-section "Direct link to Workflow Overview Section")

At the top of the workflow details page, you'll find the workflow-level metadata:

* **Summary & Details** - Displays the static summary and static details set when starting the workflow
* **Current Details** - Displays the dynamic details that can be updated during workflow execution

All Workflow details support standard Markdown formatting (excluding images, HTML, and scripts), allowing you to create rich, structured information displays.

### Event History[​](#event-history "Direct link to Event History")

Individual events in the Workflow's Event History display their associated summaries when available.

Workflow, Activity and Timer summaries appear in purple text next to their corresponding events, providing immediate context without requiring you to expand the Event details.
When you do expand an Event, the summary is also prominently displayed in the detailed view.

* [Adding Summary and Details to Workflows](#adding-summary-and-details-to-workflows)
  + [Starting a Workflow](#starting-a-workflow)+ [Inside the Workflow](#inside-the-workflow)+ [Adding Summary to Activities and Timers](#adding-summary-to-activities-and-timers)* [Viewing Summary and Details in the UI](#viewing-summary-and-details-in-the-ui)
    + [Workflow Overview Section](#workflow-overview-section)+ [Event History](#event-history)