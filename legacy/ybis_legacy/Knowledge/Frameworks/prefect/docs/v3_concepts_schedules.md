Schedule flow runs - Prefect

[Skip to main content](#content-area)

Join us at inaugural PyAI Conf in San Francisco on March 10th! [Learn more](https://pyai.events?utm_source=docs.prefect.io)

[Prefect home page![light logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-black.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=a80a77749c9345aedc0ff328008a9625)![dark logo](https://mintcdn.com/prefect-bd373955/wj7H7r0GmwFtZG8f/logos/logo-word-white.svg?fit=max&auto=format&n=wj7H7r0GmwFtZG8f&q=85&s=78ce256196f84e2685a57efdf840d384)](https://docs.prefect.io)

Search...

⌘K

Search...

Navigation

Deployments

Schedule flow runs

[Getting Started](/v3/get-started)[Concepts](/v3/concepts)[How-to Guides](/v3/how-to-guides)[Advanced](/v3/advanced)[Examples](/v3/examples)[Integrations](/integrations/integrations)[API Reference](/v3/api-ref)[Contribute](/contribute)[Release Notes](/v3/release-notes)

* [Overview](/v3/concepts)

##### Workflows

* [Flows](/v3/concepts/flows)
* [Tasks](/v3/concepts/tasks)
* [Assets](/v3/concepts/assets)
* [Caching](/v3/concepts/caching)
* [States](/v3/concepts/states)
* [Runtime context](/v3/concepts/runtime-context)
* [Artifacts](/v3/concepts/artifacts)
* [Task runners](/v3/concepts/task-runners)
* [Global concurrency limits](/v3/concepts/global-concurrency-limits)
* [Tag-based concurrency limits](/v3/concepts/tag-based-concurrency-limits)

##### Deployments

* [Deployments](/v3/concepts/deployments)
* [Schedules](/v3/concepts/schedules)
* [Work pools](/v3/concepts/work-pools)
* [Workers](/v3/concepts/workers)

##### Configuration

* [Variables](/v3/concepts/variables)
* [Blocks](/v3/concepts/blocks)
* [Settings and profiles](/v3/concepts/settings-and-profiles)
* [Prefect server](/v3/concepts/server)

##### Automations

* [Events](/v3/concepts/events)
* [Automations](/v3/concepts/automations)
* [Event triggers](/v3/concepts/event-triggers)

##### Prefect Cloud

* [Rate limits and data retention](/v3/concepts/rate-limits)
* [SLAs](/v3/concepts/slas)
* [Webhooks](/v3/concepts/webhooks)

On this page

* [Schedule types](#schedule-types)
* [Cron](#cron)
* [How the day\_or property works](#how-the-day-or-property-works)
* [Interval](#interval)
* [RRule](#rrule)
* [How scheduling works](#how-scheduling-works)
* [Further reading](#further-reading)

Prefect allows you to specify schedules on which your flows run.
You can add one or more schedules to any deployed flow.
Schedules tell Prefect when and how to create new flow runs.
You can add a schedule to a deployed flow in the Prefect UI, in the CLI through the `prefect deployment schedule` command, or the `prefect.yaml` configuration file.

## [​](#schedule-types) Schedule types

Prefect supports three types of schedules:

* [`Cron`](#cron) is most appropriate for users who are already familiar with `cron` from previous use.
* [`Interval`](#interval) is best suited for deployments that run at some consistent cadence that isn’t related to absolute time.
* [`RRule`](#rrule) is best suited for deployments that rely on calendar logic for simple recurring schedules, irregular intervals, exclusions,
  or day-of-month adjustments.

**Schedules can be inactive**When you create or edit a schedule, you can set the `active` property to `False` in Python (or `false` in a YAML file) to
deactivate the schedule.
This is useful to keep the schedule configuration but temporarily stop the schedule from creating new flow runs.

### [​](#cron) Cron

A `Cron` schedule uses a standard [`cron`](https://en.wikipedia.org/wiki/Cron) string to define when flow runs should occur. This is ideal for schedules tied to specific clock times and dates (e.g., “every Monday at 9:00 AM”). You may also provide a timezone to enforce daylight saving time (DST) behaviors.
Prefect’s cron scheduling is based on the `croniter` library, allowing it to interpret familiar cron expressions. For example, the expression `0 9 * * MON-FRI` means “at 9:00 AM on every Monday through Friday”.

**Supported `croniter` features**While Prefect supports most features of `croniter` for creating `cron`-like schedules, it does not support “R”
random or “H” hashed keyword expressions or the schedule jittering possible with those expressions.

`Cron` properties include:

| Property | Description |
| --- | --- |
| cron | A valid `cron` string. (Required) |
| day\_or | Boolean indicating how `croniter` handles `day` and `day_of_week` entries. Default is `True`. |
| timezone | String name of a time zone. (See the [IANA Time Zone Database](https://www.iana.org/time-zones) for valid time zones.) |

#### [​](#how-the-day-or-property-works) How the `day_or` property works

The `day_or` property defaults to `True`, matching the behavior of `cron`.
In this mode, if you specify a `day` (of the month)
entry and a `day_of_week` entry, the schedule runs a flow on both the specified day of the month *and* on the specified day of the
week.
The “or” in `day_or` refers to the two entries treated like an `OR` statement. The schedule should include
both, as in the SQL statement:

Copy

```
SELECT * FROM employees WHERE first_name = 'Ford' OR last_name = 'Prefect';
```

For example, with `day_or` set to `True`, the cron schedule `* * 3 1 2` runs a flow every minute on the third day of the month
and on Tuesday (the second day of the week) in January (the first month of the year).
With `day_or` set to `False`, the `day` (of the month) and `day_of_week` entries are joined with the more restrictive `AND`
operation, as in the SQL statement:

Copy

```
SELECT * from employees WHERE first_name = 'Zaphod' AND last_name = 'Beeblebrox';
```

For example, the same schedule, when `day_or` is `False`, runs a flow on every minute on the **third Tuesday** in January.
This behavior matches `fcron` instead of `cron`.

**Daylight saving time considerations**If the `timezone` is a DST-observing one, then the schedule adjusts itself appropriately.The `cron` rules for DST are based on schedule times, not intervals. This means that an hourly `cron` schedule fires on
every new schedule hour, not every elapsed hour.
For example, when clocks are set back, this results in a two-hour pause as the schedule will fire *the first time* 1 AM is reached and *the first time* 2 AM is reached, 120 minutes later.Longer schedules, such as one that fires at 9 AM every morning, adjust for DST automatically.

### [​](#interval) Interval

As the name suggests, an `Interval` schedule is best for deployments that need to run at a consistent cadence not strictly tied to absolute clock time (e.g., “every 10 minutes” or “every 3 hours”). It creates new flow runs on a regular interval, measured in seconds, which can be anchored to a specific `anchor_date`.

Copy

```
schedule:
  interval: 600
  timezone: America/Chicago
```

`Interval` properties include:

| Property | Description |
| --- | --- |
| interval | `datetime.timedelta` indicating the time between flow runs. (Required) |
| anchor\_date | `datetime.datetime` indicating the starting or “anchor” date to begin the schedule. If no `anchor_date` is supplied, the current UTC time is used. |
| timezone | String name of a time zone, used to enforce localization behaviors like DST boundaries. (See the [IANA Time Zone Database](https://www.iana.org/time-zones) for valid time zones.) |

The `anchor_date` does not indicate a “start time” for the schedule, but a fixed point to
compute intervals.
If the anchor date is in the future, then schedule dates are computed by subtracting the `interval` from it.

**Daylight saving time considerations**If the schedule’s `anchor_date` or `timezone` are provided with a DST-observing timezone, then the schedule adjusts itself
appropriately.
Intervals greater than 24 hours will follow DST conventions, while intervals of less than 24 hours will follow UTC intervals.For example, an hourly schedule will fire every UTC hour, even across DST boundaries. When clocks are set back, this results in two runs that *appear* to be scheduled for 1 AM local time, even though they are an hour apart in UTC time.For longer intervals, like a daily schedule, the interval schedule adjusts for DST boundaries so that the clock-hour remains constant.
This means that a daily schedule that always fires at 9 AM will observe DST and continue to fire at 9 AM in the local time zone.

### [​](#rrule) RRule

For complex scheduling needs that go beyond simple cron expressions or fixed intervals, `RRule` (Recurrence Rule) is the most powerful option. It’s ideal for deployments that rely on calendar-based logic, such as “the last weekday of each month,” “every other Tuesday,” or schedules with specific exclusions.
`RRule` scheduling supports [iCal recurrence rules](https://icalendar.org/iCalendar-RFC-5545/3-8-5-3-recurrence-rule.html), providing a rich syntax for defining a wide array of repetitive schedules, from yearly down to every minute.
RRules are appropriate for any kind of calendar-date manipulation, including simple repetition, irregular intervals, exclusions,
week day or day-of-month adjustments, and more. RRules can represent complex logic like:

* The last weekday of each month
* The fourth Thursday of November
* Every other day of the week

`RRule` properties include:

| Property | Description |
| --- | --- |
| rrule | String representation of an RRule schedule. See the [`rrulestr` examples](https://dateutil.readthedocs.io/en/stable/rrule.html#rrulestr-examples) for syntax. |
| timezone | String name of a time zone. See the [IANA Time Zone Database](https://www.iana.org/time-zones) for valid time zones. |

You may find it useful to use an RRule string generator such as the [iCalendar.org RRule Tool](https://icalendar.org/rrule-tool.html) to help create valid RRules.

Copy

```
schedule:
  rrule: 'FREQ=WEEKLY;BYDAY=MO,WE,FR;UNTIL=20240730T040000Z'
```

**RRule restrictions**
The max supported character length of an `rrulestr` is 6,500 characters`COUNT` is not supported. Please use `UNTIL` or the `/deployments/{id}/runs` endpoint to schedule a fixed number of
flow runs.

**Daylight saving time considerations**As a calendar-oriented standard, `RRules` are sensitive to the initial timezone provided.
A 9 AM daily schedule with a DST-aware start date maintains a local 9 AM time through DST boundaries. A 9 AM daily schedule
with a UTC start date maintains a 9 AM UTC time.

## [​](#how-scheduling-works) How scheduling works

Prefect’s `Scheduler` service evaluates each deployment’s schedules and creates new runs appropriately. It starts
automatically when `prefect server start` is run and it is a built-in service of Prefect Cloud.
The `Scheduler` creates the fewest runs that satisfy the following constraints, in order:

* No more than 100 runs will be scheduled.
* Runs will not be scheduled more than 100 days in the future.
* At least three runs will be scheduled.
* Runs will be scheduled until at least one hour in the future.

These behaviors are adjustable through the relevant settings with the `prefect config view --show-defaults` command:

Copy

```
PREFECT_API_SERVICES_SCHEDULER_DEPLOYMENT_BATCH_SIZE='100'
PREFECT_API_SERVICES_SCHEDULER_ENABLED='True'
PREFECT_API_SERVICES_SCHEDULER_INSERT_BATCH_SIZE='500'
PREFECT_API_SERVICES_SCHEDULER_LOOP_SECONDS='60.0'
PREFECT_API_SERVICES_SCHEDULER_MIN_RUNS='3'
PREFECT_API_SERVICES_SCHEDULER_MAX_RUNS='100'
PREFECT_API_SERVICES_SCHEDULER_MIN_SCHEDULED_TIME='1:00:00'
PREFECT_API_SERVICES_SCHEDULER_MAX_SCHEDULED_TIME='100 days, 0:00:00'
```

See the [Settings docs](/v3/develop/settings-and-profiles) for more information on altering your settings.
These settings mean that if a deployment has an hourly schedule, the default settings will create runs for the next four days (or 100 hours).
If it has a weekly schedule, the default settings will maintain the next 14 runs (up to 100 days in the future).

**`Scheduler` does not affect execution**The Prefect `Scheduler` service only creates new flow runs and places them in `Scheduled` states.
It is not involved in flow or task execution.

If you change a schedule, previously scheduled flow runs that have not started are removed, and new scheduled flow runs are
created to reflect the new schedule.
To remove all scheduled runs for a flow deployment, you can remove the schedule.

## [​](#further-reading) Further reading

* [How to create schedules](/v3/how-to-guides/deployments/create-schedules)

Was this page helpful?

YesNo

[Deployments](/v3/concepts/deployments)[Work pools](/v3/concepts/work-pools)

⌘I