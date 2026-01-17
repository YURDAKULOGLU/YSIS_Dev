st.login - Streamlit Docs

*star*

#### Tip

Learn more in [User authentication and information](/develop/concepts/connections/authentication).

## st.login

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Initiate the login flow for the given provider.

This command redirects the user to an OpenID Connect (OIDC) provider. After
the user authenticates their identity, they are redirected back to the
home page of your app. Streamlit stores a cookie with the user's identity
information in the user's browser . You can access the identity information
through [st.user](https://docs.streamlit.io/develop/api-reference/user/st.user). Call st.logout() to remove the cookie
and start a new session.

You can use any OIDC provider, including Google, Microsoft, Okta, and more.
You must configure the provider through secrets management. Although OIDC
is an extension of OAuth 2.0, you can't use generic OAuth providers.
Streamlit parses the user's identity token and surfaces its attributes in
st.user. If the provider returns an access token, that
token is ignored. Therefore, this command will not allow your app to act on
behalf of a user in a secure system.

For all providers, there are two shared settings, redirect\_uri and
cookie\_secret, which you must specify in an [auth] dictionary
in secrets.toml. Other settings must be defined as described in the
provider parameter.

* redirect\_uri is your app's absolute URL with the pathname
  oauth2callback. For local development using the default port, this is
  http://localhost:8501/oauth2callback.
* cookie\_secret should be a strong, randomly generated secret.

In addition to the shared settings, the following settings are required:

* client\_id
* client\_secret
* server\_metadata\_url

For a complete list of OIDC parameters, see [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest) and
your provider's documentation. By default, Streamlit sets
scope="openid profile email" and prompt="select\_account". You can
change these and other OIDC parameters by passing a dictionary of settings
to client\_kwargs. state and nonce, which are used for
security, are handled automatically and don't need to be specified. For
more information, see Example 4.

Important

* You must install Authlib>=1.3.2 to use this command. You can
  install it as an extra with Streamlit:

  ```
  pip install streamlit[auth]
  ```
* Your authentication configuration is dependent on your host location.
  When you deploy your app, remember to update your redirect\_uri
  within your app and your provider.
* All URLs declared in the settings must be absolute (i.e., begin with
  http:// or https://).
* Streamlit automatically enables CORS and XSRF protection when you
  configure authentication in secrets.toml. This takes precedence
  over configuration options in config.toml.
* If a user is logged into your app and opens a new tab in the same
  browser, they will automatically be logged in to the new session with
  the same account.
* If a user closes your app without logging out, the identity cookie
  will expire after 30 days.
* For security reasons, authentication is not supported for embedded
  apps.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/user_info.py#L54 "View st.login source code on GitHub") | |
| --- | --- |
| st.login(provider=None) | |
| Parameters | |
| provider (str or None) | The name of your provider configuration to use for login.  If provider is None (default), Streamlit will use all settings in the [auth] dictionary within your app's secrets.toml file. Otherwise, use an [auth.{provider}] dictionary for the named provider, as shown in the examples that follow. When you pass a string to provider, Streamlit will use redirect\_uri and cookie\_secret, while ignoring any other values in the [auth] dictionary.  Due to internal implementation details, Streamlit does not support using an underscore within provider at this time. |

#### Examples

**Example 1: Use an unnamed default identity provider**

If you do not specify a name for your provider, specify all settings within
the [auth] dictionary of your secrets.toml file. The following
example configures Google as the default provider. For information about
using OIDC with Google, see [Google Identity](https://developers.google.com/identity/openid-connect/openid-connect).

.streamlit/secrets.toml:

```
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "xxx"
client_id = "xxx"
client_secret = "xxx"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"  # fmt: skip
```

Your app code:

```
import streamlit as st

if not st.user.is_logged_in:
    if st.button("Log in"):
        st.login()
else:
    if st.button("Log out"):
        st.logout()
    st.write(f"Hello, {st.user.name}!")
```

**Example 2: Use a named identity provider**

If you specify a name for your provider, save the shared settings in the
[auth] dictionary of your secrets.toml file, and save the other
settings in an [auth.{provider}] dictionary, where {provider} is
the name of your provider. The following example configures Microsoft as
the provider. The example uses provider="microsoft", but you can use
any name. This name is internal to Streamlit and is used to match the login
command to its configuration. For information about using OIDC with
Microsoft, see [Microsoft Entra ID](https://learn.microsoft.com/en-us/power-pages/security/authentication/openid-settings).
To configure your {tenant} value in server\_metadata\_url, see
[Microsoft identity platform](https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc#find-your-apps-openid-configuration-document-uri).

.streamlit/secrets.toml:

```
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "xxx"

[auth.microsoft]
client_id = "xxx"
client_secret = "xxx"
server_metadata_url = "https://login.microsoftonline.com/{tenant}/v2.0/.well-known/openid-configuration"
```

Your app code:

```
import streamlit as st

if not st.user.is_logged_in:
    st.login("microsoft")
else:
    st.write(f"Hello, {st.user.name}!")
```

**Example 3: Use multiple, named providers**

If you want to give your users a choice of authentication methods,
configure multiple providers and give them each a unique name. The
following example lets users choose between Okta and Microsoft to log in.
Always check with your identity provider to understand the structure of
their identity tokens because the returned fields may differ. Remember to
set {tenant} and {subdomain} in server\_metadata\_url for
Microsoft and Okta, respectively.

```
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "xxx"

[auth.microsoft]
client_id = "xxx"
client_secret = "xxx"
server_metadata_url = "https://login.microsoftonline.com/{tenant}/v2.0/.well-known/openid-configuration"

[auth.okta]
client_id = "xxx"
client_secret = "xxx"
server_metadata_url = "https://{subdomain}.okta.com/.well-known/openid-configuration"  # fmt: skip
```

Your app code:

```
import streamlit as st

if not st.user.is_logged_in:
    st.header("Log in:")
    if st.button("Microsoft"):
        st.login("microsoft")
    if st.button("Okta"):
        st.login("okta")
else:
    if st.button("Log out"):
        st.logout()
    st.write(f"Hello, {st.user.name}!")
```

**Example 4: Change the default connection settings**

prompt="select\_account" may be treated differently by some
providers when a user is already logged into their account. If a user is
logged into their Google or Microsoft account from a previous session, the
provider will prompt them to select the account they want to use, even if
it's the only one. However, if the user is logged into their Okta or Auth0
account from a previous session, the account will automatically be
selected. st.logout() does not clear a user's related cookies. To force
users to log in every time, use prompt="login" as described in Auth0's
[Customize Signup and Login Prompts](https://auth0.com/docs/customize/login-pages/universal-login/customize-signup-and-login-prompts).

.streamlit/secrets.toml:

```
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "xxx"

[auth.auth0]
client_id = "xxx"
client_secret = "xxx"
server_metadata_url = "https://{account}.{region}.auth0.com/.well-known/openid-configuration"  # fmt: skip
client_kwargs = { "prompt" = "login" }
```

Your app code:

```
import streamlit as st

if st.button("Log in"):
    st.login("auth0")
if st.user.is_logged_in:
    if st.button("Log out"):
        st.logout()
    st.write(f"Hello, {st.user.name}!)
```

[*arrow\_back*Previous: Authentication and user info](/develop/api-reference/user)[*arrow\_forward*Next: st.logout](/develop/api-reference/user/st.logout)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI