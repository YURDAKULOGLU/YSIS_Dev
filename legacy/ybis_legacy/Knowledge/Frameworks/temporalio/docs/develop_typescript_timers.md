Durable Timers - TypeScript SDK | Temporal Platform Documentation



[Skip to main content](#__docusaurus_skipToContent_fallback)

On this page

## What is a Timer?[​](#timers "Direct link to What is a Timer?")

A Workflow can set a durable Timer for a fixed time period.
In some SDKs, the function is called `sleep()`, and in others, it's called `timer()`.

A Workflow can sleep for months.
Timers are persisted, so even if your Worker or Temporal Service is down when the time period completes, as soon as your Worker and Temporal Service are back up, the `sleep()` call will resolve and your code will continue executing.

Sleeping is a resource-light operation: it does not tie up the process, and you can run millions of Timers off a single Worker.

## Asynchronous design patterns in TypeScript[​](#asynchronous-design-patterns "Direct link to Asynchronous design patterns in TypeScript")

The real value of `sleep` and `condition` is in knowing how to use them to model asynchronous business logic.
Here are some examples we use the most; we welcome more if you can think of them!

Racing Timers

Use `Promise.race` with Timers to dynamically adjust delays.

```
export async function processOrderWorkflow({  
  orderProcessingMS,  
  sendDelayedEmailTimeoutMS,  
}: ProcessOrderOptions): Promise<void> {  
  let processing = true;  
  const processOrderPromise = processOrder(orderProcessingMS).then(() => {  
    processing = false;  
  });  
  
  await Promise.race([processOrderPromise, sleep(sendDelayedEmailTimeoutMS)]);  
  
  if (processing) {  
    await sendNotificationEmail();  
    await processOrderPromise;  
  }  
}
```



Racing Signals

Use `Promise.race` with Signals and Triggers to have a promise resolve at the earlier of either system time or human intervention.

```
import { defineSignal, sleep, Trigger } from '@temporalio/workflow';  
  
const userInteraction = new Trigger<boolean>();  
const completeUserInteraction = defineSignal('completeUserInteraction');  
  
export async function yourWorkflow(userId: string) {  
  setHandler(completeUserInteraction, () => userInteraction.resolve(true)); // programmatic resolve  
  const userInteracted = await Promise.race([  
    userInteraction,  
    sleep('30 days'),  
  ]);  
  if (!userInteracted) {  
    await sendReminderEmail(userId);  
  }  
}
```

You can invert this to create a reminder pattern where the promise resolves *if* no Signal is received.

Antipattern: Racing sleep.then

Be careful when racing a chained `sleep`.
This might cause bugs because the chained `.then` will still continue to execute.

```
await Promise.race([  
  sleep('5s').then(() => (status = 'timed_out')),  
  somethingElse.then(() => (status = 'processed')),  
]);  
  
if (status === 'processed') await complete(); // takes more than 5 seconds  
// status = timed_out
```



Updatable Timer

Here is how you can build an updatable Timer with `condition`:

```
import * as wf from '@temporalio/workflow';  
  
// usage  
export async function countdownWorkflow(): Promise<void> {  
  const target = Date.now() + 24 * 60 * 60 * 1000; // 1 day!!!  
  const timer = new UpdatableTimer(target);  
  console.log('timer set for: ' + new Date(target).toString());  
  wf.setHandler(setDeadlineSignal, (deadline) => {  
    // send in new deadlines via Signal  
    timer.deadline = deadline;  
    console.log('timer now set for: ' + new Date(deadline).toString());  
  });  
  wf.setHandler(timeLeftQuery, () => timer.deadline - Date.now());  
  await timer; // if you send in a signal with a new time, this timer will resolve earlier!  
  console.log('countdown done!');  
}
```

This is available in the third-party package [`temporal-time-utils`](https://www.npmjs.com/package/temporal-time-utils#user-content-updatabletimer), where you can also see the implementation:

```
// implementation  
export class UpdatableTimer implements PromiseLike<void> {  
  deadlineUpdated = false;  
  #deadline: number;  
  
  constructor(deadline: number) {  
    this.#deadline = deadline;  
  }  
  
  private async run(): Promise<void> {  
    /* eslint-disable no-constant-condition */  
    while (true) {  
      this.deadlineUpdated = false;  
      if (  
        !(await wf.condition(  
          () => this.deadlineUpdated,  
          this.#deadline - Date.now(),  
        ))  
      ) {  
        break;  
      }  
    }  
  }  
  
  then<TResult1 = void, TResult2 = never>(  
    onfulfilled?: (value: void) => TResult1 | PromiseLike<TResult1>,  
    onrejected?: (reason: any) => TResult2 | PromiseLike<TResult2>,  
  ): PromiseLike<TResult1 | TResult2> {  
    return this.run().then(onfulfilled, onrejected);  
  }  
  
  set deadline(value: number) {  
    this.#deadline = value;  
    this.deadlineUpdated = true;  
  }  
  
  get deadline(): number {  
    return this.#deadline;  
  }  
}
```

* [What is a Timer?](#timers)* [Asynchronous design patterns in TypeScript](#asynchronous-design-patterns)