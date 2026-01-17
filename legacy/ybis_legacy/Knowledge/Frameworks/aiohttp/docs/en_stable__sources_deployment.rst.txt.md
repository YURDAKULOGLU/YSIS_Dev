.. \_aiohttp-deployment:
=================
Server Deployment
=================
There are several options for aiohttp server deployment:
\* Standalone server
\* Running a pool of backend servers behind of :term:`nginx`, HAProxy
or other \*reverse proxy server\*
\* Using :term:`gunicorn` behind of \*reverse proxy\*
Every method has own benefits and disadvantages.
.. \_aiohttp-deployment-standalone:
Standalone
==========
Just call :func:`aiohttp.web.run\_app` function passing
:class:`aiohttp.web.Application` instance.
The method is very simple and could be the best solution in some
trivial cases. But it does not utilize all CPU cores.
For running multiple aiohttp server instances use \*reverse proxies\*.
.. \_aiohttp-deployment-nginx-supervisord:
Nginx+supervisord
=================
Running aiohttp servers behind :term:`nginx` makes several advantages.
First, nginx is the perfect frontend server. It may prevent many
attacks based on malformed http protocol etc.
Second, running several aiohttp instances behind nginx allows to
utilize all CPU cores.
Third, nginx serves static files much faster than built-in aiohttp
static file support.
But this way requires more complex configuration.
Nginx configuration
--------------------
Here is short example of an Nginx configuration file.
It does not cover all available Nginx options.
For full details, read `Nginx tutorial
`\_ and `official Nginx
documentation
`\_.
First configure HTTP server itself:
.. code-block:: nginx
http {
server {
listen 80;
client\_max\_body\_size 4G;
server\_name example.com;
location / {
proxy\_set\_header Host $http\_host;
proxy\_set\_header X-Forwarded-For $proxy\_add\_x\_forwarded\_for;
proxy\_redirect off;
proxy\_buffering off;
proxy\_pass http://aiohttp;
}
location /static {
# path for static files
root /path/to/app/static;
}
}
}
This config listens on port ``80`` for a server named ``example.com``
and redirects everything to the ``aiohttp`` backend group.
Also it serves static files from ``/path/to/app/static`` path as
``example.com/static``.
Next we need to configure \*aiohttp upstream group\*:
.. code-block:: nginx
http {
upstream aiohttp {
# fail\_timeout=0 means we always retry an upstream even if it failed
# to return a good HTTP response
# Unix domain servers
server unix:/tmp/example\_1.sock fail\_timeout=0;
server unix:/tmp/example\_2.sock fail\_timeout=0;
server unix:/tmp/example\_3.sock fail\_timeout=0;
server unix:/tmp/example\_4.sock fail\_timeout=0;
# Unix domain sockets are used in this example due to their high performance,
# but TCP/IP sockets could be used instead:
# server 127.0.0.1:8081 fail\_timeout=0;
# server 127.0.0.1:8082 fail\_timeout=0;
# server 127.0.0.1:8083 fail\_timeout=0;
# server 127.0.0.1:8084 fail\_timeout=0;
}
}
All HTTP requests for ``http://example.com`` except ones for
``http://example.com/static`` will be redirected to ``example1.sock``,
``example2.sock``, ``example3.sock`` or ``example4.sock``
backend servers. By default, Nginx uses round-robin algorithm for backend
selection.
.. note::
Nginx is not the only existing \*reverse proxy server\*, but it's the most
popular one. Alternatives like HAProxy may be used as well.
Supervisord
-----------
After configuring Nginx we need to start our aiohttp backends. It's best
to use some tool for starting them automatically after a system reboot
or backend crash.
There are many ways to do it: Supervisord, Upstart, Systemd,
Gaffer, Circus, Runit etc.
Here we'll use `Supervisord `\_ as an example:
.. code-block:: cfg
[program:aiohttp]
numprocs = 4
numprocs\_start = 1
process\_name = example\_%(process\_num)s
; Unix socket paths are specified by command line.
command=/path/to/aiohttp\_example.py --path=/tmp/example\_%(process\_num)s.sock
; We can just as easily pass TCP port numbers:
; command=/path/to/aiohttp\_example.py --port=808%(process\_num)s
user=nobody
autostart=true
autorestart=true
aiohttp server
--------------
The last step is preparing the aiohttp server to work with supervisord.
Assuming we have properly configured :class:`aiohttp.web.Application`
and port is specified by command line, the task is trivial:
.. code-block:: python3
# aiohttp\_example.py
import argparse
from aiohttp import web
parser = argparse.ArgumentParser(description="aiohttp server example")
parser.add\_argument('--path')
parser.add\_argument('--port')
if \_\_name\_\_ == '\_\_main\_\_':
app = web.Application()
# configure app
args = parser.parse\_args()
web.run\_app(app, path=args.path, port=args.port)
For real use cases we perhaps need to configure other things like
logging etc., but it's out of scope of the topic.
.. \_aiohttp-deployment-gunicorn:
Nginx+Gunicorn
==============
aiohttp can be deployed using `Gunicorn
`\_, which is based on a
pre-fork worker model. Gunicorn launches your app as worker processes
for handling incoming requests.
As opposed to deployment with :ref:`bare Nginx
`, this solution does not need to
manually run several aiohttp processes and use a tool like supervisord
to monitor them. But nothing is free: running aiohttp
application under gunicorn is slightly slower.
Prepare environment
-------------------
You first need to setup your deployment environment. This example is
based on `Ubuntu `\_ 16.04.
Create a directory for your application::
>> mkdir myapp
>> cd myapp
Create a Python virtual environment::
>> python3 -m venv venv
>> source venv/bin/activate
Now that the virtual environment is ready, we'll proceed to install
aiohttp and gunicorn::
>> pip install gunicorn
>> pip install aiohttp
Application
-----------
Lets write a simple application, which we will save to file. We'll
name this file \*my\_app\_module.py\*::
from aiohttp import web
async def index(request):
return web.Response(text="Welcome home!")
my\_web\_app = web.Application()
my\_web\_app.router.add\_get('/', index)
Application factory
-------------------
As an option an entry point could be a coroutine that accepts no
parameters and returns an application instance::
from aiohttp import web
async def index(request):
return web.Response(text="Welcome home!")
async def my\_web\_app():
app = web.Application()
app.router.add\_get('/', index)
return app
Start Gunicorn
--------------
When `Running Gunicorn
`\_, you provide the name
of the module, i.e. \*my\_app\_module\*, and the name of the app or
application factory, i.e. \*my\_web\_app\*, along with other `Gunicorn
Settings `\_ provided
as command line flags or in your config file.
In this case, we will use:
\* the ``--bind`` flag to set the server's socket address;
\* the ``--worker-class`` flag to tell Gunicorn that we want to use a
custom worker subclass instead of one of the Gunicorn default worker
types;
\* you may also want to use the ``--workers`` flag to tell Gunicorn how
many worker processes to use for handling requests. (See the
documentation for recommendations on `How Many Workers?
`\_)
\* you may also want to use the ``--accesslog`` flag to enable the access
log to be populated. (See :ref:`logging ` for more information.)
The custom worker subclass is defined in ``aiohttp.GunicornWebWorker``::
>> gunicorn my\_app\_module:my\_web\_app --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker
[2017-03-11 18:27:21 +0000] [1249] [INFO] Starting gunicorn 19.7.1
[2017-03-11 18:27:21 +0000] [1249] [INFO] Listening at: http://127.0.0.1:8080 (1249)
[2017-03-11 18:27:21 +0000] [1249] [INFO] Using worker: aiohttp.worker.GunicornWebWorker
[2015-03-11 18:27:21 +0000] [1253] [INFO] Booting worker with pid: 1253
Gunicorn is now running and ready to serve requests to your app's
worker processes.
.. note::
If you want to use an alternative asyncio event loop
`uvloop `\_, you can use the
``aiohttp.GunicornUVLoopWebWorker`` worker class.
Proxy through NGINX
----------------------
We can proxy our gunicorn workers through NGINX with a configuration like this:
.. code-block:: nginx
worker\_processes 1;
user nobody nogroup;
events {
worker\_connections 1024;
}
http {
## Main Server Block
server {
## Open by default.
listen 80 default\_server;
server\_name main;
client\_max\_body\_size 200M;
## Main site location.
location / {
proxy\_pass http://127.0.0.1:8080;
proxy\_set\_header Host $host;
proxy\_set\_header X-Forwarded-Host $server\_name;
proxy\_set\_header X-Real-IP $remote\_addr;
}
}
}
Since gunicorn listens for requests at our localhost address on port 8080, we can
use the `proxy\_pass `\_
directive to send web traffic to our workers. If everything is configured correctly,
we should reach our application at the ip address of our web server.
Proxy through NGINX + SSL
----------------------------
Here is an example NGINX configuration setup to accept SSL connections:
.. code-block:: nginx
worker\_processes 1;
user nobody nogroup;
events {
worker\_connections 1024;
}
http {
## SSL Redirect
server {
listen 80 default;
return 301 https://$host$request\_uri;
}
## Main Server Block
server {
# Open by default.
listen 443 ssl default\_server;
listen [::]:443 ssl default\_server;
server\_name main;
client\_max\_body\_size 200M;
ssl\_certificate /etc/secrets/cert.pem;
ssl\_certificate\_key /etc/secrets/key.pem;
## Main site location.
location / {
proxy\_pass http://127.0.0.1:8080;
proxy\_set\_header Host $host;
proxy\_set\_header X-Forwarded-Host $server\_name;
proxy\_set\_header X-Real-IP $remote\_addr;
}
}
}
The first server block accepts regular http connections on port 80 and redirects
them to our secure SSL connection. The second block matches our previous example
except we need to change our open port to https and specify where our SSL
certificates are being stored with the ``ssl\_certificate`` and ``ssl\_certificate\_key``
directives.
During development, you may want to `create your own self-signed certificates for testing purposes `\_
and use another service like `Let's Encrypt `\_ when you
are ready to move to production.
More information
----------------
See the `official documentation
`\_ for more
information about suggested nginx configuration. You can also find out more about
`configuring for secure https connections as well. `\_
Logging configuration
---------------------
``aiohttp`` and ``gunicorn`` use different format for specifying access log.
By default aiohttp uses own defaults::
'%a %t "%r" %s %b "%{Referer}i" "%{User-Agent}i"'
For more information please read :ref:`Format Specification for Access
Log `.
Proxy through Apache at your own risk
-------------------------------------
Issues have been reported using Apache2 in front of aiohttp server:
`#2687 Intermittent 502 proxy errors when running behind Apache `.