First steps with Django — Celery 5.6.2 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](../contributing.html "Contributing") |
* [previous](index.html "Django") |
* [Celery 5.6.2 documentation](../index.html) »
* [Django](index.html) »
* First steps with Django

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/django/first-steps-with-django.html).

# First steps with Django[¶](#first-steps-with-django "Link to this heading")

## Using Celery with Django[¶](#using-celery-with-django "Link to this heading")

Note

Previous versions of Celery required a separate library to work with Django,
but since 3.1 this is no longer the case. Django is supported out of the
box now so this document only contains a basic way to integrate Celery and
Django. You’ll use the same API as non-Django users so you’re recommended
to read the [First Steps with Celery](../getting-started/first-steps-with-celery.html#first-steps) tutorial
first and come back to this tutorial. When you have a working example you can
continue to the [Next Steps](../getting-started/next-steps.html#next-steps) guide.

Note

Celery 5.5.x supports Django 2.2 LTS or newer versions.
Please use Celery 5.2.x for versions older than Django 2.2 or Celery 4.4.x if your Django version is older than 1.11.

To use Celery with your Django project you must first define
an instance of the Celery library (called an “app”)

If you have a modern Django project layout like:

```
- proj/
  - manage.py
  - proj/
    - __init__.py
    - settings.py
    - urls.py
```

then the recommended way is to create a new proj/proj/celery.py module
that defines the Celery instance:

file:
:   proj/proj/celery.py

```
import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('proj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
```

Then you need to import this app in your `proj/proj/__init__.py`
module. This ensures that the app is loaded when Django starts
so that the `@shared_task` decorator (mentioned later) will use it:

`proj/proj/__init__.py`:

```
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)
```

Note that this example project layout is suitable for larger projects,
for simple projects you may use a single contained module that defines
both the app and tasks, like in the [First Steps with Celery](../getting-started/first-steps-with-celery.html#tut-celery) tutorial.

Let’s break down what happens in the first module,
first, we set the default [`DJANGO_SETTINGS_MODULE`](http://docs.djangoproject.com/en/dev/topics/settings/#envvar-DJANGO_SETTINGS_MODULE "(in Django v6.1)") environment
variable for the **celery** command-line program:

```
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
```

You don’t need this line, but it saves you from always passing in the
settings module to the `celery` program. It must always come before
creating the app instances, as is what we do next:

```
app = Celery('proj')
```

This is our instance of the library, you can have many instances
but there’s probably no reason for that when using Django.

We also add the Django settings module as a configuration source
for Celery. This means that you don’t have to use multiple
configuration files, and instead configure Celery directly
from the Django settings; but you can also separate them if wanted.

```
app.config_from_object('django.conf:settings', namespace='CELERY')
```

The uppercase name-space means that all
[Celery configuration options](../userguide/configuration.html#configuration)
must be specified in uppercase instead of lowercase, and start with
`CELERY_`, so for example the [`task_always_eager`](../userguide/configuration.html#std-setting-task_always_eager) setting
becomes `CELERY_TASK_ALWAYS_EAGER`, and the [`broker_url`](../userguide/configuration.html#std-setting-broker_url)
setting becomes `CELERY_BROKER_URL`. This also applies to the
workers settings, for instance, the [`worker_concurrency`](../userguide/configuration.html#std-setting-worker_concurrency)
setting becomes `CELERY_WORKER_CONCURRENCY`.

For example, a Django project’s configuration file might include:

settings.py[¶](#id1 "Link to this code")

```
...

# Celery Configuration Options
CELERY_TIMEZONE = "Australia/Tasmania"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
```

You can pass the settings object directly instead, but using a string
is better since then the worker doesn’t have to serialize the object.
The `CELERY_` namespace is also optional, but recommended (to
prevent overlap with other Django settings).

Next, a common practice for reusable apps is to define all tasks
in a separate `tasks.py` module, and Celery does have a way to
auto-discover these modules:

```
app.autodiscover_tasks()
```

With the line above Celery will automatically discover tasks from all
of your installed apps, following the `tasks.py` convention:

```
- app1/
    - tasks.py
    - models.py
- app2/
    - tasks.py
    - models.py
```

This way you don’t have to manually add the individual modules
to the [`CELERY_IMPORTS`](../userguide/configuration.html#std-setting-imports) setting.

Finally, the `debug_task` example is a task that dumps
its own request information. This is using the new `bind=True` task option
introduced in Celery 3.1 to easily refer to the current task instance.

### Using the `@shared_task` decorator[¶](#using-the-shared-task-decorator "Link to this heading")

The tasks you write will probably live in reusable apps, and reusable
apps cannot depend on the project itself, so you also cannot import your app
instance directly.

The `@shared_task` decorator lets you create tasks without having any
concrete app instance:

`demoapp/tasks.py`:

```
# Create your tasks here

from demoapp.models import Widget

from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_widgets():
    return Widget.objects.count()


@shared_task
def rename_widget(widget_id, name):
    w = Widget.objects.get(id=widget_id)
    w.name = name
    w.save()
```

See also

You can find the full source code for the Django example project at:
<https://github.com/celery/celery/tree/main/examples/django/>

### Trigger tasks at the end of the database transaction[¶](#trigger-tasks-at-the-end-of-the-database-transaction "Link to this heading")

A common pitfall with Django is triggering a task immediately and not wait until
the end of the database transaction, which means that the Celery task may run
before all changes are persisted to the database. For example:

```
# views.py
def create_user(request):
    # Note: simplified example, use a form to validate input
    user = User.objects.create(username=request.POST['username'])
    send_email.delay(user.pk)
    return HttpResponse('User created')

# task.py
@shared_task
def send_email(user_pk):
    user = User.objects.get(pk=user_pk)
    # send email ...
```

In this case, the `send_email` task could start before the view has committed
the transaction to the database, and therefore the task may not be able to find
the user.

A common solution is to use Django’s [on\_commit](https://docs.djangoproject.com/en/stable/topics/db/transactions/#django.db.transaction.on_commit) hook to trigger the task
after the transaction has been committed:

```
- send_email.delay(user.pk)
+ transaction.on_commit(lambda: send_email.delay(user.pk))
```

Added in version 5.4.

Since this is such a common pattern, Celery 5.4 introduced a handy shortcut for this,
using a [`DjangoTask`](../reference/celery.contrib.django.task.html#celery.contrib.django.task.DjangoTask "celery.contrib.django.task.DjangoTask"). Instead of calling
[`delay()`](../reference/celery.app.task.html#celery.app.task.Task.delay "celery.app.task.Task.delay"), you should call
[`delay_on_commit()`](../reference/celery.contrib.django.task.html#celery.contrib.django.task.DjangoTask.delay_on_commit "celery.contrib.django.task.DjangoTask.delay_on_commit"):

```
- send_email.delay(user.pk)
+ send_email.delay_on_commit(user.pk)
```

This API takes care of wrapping the call into the [on\_commit](https://docs.djangoproject.com/en/stable/topics/db/transactions/#django.db.transaction.on_commit) hook for you.
In rare cases where you want to trigger a task without waiting, the existing
[`delay()`](../reference/celery.app.task.html#celery.app.task.Task.delay "celery.app.task.Task.delay") API is still available.

One key difference compared to the `delay` method, is that `delay_on_commit`
will NOT return the task ID back to the caller. The task is not sent to the broker
when you call the method, only when the Django transaction finishes. If you need the
task ID, best to stick to [`delay()`](../reference/celery.app.task.html#celery.app.task.Task.delay "celery.app.task.Task.delay").

This task class should be used automatically if you’ve follow the setup steps above.
However, if your app [uses a custom task base class](../userguide/tasks.html#task-custom-classes),
you’ll need inherit from [`DjangoTask`](../reference/celery.contrib.django.task.html#celery.contrib.django.task.DjangoTask "celery.contrib.django.task.DjangoTask") instead of
[`Task`](../reference/celery.app.task.html#celery.app.task.Task "celery.app.task.Task") to get this behaviour.

### Django Connection pool[¶](#django-connection-pool "Link to this heading")

From Django 5.1+ there is built-in support for database connection pooling.
If you enable it in Django `DATABASES` settings Celery will automatically
handle connection pool closing in worker processes via `close_pool`
database backend method as
[sharing connections across processes is not possible.](https://github.com/psycopg/psycopg/issues/544#issuecomment-1500886864)

You can find more about Connection pool at [Django docs.](https://docs.djangoproject.com/en/dev/ref/databases/#connection-pool)

## Extensions[¶](#extensions "Link to this heading")

### `django-celery-results` - Using the Django ORM/Cache as a result backend[¶](#django-celery-results-using-the-django-orm-cache-as-a-result-backend "Link to this heading")

The <https://pypi.org/project/django-celery-results/> extension provides result backends
using either the Django ORM, or the Django Cache framework.

To use this with your project you need to follow these steps:

1. Install the <https://pypi.org/project/django-celery-results/> library:

   > ```
   > $ pip install django-celery-results
   > ```
2. Add `django_celery_results` to `INSTALLED_APPS` in your
   Django project’s `settings.py`:

   ```
   INSTALLED_APPS = (
       ...,
       'django_celery_results',
   )
   ```

   Note that there is no dash in the module name, only underscores.
3. Create the Celery database tables by performing a database migrations:

   > ```
   > $ python manage.py migrate django_celery_results
   > ```
4. Configure Celery to use the <https://pypi.org/project/django-celery-results/> backend.

   > Assuming you are using Django’s `settings.py` to also configure
   > Celery, add the following settings:
   >
   > ```
   > CELERY_RESULT_BACKEND = 'django-db'
   > ```
   >
   > When using the cache backend, you can specify a cache defined within
   > Django’s CACHES setting.
   >
   > ```
   > CELERY_RESULT_BACKEND = 'django-cache'
   >
   > # pick which cache from the CACHES setting.
   > CELERY_CACHE_BACKEND = 'default'
   >
   > # django setting.
   > CACHES = {
   >     'default': {
   >         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
   >         'LOCATION': 'my_cache_table',
   >     }
   > }
   > ```
   >
   > For additional configuration options, view the
   > [Task result backend settings](../userguide/configuration.html#conf-result-backend) reference.

### `django-celery-beat` - Database-backed Periodic Tasks with Admin interface.[¶](#django-celery-beat-database-backed-periodic-tasks-with-admin-interface "Link to this heading")

See [Using custom scheduler classes](../userguide/periodic-tasks.html#beat-custom-schedulers) for more information.

## Starting the worker process[¶](#starting-the-worker-process "Link to this heading")

In a production environment you’ll want to run the worker in the background
as a daemon - see [Daemonization](../userguide/daemonizing.html#daemonizing) - but for testing and
development it is useful to be able to start a worker instance by using the
**celery worker** manage command, much as you’d use Django’s
**manage.py runserver**:

```
$ celery -A proj worker -l INFO
```

For a complete listing of the command-line options available,
use the help command:

```
$ celery --help
```

## Where to go from here[¶](#where-to-go-from-here "Link to this heading")

If you want to learn more you should continue to the
[Next Steps](../getting-started/next-steps.html#next-steps) tutorial, and after that you
can study the [User Guide](../userguide/index.html#guide).

[![Logo of Celery](../_static/celery_512.png)](../index.html)

### Donations

Please help support this community project with a donation.

[![](https://opencollective.com/celery/donate/button@2x.png?color=blue)](https://opencollective.com/celery/donate)

#### Previous topic

[Django](index.html "previous chapter")

#### Next topic

[Contributing](../contributing.html "next chapter")

### This Page

* [Show Source](../_sources/django/first-steps-with-django.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](../contributing.html "Contributing") |
* [previous](index.html "Django") |
* [Celery 5.6.2 documentation](../index.html) »
* [Django](index.html) »
* First steps with Django

© [Copyright](../copyright.html) 2009-2023, Ask Solem & contributors.