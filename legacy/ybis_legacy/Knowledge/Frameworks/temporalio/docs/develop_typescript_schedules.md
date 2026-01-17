Schedules - TypeScript SDK | Temporal Platform Documentation



[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

The pages shows how to do the following:

* [Schedule a Workflow](#schedule-a-workflow)
  + [Create a Scheduled Workflow](#create)
  + [Backfill a Scheduled Workflow](#backfill)
  + [Delete a Scheduled Workflow](#delete)
  + [Describe a Scheduled Workflow](#describe)
  + [List a Scheduled Workflow](#list)
  + [Pause a Scheduled Workflow](#pause)
  + [Trigger a Scheduled Workflow](#trigger)
  + [Update a Scheduled Workflow](#update)
* [Temporal Cron Jobs](#temporal-cron-jobs)
* [Start Delay](#start-delay)

## How to Schedule a Workflow[​](#schedule-a-workflow "Direct link to How to Schedule a Workflow")

Scheduling Workflows is a crucial aspect of any automation process, especially when dealing with time-sensitive tasks. By scheduling a Workflow, you can automate repetitive tasks, reduce the need for manual intervention, and ensure timely execution of your business processes

Use any of the following action to help Schedule a Workflow Execution and take control over your automation process.

### How to Create a Scheduled Workflow[​](#create "Direct link to How to Create a Scheduled Workflow")

The create action enables you to create a new Schedule. When you create a new Schedule, a unique Schedule ID is generated, which you can use to reference the Schedule in other Schedule commands.

Schedule Auto-Deletion

Once a Schedule has completed creating all its Workflow Executions, the Temporal Service deletes it since it won’t fire again.
The Temporal Service doesn't guarantee when this removal will happen.

[schedules/src/start-schedule.ts](https://github.com/temporalio/samples-typescript/blob/main/schedules/src/start-schedule.ts)

```
async function run() {  
  const config = loadClientConnectConfig();  
  const connection = await Connection.connect(config.connectionOptions);  
  const client = new Client({ connection });  
  
  // https://typescript.temporal.io/api/classes/client.ScheduleClient#create  
  const schedule = await client.schedule.create({  
    action: {  
      type: 'startWorkflow',  
      workflowType: reminder,  
      args: ['♻️ Dear future self, please take out the recycling tonight. Sincerely, past you ❤️'],  
      taskQueue: 'schedules',  
    },  
    scheduleId: 'sample-schedule',  
    policies: {  
      catchupWindow: '1 day',  
      overlap: ScheduleOverlapPolicy.ALLOW_ALL,  
    },  
    spec: {  
      intervals: [{ every: '10s' }],  
      // or periodic calendar times:  
      // calendars: [  
      //   {  
      //     comment: 'every wednesday at 8:30pm',  
      //     dayOfWeek: 'WEDNESDAY',  
      //     hour: 20,  
      //     minute: 30,  
      //   },  
      // ],  
      // or a single datetime:  
      // calendars: [  
      //   {  
      //     comment: '1/1/23 at 9am',  
      //     year: 2023,  
      //     month: 1,  
      //     dayOfMonth: 1,  
      //     hour: 9,  
      //   },  
      // ],  
    },  
  });
```

### How to Backfill a Scheduled Workflow[​](#backfill "Direct link to How to Backfill a Scheduled Workflow")

The backfill action executes Actions ahead of their specified time range. This command is useful when you need to execute a missed or delayed Action, or when you want to test the Workflow before its scheduled time.

[schedules/src/backfill-schedule.ts](https://github.com/temporalio/samples-typescript/blob/main/schedules/src/backfill-schedule.ts)

```
function subtractMinutes(minutes: number): Date {  
  const now = new Date();  
  return new Date(now.getTime() - minutes * 60 * 1000);  
}  
  
async function run() {  
  const client = new Client({  
    connection: await Connection.connect(),  
  });  
  
  const backfillOptions: Backfill = {  
    start: subtractMinutes(10),  
    end: subtractMinutes(9),  
    overlap: ScheduleOverlapPolicy.ALLOW_ALL,  
  };  
  
  const handle = client.schedule.getHandle('sample-schedule');  
  await handle.backfill(backfillOptions);  
  
  console.log(`Schedule is now backfilled.`);  
}
```

### How to Delete a Scheduled Workflow[​](#delete "Direct link to How to Delete a Scheduled Workflow")

The delete action enables you to delete a Schedule. When you delete a Schedule, it does not affect any Workflows that were started by the Schedule.

[schedules/src/delete-schedule.ts](https://github.com/temporalio/samples-typescript/blob/main/schedules/src/delete-schedule.ts)

```
async function run() {  
  const client = new Client({  
    connection: await Connection.connect(),  
  });  
  
  const handle = client.schedule.getHandle('sample-schedule');  
  await handle.delete();  
  
  console.log(`Schedule is now deleted.`);  
}
```

### How to Describe a Scheduled Workflow[​](#describe "Direct link to How to Describe a Scheduled Workflow")

The describe action shows the current Schedule configuration, including information about past, current, and future Workflow Runs. This command is helpful when you want to get a detailed view of the Schedule and its associated Workflow Runs.

[schedules/src/describe-schedule.ts](https://github.com/temporalio/samples-typescript/blob/main/schedules/src/describe-schedule.ts)

```
async function run() {  
  const client = new Client({  
    connection: await Connection.connect(),  
  });  
  
  const handle = client.schedule.getHandle('sample-schedule');  
  
  const result = await handle.describe();  
  
  console.log(`Schedule description: ${JSON.stringify(result)}`);  
}
```

### How to List a Scheduled Workflow[​](#list "Direct link to How to List a Scheduled Workflow")

The list action lists all the available Schedules. This command is useful when you want to view a list of all the Schedules and their respective Schedule IDs.

[schedules/src/list-schedule.ts](https://github.com/temporalio/samples-typescript/blob/main/schedules/src/list-schedule.ts)

```
async function run() {  
  const client = new Client({  
    connection: await Connection.connect(),  
  });  
  
  const schedules = [];  
  
  const scheduleList = client.schedule.list();  
  
  for await (const schedule of scheduleList) {  
    schedules.push(schedule);  
  }  
  
  console.log(`Schedules are now listed: ${JSON.stringify(schedules)}`);  
}
```

### How to Pause a Scheduled Workflow[​](#pause "Direct link to How to Pause a Scheduled Workflow")

The pause action enables you to pause and unpause a Schedule. When you pause a Schedule, all the future Workflow Runs associated with the Schedule are temporarily stopped. This command is useful when you want to temporarily halt a Workflow due to maintenance or any other reason.

[schedules/src/pause-schedule.ts](https://github.com/temporalio/samples-typescript/blob/main/schedules/src/pause-schedule.ts)

```
async function run() {  
  const client = new Client({  
    connection: await Connection.connect(),  
  });  
  
  const handle = client.schedule.getHandle('sample-schedule');  
  await handle.pause();  
  
  console.log(`Schedule is now paused.`);  
}
```

### How to Trigger a Scheduled Workflow[​](#trigger "Direct link to How to Trigger a Scheduled Workflow")

The trigger action triggers an immediate action with a given Schedule. By default, this action is subject to the Overlap Policy of the Schedule. This command is helpful when you want to execute a Workflow outside of its scheduled time.

[schedules/src/trigger-schedule.ts](https://github.com/temporalio/samples-typescript/blob/main/schedules/src/trigger-schedule.ts)

```
async function run() {  
  const client = new Client({  
    connection: await Connection.connect(),  
  });  
  
  const handle = client.schedule.getHandle('sample-schedule');  
  
  await handle.trigger();  
  
  console.log(`Schedule is now triggered.`);  
}
```

### How to Update a Scheduled Workflow[​](#update "Direct link to How to Update a Scheduled Workflow")

The update action enables you to update an existing Schedule. This command is useful when you need to modify the Schedule's configuration, such as changing the start time, end time, or interval.

[schedules/src/update-schedule.ts](https://github.com/temporalio/samples-typescript/blob/main/schedules/src/update-schedule.ts)

```
const updateSchedule = (  
  input: ScheduleDescription,  
): ScheduleUpdateOptions<ScheduleOptionsStartWorkflowAction<Workflow>> => {  
  const scheduleAction = input.action;  
  
  scheduleAction.args = ['my updated schedule arg'];  
  
  return { ...input, ...scheduleAction };  
};  
  
async function run() {  
  const client = new Client({  
    connection: await Connection.connect(),  
  });  
  
  const handle = client.schedule.getHandle('sample-schedule');  
  
  await handle.update(updateSchedule);  
  
  console.log(`Schedule is now updated.`);  
}
```

## How to use Temporal Cron Jobs[​](#temporal-cron-jobs "Direct link to How to use Temporal Cron Jobs")

Cron support is not recommended

We recommend using [Schedules](https://docs.temporal.io/schedule) instead of Cron Jobs.
Schedules were built to provide a better developer experience, including more configuration options and the ability to update or pause running Schedules.

A [Temporal Cron Job](/cron-job) is the series of Workflow Executions that occur when a Cron Schedule is provided in the call to spawn a Workflow Execution.

A Cron Schedule is provided as an option when the call to spawn a Workflow Execution is made.

You can set each Workflow to repeat on a schedule with the `cronSchedule` option:

```
const handle = await client.workflow.start(scheduledWorkflow, {  
  // ...  
  cronSchedule: '* * * * *', // start every minute  
});
```

Temporal Workflow Schedule Cron strings follow this format:

```
┌───────────── minute (0 - 59)  
│ ┌───────────── hour (0 - 23)  
│ │ ┌───────────── day of the month (1 - 31)  
│ │ │ ┌───────────── month (1 - 12)  
│ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday)  
│ │ │ │ │  
* * * * *
```

## Start Delay[​](#start-delay "Direct link to Start Delay")

**How to use Start Delay**

Use the `startDelay` to schedule a Workflow Execution at a specific one-time future point rather than on a recurring schedule.

You may specify the `startDelay` option on either the [`client.workflow.start()`](https://typescript.temporal.io/api/classes/client.WorkflowClient#start) or [`client.workflow.execute()`](https://typescript.temporal.io/api/classes/client.WorkflowClient#execute) methods of a Workflow Client.
For example:

```
const handle = await client.workflow.start(someWorkflow, {  
  // ...  
  startDelay: '2 hours',  
});
```

* [How to Schedule a Workflow](#schedule-a-workflow)* [How to use Temporal Cron Jobs](#temporal-cron-jobs)* [Start Delay](#start-delay)