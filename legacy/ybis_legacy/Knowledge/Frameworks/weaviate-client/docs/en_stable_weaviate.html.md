weaviate — Weaviate Python Client 4.19.2 documentation



* [Weaviate Library](modules.html)
* weaviate
* [View page source](_sources/weaviate.rst.txt)

---

# weaviate[](#module-weaviate "Link to this heading")

Weaviate Python Client Library used to interact with a Weaviate instance.

*class* weaviate.WeaviateClient(*connection\_params=None*, *embedded\_options=None*, *auth\_client\_secret=None*, *additional\_headers=None*, *additional\_config=None*, *skip\_init\_checks=False*)[[source]](_modules/weaviate/client.html#WeaviateClient)[](#weaviate.WeaviateClient "Link to this definition")
:   The v4 Python-native Weaviate Client class that encapsulates Weaviate functionalities in one object.

    WARNING: This client is only compatible with Weaviate v1.23.6 and higher!

    A Client instance creates all the needed objects to interact with Weaviate, and connects all of
    them to the same Weaviate instance. See below the Attributes of the Client instance. For the
    per attribute functionality see that attribute’s documentation.

    backup[](#weaviate.WeaviateClient.backup "Link to this definition")
    :   Backup object instance connected to the same Weaviate instance as the Client.
        This namespace contains all the functionality to upload data in batches to Weaviate for all collections and tenants.

        Type:
        :   [\_Backup](weaviate.backup.html#weaviate.backup._Backup "weaviate.backup._Backup")

    batch[](#weaviate.WeaviateClient.batch "Link to this definition")
    :   BatchClient object instance connected to the same Weaviate instance as the Client.
        This namespace contains all functionality to backup data.

        Type:
        :   [\_BatchClientWrapper](weaviate.collections.batch.html#weaviate.collections.batch.client._BatchClientWrapper "weaviate.collections.batch.client._BatchClientWrapper")

    cluster[](#weaviate.WeaviateClient.cluster "Link to this definition")
    :   Cluster object instance connected to the same Weaviate instance as the Client.
        This namespace contains all functionality to inspect the connected Weaviate cluster.

        Type:
        :   [\_Cluster](weaviate.cluster.html#weaviate.cluster._Cluster "weaviate.cluster._Cluster")

    collections[](#weaviate.WeaviateClient.collections "Link to this definition")
    :   Collections object instance connected to the same Weaviate instance as the Client.
        This namespace contains all the functionality to manage Weaviate data collections. It is your main entry point for all
        collection-related functionality. Use it to retrieve collection objects using client.collections.get(“MyCollection”)
        or to create new collections using client.collections.create(“MyCollection”, …).

        Type:
        :   [\_Collections](weaviate.collections.collections.html#weaviate.collections.collections._Collections "weaviate.collections.collections._Collections")

    debug[](#weaviate.WeaviateClient.debug "Link to this definition")
    :   Debug object instance connected to the same Weaviate instance as the Client.
        This namespace contains functionality used to debug Weaviate clusters. As such, it is deemed experimental and is subject to change.
        We can make no guarantees about the stability of this namespace nor the potential for future breaking changes. Use at your own risk.

        Type:
        :   [\_Debug](weaviate.debug.html#weaviate.debug._Debug "weaviate.debug._Debug")

    roles[](#weaviate.WeaviateClient.roles "Link to this definition")
    :   Roles object instance connected to the same Weaviate instance as the Client.
        This namespace contains all functionality to manage Weaviate’s RBAC functionality.

        Type:
        :   [\_Roles](weaviate.rbac.html#weaviate.rbac._Roles "weaviate.rbac._Roles")

    users[](#weaviate.WeaviateClient.users "Link to this definition")
    :   Users object instance connected to the same Weaviate instance as the Client.
        This namespace contains all functionality to manage Weaviate users.

        Type:
        :   [\_Users](weaviate.users.html#weaviate.users._Users "weaviate.users._Users")

    Initialise a WeaviateClient class instance to use when interacting with Weaviate.

    Use this specific initializer when you want to create a custom Client specific to your Weaviate setup.

    To simplify connections to Weaviate Cloud or local instances, use the [`weaviate.connect_to_weaviate_cloud()`](#weaviate.connect_to_weaviate_cloud "weaviate.connect_to_weaviate_cloud")
    or [`weaviate.connect_to_local()`](#weaviate.connect_to_local "weaviate.connect_to_local") helper functions.

    Parameters:
    :   * **connection\_params** ([*ConnectionParams*](weaviate.connect.html#weaviate.connect.ConnectionParams "weaviate.connect.base.ConnectionParams") *|* *None*) – The connection parameters to use for the underlying HTTP requests.
        * **embedded\_options** ([*EmbeddedOptions*](#weaviate.embedded.EmbeddedOptions "weaviate.embedded.EmbeddedOptions") *|* *None*) – The options to use when provisioning an embedded Weaviate instance.
        * **auth\_client\_secret** ([*\_BearerToken*](#weaviate.auth._BearerToken "weaviate.auth._BearerToken") *|* [*\_ClientPassword*](#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword") *|* [*\_ClientCredentials*](#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials") *|* [*\_APIKey*](#weaviate.auth._APIKey "weaviate.auth._APIKey") *|* *None*) – Authenticate to weaviate by using one of the given authentication modes:
          - weaviate.auth.AuthBearerToken to use existing access and (optionally, but recommended) refresh tokens
          - weaviate.auth.AuthClientPassword to use username and password for oidc Resource Owner Password flow
          - weaviate.auth.AuthClientCredentials to use a client secret for oidc client credential flow
        * **additional\_headers** (*dict* *|* *None*) – Additional headers to include in the requests. Can be used to set OpenAI/HuggingFace/Cohere etc. keys.
          [Here](https://weaviate.io/developers/weaviate/modules/reader-generator-modules/generative-openai#providing-the-key-to-weaviate) is an
          example of how to set API keys within this parameter.
        * **additional\_config** ([*AdditionalConfig*](#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") *|* *None*) – Additional and advanced configuration options for Weaviate.
        * **skip\_init\_checks** (*bool*) – If set to True then the client will not perform any checks including ensuring that weaviate has started.
          This is useful for air-gapped environments and high-performance setups.

    close()[](#weaviate.WeaviateClient.close "Link to this definition")
    :   In order to clean up any resources used by the client, call this method when you are done with it.

        If you do not do this, memory leaks may occur due to stale connections.
        This method also closes the embedded database if one was started.

        Return type:
        :   None | *Awaitable*[None]

    connect()[](#weaviate.WeaviateClient.connect "Link to this definition")
    :   Connect to the Weaviate instance performing all the necessary checks.

        If you have specified skip\_init\_checks in the constructor then this method will not perform any runtime checks
        to ensure that Weaviate is running and ready to accept requests. This is useful for air-gapped environments and high-performance setups.

        This method is idempotent and will only perform the checks once. Any subsequent calls do nothing while client.is\_connected() == True.

        Raises:
        :   * [**WeaviateConnectionError**](weaviate.exceptions.html#weaviate.exceptions.WeaviateConnectionError "weaviate.exceptions.WeaviateConnectionError") – If the network connection to weaviate fails.
            * [**UnexpectedStatusCodeError**](weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError") – If weaviate reports a none OK status.

        Return type:
        :   None | *Awaitable*[None]

    get\_meta()[](#weaviate.WeaviateClient.get_meta "Link to this definition")
    :   Get the meta endpoint description of weaviate.

        Returns:
        :   The dict describing the weaviate configuration.

        Raises:
        :   [**UnexpectedStatusCodeError**](weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError") – If Weaviate reports a none OK status.

        Return type:
        :   dict | *Awaitable*[dict]

    get\_open\_id\_configuration()[](#weaviate.WeaviateClient.get_open_id_configuration "Link to this definition")
    :   Get the openid-configuration.

        Returns:
        :   The configuration or None if not configured.

        Raises:
        :   [**UnexpectedStatusCodeError**](weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError") – If Weaviate reports a none OK status.

        Return type:
        :   *Dict*[str, *Any*] | None | *Awaitable*[*Dict*[str, *Any*] | None]

    graphql\_raw\_query(*gql\_query*)[](#weaviate.WeaviateClient.graphql_raw_query "Link to this definition")
    :   Allows to send graphQL string queries, this should only be used for weaviate-features that are not yet supported.

        Be cautious of injection risks when generating query strings.

        Parameters:
        :   **gql\_query** (*str*) – GraphQL query as a string.

        Returns:
        :   A dict with the response from the GraphQL query.

        Raises:
        :   * **TypeError** – If gql\_query is not of type str.
            * [**WeaviateConnectionError**](weaviate.exceptions.html#weaviate.exceptions.WeaviateConnectionError "weaviate.exceptions.WeaviateConnectionError") – If the network connection to weaviate fails.
            * [**UnexpectedStatusCodeError**](weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError") – If weaviate reports a none OK status.

        Return type:
        :   [*\_RawGQLReturn*](weaviate.collections.classes.html#weaviate.collections.classes.internal._RawGQLReturn "weaviate.collections.classes.internal._RawGQLReturn") | *Awaitable*[[*\_RawGQLReturn*](weaviate.collections.classes.html#weaviate.collections.classes.internal._RawGQLReturn "weaviate.collections.classes.internal._RawGQLReturn")]

    is\_connected()[](#weaviate.WeaviateClient.is_connected "Link to this definition")
    :   Check if the client is connected to Weaviate.

        Returns:
        :   True if the client is connected to Weaviate with an open connection pool, False otherwise.

        Return type:
        :   bool

    is\_live()[](#weaviate.WeaviateClient.is_live "Link to this definition")
    :   Return type:
        :   bool | *Awaitable*[bool]

    is\_ready()[](#weaviate.WeaviateClient.is_ready "Link to this definition")
    :   Return type:
        :   bool | *Awaitable*[bool]

*class* weaviate.WeaviateAsyncClient(*connection\_params=None*, *embedded\_options=None*, *auth\_client\_secret=None*, *additional\_headers=None*, *additional\_config=None*, *skip\_init\_checks=False*)[[source]](_modules/weaviate/client.html#WeaviateAsyncClient)[](#weaviate.WeaviateAsyncClient "Link to this definition")
:   The v4 Python-native Weaviate Client class that encapsulates Weaviate functionalities in one object.

    WARNING: This client is only compatible with Weaviate v1.23.6 and higher!

    A Client instance creates all the needed objects to interact with Weaviate, and connects all of
    them to the same Weaviate instance. See below the Attributes of the Client instance. For the
    per attribute functionality see that attribute’s documentation.

    backup[](#weaviate.WeaviateAsyncClient.backup "Link to this definition")
    :   Backup object instance connected to the same Weaviate instance as the Client.
        This namespace contains all the functionality to upload data in batches to Weaviate for all collections and tenants.

        Type:
        :   [\_BackupAsync](weaviate.backup.html#weaviate.backup._BackupAsync "weaviate.backup._BackupAsync")

    cluster[](#weaviate.WeaviateAsyncClient.cluster "Link to this definition")
    :   Cluster object instance connected to the same Weaviate instance as the Client.
        This namespace contains all functionality to inspect the connected Weaviate cluster.

        Type:
        :   [\_ClusterAsync](weaviate.cluster.html#weaviate.cluster._ClusterAsync "weaviate.cluster._ClusterAsync")

    collections[](#weaviate.WeaviateAsyncClient.collections "Link to this definition")
    :   Collections object instance connected to the same Weaviate instance as the Client.
        This namespace contains all the functionality to manage Weaviate data collections. It is your main entry point for all
        collection-related functionality. Use it to retrieve collection objects using client.collections.get(“MyCollection”)
        or to create new collections using client.collections.create(“MyCollection”, …).

        Type:
        :   [\_CollectionsAsync](weaviate.collections.collections.html#weaviate.collections.collections._CollectionsAsync "weaviate.collections.collections._CollectionsAsync")

    debug[](#weaviate.WeaviateAsyncClient.debug "Link to this definition")
    :   Debug object instance connected to the same Weaviate instance as the Client.
        This namespace contains functionality used to debug Weaviate clusters. As such, it is deemed experimental and is subject to change.
        We can make no guarantees about the stability of this namespace nor the potential for future breaking changes. Use at your own risk.

        Type:
        :   [\_DebugAsync](weaviate.debug.html#weaviate.debug._DebugAsync "weaviate.debug._DebugAsync")

    roles[](#weaviate.WeaviateAsyncClient.roles "Link to this definition")
    :   Roles object instance connected to the same Weaviate instance as the Client.
        This namespace contains all functionality to manage Weaviate’s RBAC functionality.

        Type:
        :   [\_RolesAsync](weaviate.rbac.html#weaviate.rbac._RolesAsync "weaviate.rbac._RolesAsync")

    users[](#weaviate.WeaviateAsyncClient.users "Link to this definition")
    :   Users object instance connected to the same Weaviate instance as the Client.
        This namespace contains all functionality to manage Weaviate users.

        Type:
        :   [\_UsersAsync](weaviate.users.html#weaviate.users._UsersAsync "weaviate.users._UsersAsync")

    Initialise a WeaviateAsyncClient class instance to use when interacting with Weaviate.

    Use this specific initializer when you want to create a custom Client specific to your Weaviate setup.

    To simplify connections to Weaviate Cloud or local instances, use the [`weaviate.use_async_with_weaviate_cloud()`](#weaviate.use_async_with_weaviate_cloud "weaviate.use_async_with_weaviate_cloud")
    or [`weaviate.use_async_with_local()`](#weaviate.use_async_with_local "weaviate.use_async_with_local") helper functions.

    Parameters:
    :   * **connection\_params** ([*ConnectionParams*](weaviate.connect.html#weaviate.connect.ConnectionParams "weaviate.connect.base.ConnectionParams") *|* *None*) – The connection parameters to use for the underlying HTTP requests.
        * **embedded\_options** ([*EmbeddedOptions*](#weaviate.embedded.EmbeddedOptions "weaviate.embedded.EmbeddedOptions") *|* *None*) – The options to use when provisioning an embedded Weaviate instance.
        * **auth\_client\_secret** ([*\_BearerToken*](#weaviate.auth._BearerToken "weaviate.auth._BearerToken") *|* [*\_ClientPassword*](#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword") *|* [*\_ClientCredentials*](#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials") *|* [*\_APIKey*](#weaviate.auth._APIKey "weaviate.auth._APIKey") *|* *None*) – Authenticate to weaviate by using one of the given authentication modes:
          - weaviate.auth.AuthBearerToken to use existing access and (optionally, but recommended) refresh tokens
          - weaviate.auth.AuthClientPassword to use username and password for oidc Resource Owner Password flow
          - weaviate.auth.AuthClientCredentials to use a client secret for oidc client credential flow
        * **additional\_headers** (*dict* *|* *None*) –

          Additional headers to include in the requests. Can be used to set OpenAI/HuggingFace/Cohere etc. keys.
          [Here](https://weaviate.io/developers/weaviate/modules/reader-generator-modules/generative-openai#providing-the-key-to-weaviate) is an
          example of how to set API keys within this parameter.
        * **additional\_config** ([*AdditionalConfig*](#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") *|* *None*) – Additional and advanced configuration options for Weaviate.
        * **skip\_init\_checks** (*bool*) – If set to True then the client will not perform any checks including ensuring that weaviate has started.
          This is useful for air-gapped environments and high-performance setups.

    close()[](#weaviate.WeaviateAsyncClient.close "Link to this definition")
    :   In order to clean up any resources used by the client, call this method when you are done with it.

        If you do not do this, memory leaks may occur due to stale connections.
        This method also closes the embedded database if one was started.

        Return type:
        :   None | *Awaitable*[None]

    connect()[](#weaviate.WeaviateAsyncClient.connect "Link to this definition")
    :   Connect to the Weaviate instance performing all the necessary checks.

        If you have specified skip\_init\_checks in the constructor then this method will not perform any runtime checks
        to ensure that Weaviate is running and ready to accept requests. This is useful for air-gapped environments and high-performance setups.

        This method is idempotent and will only perform the checks once. Any subsequent calls do nothing while client.is\_connected() == True.

        Raises:
        :   * [**WeaviateConnectionError**](weaviate.exceptions.html#weaviate.exceptions.WeaviateConnectionError "weaviate.exceptions.WeaviateConnectionError") – If the network connection to weaviate fails.
            * [**UnexpectedStatusCodeError**](weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError") – If weaviate reports a none OK status.

        Return type:
        :   None | *Awaitable*[None]

    get\_meta()[](#weaviate.WeaviateAsyncClient.get_meta "Link to this definition")
    :   Get the meta endpoint description of weaviate.

        Returns:
        :   The dict describing the weaviate configuration.

        Raises:
        :   [**UnexpectedStatusCodeError**](weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError") – If Weaviate reports a none OK status.

        Return type:
        :   dict | *Awaitable*[dict]

    get\_open\_id\_configuration()[](#weaviate.WeaviateAsyncClient.get_open_id_configuration "Link to this definition")
    :   Get the openid-configuration.

        Returns:
        :   The configuration or None if not configured.

        Raises:
        :   [**UnexpectedStatusCodeError**](weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError") – If Weaviate reports a none OK status.

        Return type:
        :   *Dict*[str, *Any*] | None | *Awaitable*[*Dict*[str, *Any*] | None]

    graphql\_raw\_query(*gql\_query*)[](#weaviate.WeaviateAsyncClient.graphql_raw_query "Link to this definition")
    :   Allows to send graphQL string queries, this should only be used for weaviate-features that are not yet supported.

        Be cautious of injection risks when generating query strings.

        Parameters:
        :   **gql\_query** (*str*) – GraphQL query as a string.

        Returns:
        :   A dict with the response from the GraphQL query.

        Raises:
        :   * **TypeError** – If gql\_query is not of type str.
            * [**WeaviateConnectionError**](weaviate.exceptions.html#weaviate.exceptions.WeaviateConnectionError "weaviate.exceptions.WeaviateConnectionError") – If the network connection to weaviate fails.
            * [**UnexpectedStatusCodeError**](weaviate.exceptions.html#weaviate.exceptions.UnexpectedStatusCodeError "weaviate.exceptions.UnexpectedStatusCodeError") – If weaviate reports a none OK status.

        Return type:
        :   [*\_RawGQLReturn*](weaviate.collections.classes.html#weaviate.collections.classes.internal._RawGQLReturn "weaviate.collections.classes.internal._RawGQLReturn") | *Awaitable*[[*\_RawGQLReturn*](weaviate.collections.classes.html#weaviate.collections.classes.internal._RawGQLReturn "weaviate.collections.classes.internal._RawGQLReturn")]

    is\_connected()[](#weaviate.WeaviateAsyncClient.is_connected "Link to this definition")
    :   Check if the client is connected to Weaviate.

        Returns:
        :   True if the client is connected to Weaviate with an open connection pool, False otherwise.

        Return type:
        :   bool

    is\_live()[](#weaviate.WeaviateAsyncClient.is_live "Link to this definition")
    :   Return type:
        :   bool | *Awaitable*[bool]

    is\_ready()[](#weaviate.WeaviateAsyncClient.is_ready "Link to this definition")
    :   Return type:
        :   bool | *Awaitable*[bool]

weaviate.connect\_to\_custom(*http\_host*, *http\_port*, *http\_secure*, *grpc\_host*, *grpc\_port*, *grpc\_secure*, *headers=None*, *additional\_config=None*, *auth\_credentials=None*, *skip\_init\_checks=False*)[[source]](_modules/weaviate/connect/helpers.html#connect_to_custom)[](#weaviate.connect_to_custom "Link to this definition")
:   Connect to a Weaviate instance with custom connection parameters.

    If this is not sufficient for your customization needs then instantiate a weaviate.WeaviateClient instance directly.

    This method handles automatically connecting to Weaviate but not automatically closing the connection. Once you are done with the client
    you should call client.close() to close the connection and free up resources. Alternatively, you can use the client as a context manager
    in a with statement, which will automatically close the connection when the context is exited. See the examples below for details.

    Parameters:
    :   * **http\_host** (*str*) – The host to use for the underlying REST and GraphQL API calls.
        * **http\_port** (*int*) – The port to use for the underlying REST and GraphQL API calls.
        * **http\_secure** (*bool*) – Whether to use https for the underlying REST and GraphQL API calls.
        * **grpc\_host** (*str*) – The host to use for the underlying gRPC API.
        * **grpc\_port** (*int*) – The port to use for the underlying gRPC API.
        * **grpc\_secure** (*bool*) – Whether to use a secure channel for the underlying gRPC API.
        * **headers** (*Dict**[**str**,* *str**]* *|* *None*) – Additional headers to include in the requests, e.g. API keys for Cloud vectorization.
        * **additional\_config** ([*AdditionalConfig*](#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") *|* *None*) – This includes many additional, rarely used config options. use wvc.init.AdditionalConfig() to configure.
        * **auth\_credentials** ([*\_BearerToken*](#weaviate.auth._BearerToken "weaviate.auth._BearerToken") *|* [*\_ClientPassword*](#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword") *|* [*\_ClientCredentials*](#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials") *|* [*\_APIKey*](#weaviate.auth._APIKey "weaviate.auth._APIKey") *|* *None*) – The credentials to use for authentication with your Weaviate instance. This can be an API key, in which case pass a string or use weaviate.classes.init.Auth.api\_key(),
          a bearer token, in which case use weaviate.classes.init.Auth.bearer\_token(), a client secret, in which case use weaviate.classes.init.Auth.client\_credentials()
          or a username and password, in which case use weaviate.classes.init.Auth.client\_password().
        * **skip\_init\_checks** (*bool*) – Whether to skip the initialization checks when connecting to Weaviate.

    Returns:
    :   The client connected to the instance with the required parameters set appropriately.

    Return type:
    :   [*WeaviateClient*](#weaviate.WeaviateClient "weaviate.client.WeaviateClient")

    Examples

    ```
    >>> ################## Without Context Manager #############################
    >>> import weaviate
    >>> client = weaviate.connect_to_custom(
    ...     http_host="localhost",
    ...     http_port=8080,
    ...     http_secure=False,
    ...     grpc_host="localhost",
    ...     grpc_port=50051,
    ...     grpc_secure=False,
    ... )
    >>> client.is_ready()
    True
    >>> client.close() # Close the connection when you are done with it.
    >>> ################## With Context Manager #############################
    >>> import weaviate
    >>> with weaviate.connect_to_custom(
    ...     http_host="localhost",
    ...     http_port=8080,
    ...     http_secure=False,
    ...     grpc_host="localhost",
    ...     grpc_port=50051,
    ...     grpc_secure=False,
    ... ) as client:
    ...     client.is_ready()
    True
    >>> # The connection is automatically closed when the context is exited.
    ```

weaviate.connect\_to\_embedded(*hostname='127.0.0.1'*, *port=8079*, *grpc\_port=50050*, *headers=None*, *additional\_config=None*, *version='1.30.5'*, *persistence\_data\_path=None*, *binary\_path=None*, *environment\_variables=None*)[[source]](_modules/weaviate/connect/helpers.html#connect_to_embedded)[](#weaviate.connect_to_embedded "Link to this definition")
:   Connect to an embedded Weaviate instance.

    This method handles automatically connecting to Weaviate but not automatically closing the connection. Once you are done with the client
    you should call client.close() to close the connection and free up resources. Alternatively, you can use the client as a context manager
    in a with statement, which will automatically close the connection when the context is exited. See the examples below for details.

    See [the docs](https://weaviate.io/developers/weaviate/installation/embedded#embedded-options) for more details.

    Parameters:
    :   * **hostname** (*str*) – The hostname to use for the underlying REST & GraphQL API calls.
        * **port** (*int*) – The port to use for the underlying REST and GraphQL API calls.
        * **grpc\_port** (*int*) – The port to use for the underlying gRPC API.
        * **headers** (*Dict**[**str**,* *str**]* *|* *None*) – Additional headers to include in the requests, e.g. API keys for Cloud vectorization.
        * **additional\_config** ([*AdditionalConfig*](#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") *|* *None*) – This includes many additional, rarely used config options. use wvc.init.AdditionalConfig() to configure.
        * **version** (*str*) – Weaviate version to be used for the embedded instance.
        * **persistence\_data\_path** (*str* *|* *None*) – Directory where the files making up the database are stored.
          When the XDG\_DATA\_HOME env variable is set, the default value is: XDG\_DATA\_HOME/weaviate/
          Otherwise it is: ~/.local/share/weaviate
        * **binary\_path** (*str* *|* *None*) – Directory where to download the binary. If deleted, the client will download the binary again.
          When the XDG\_CACHE\_HOME env variable is set, the default value is: XDG\_CACHE\_HOME/weaviate-embedded/
          Otherwise it is: ~/.cache/weaviate-embedded
        * **environment\_variables** (*Dict**[**str**,* *str**]* *|* *None*) – Additional environment variables to be passed to the embedded instance for configuration.

    Returns:
    :   The client connected to the embedded instance with the required parameters set appropriately.

    Return type:
    :   [*WeaviateClient*](#weaviate.WeaviateClient "weaviate.client.WeaviateClient")

    Examples

    ```
    >>> import weaviate
    >>> client = weaviate.connect_to_embedded(
    ...     port=8080,
    ...     grpc_port=50051,
    ... )
    >>> client.is_ready()
    True
    >>> client.close() # Close the connection when you are done with it.
    ################## With Context Manager #############################
    >>> import weaviate
    >>> with weaviate.connect_to_embedded(
    ...     port=8080,
    ...     grpc_port=50051,
    ... ) as client:
    ...     client.is_ready()
    True
    >>> # The connection is automatically closed when the context is exited.
    ```

weaviate.connect\_to\_local(*host='localhost'*, *port=8080*, *grpc\_port=50051*, *headers=None*, *additional\_config=None*, *skip\_init\_checks=False*, *auth\_credentials=None*)[[source]](_modules/weaviate/connect/helpers.html#connect_to_local)[](#weaviate.connect_to_local "Link to this definition")
:   Connect to a local Weaviate instance deployed using Docker compose with standard port configurations.

    This method handles automatically connecting to Weaviate but not automatically closing the connection. Once you are done with the client
    you should call client.close() to close the connection and free up resources. Alternatively, you can use the client as a context manager
    in a with statement, which will automatically close the connection when the context is exited. See the examples below for details.

    Parameters:
    :   * **host** (*str*) – The host to use for the underlying REST and GraphQL API calls.
        * **port** (*int*) – The port to use for the underlying REST and GraphQL API calls.
        * **grpc\_port** (*int*) – The port to use for the underlying gRPC API.
        * **headers** (*Dict**[**str**,* *str**]* *|* *None*) – Additional headers to include in the requests, e.g. API keys for Cloud vectorization.
        * **additional\_config** ([*AdditionalConfig*](#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") *|* *None*) – This includes many additional, rarely used config options. use wvc.init.AdditionalConfig() to configure.
        * **skip\_init\_checks** (*bool*) – Whether to skip the initialization checks when connecting to Weaviate.
        * **auth\_credentials** (*str* *|* [*\_BearerToken*](#weaviate.auth._BearerToken "weaviate.auth._BearerToken") *|* [*\_ClientPassword*](#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword") *|* [*\_ClientCredentials*](#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials") *|* [*\_APIKey*](#weaviate.auth._APIKey "weaviate.auth._APIKey") *|* *None*) – The credentials to use for authentication with your Weaviate instance. This can be an API key, in which case pass a string or use weaviate.classes.init.Auth.api\_key(),
          a bearer token, in which case use weaviate.classes.init.Auth.bearer\_token(), a client secret, in which case use weaviate.classes.init.Auth.client\_credentials()
          or a username and password, in which case use weaviate.classes.init.Auth.client\_password().

    Return type:
    :   The client connected to the local instance with default parameters set as

    Examples

    ```
    >>> ################## Without Context Manager #############################
    >>> import weaviate
    >>> client = weaviate.connect_to_local(
    ...     host="localhost",
    ...     port=8080,
    ...     grpc_port=50051,
    ... )
    >>> client.is_ready()
    True
    >>> client.close() # Close the connection when you are done with it.
    >>> ################## With Context Manager #############################
    >>> import weaviate
    >>> with weaviate.connect_to_local(
    ...     host="localhost",
    ...     port=8080,
    ...     grpc_port=50051,
    ... ) as client:
    ...     client.is_ready()
    True
    >>> # The connection is automatically closed when the context is exited.
    ```

weaviate.connect\_to\_wcs(*cluster\_url*, *auth\_credentials*, *headers=None*, *additional\_config=None*, *skip\_init\_checks=False*)[[source]](_modules/weaviate/connect/helpers.html#connect_to_wcs)[](#weaviate.connect_to_wcs "Link to this definition")
:   Deprecated since version 4.6.2.

    This method is deprecated and will be removed in a future release. Use [`connect_to_weaviate_cloud()`](#weaviate.connect_to_weaviate_cloud "weaviate.connect_to_weaviate_cloud") instead.

    Parameters:
    :   * **cluster\_url** (*str*)
        * **auth\_credentials** (*str* *|* [*\_BearerToken*](#weaviate.auth._BearerToken "weaviate.auth._BearerToken") *|* [*\_ClientPassword*](#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword") *|* [*\_ClientCredentials*](#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials") *|* [*\_APIKey*](#weaviate.auth._APIKey "weaviate.auth._APIKey"))
        * **headers** (*Dict**[**str**,* *str**]* *|* *None*)
        * **additional\_config** ([*AdditionalConfig*](#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") *|* *None*)
        * **skip\_init\_checks** (*bool*)

    Return type:
    :   [*WeaviateClient*](#weaviate.WeaviateClient "weaviate.client.WeaviateClient")

weaviate.connect\_to\_weaviate\_cloud(*cluster\_url*, *auth\_credentials*, *headers=None*, *additional\_config=None*, *skip\_init\_checks=False*)[[source]](_modules/weaviate/connect/helpers.html#connect_to_weaviate_cloud)[](#weaviate.connect_to_weaviate_cloud "Link to this definition")
:   Connect to a Weaviate Cloud (WCD) instance.

    This method handles automatically connecting to Weaviate but not automatically closing the connection. Once you are done with the client
    you should call client.close() to close the connection and free up resources. Alternatively, you can use the client as a context manager
    in a with statement, which will automatically close the connection when the context is exited. See the examples below for details.

    Parameters:
    :   * **cluster\_url** (*str*) – The WCD cluster URL or hostname to connect to. Usually in the form: rAnD0mD1g1t5.something.weaviate.cloud
        * **auth\_credentials** (*str* *|* [*\_BearerToken*](#weaviate.auth._BearerToken "weaviate.auth._BearerToken") *|* [*\_ClientPassword*](#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword") *|* [*\_ClientCredentials*](#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials") *|* [*\_APIKey*](#weaviate.auth._APIKey "weaviate.auth._APIKey")) – The credentials to use for authentication with your Weaviate instance. This can be an API key, in which case pass a string or use
          weaviate.classes.init.Auth.api\_key(), a bearer token, in which case use weaviate.classes.init.Auth.bearer\_token(), a client secret,
          in which case use weaviate.classes.init.Auth.client\_credentials() or a username and password, in which case use weaviate.classes.init.Auth.client\_password().
        * **headers** (*Dict**[**str**,* *str**]* *|* *None*) – Additional headers to include in the requests, e.g. API keys for third-party Cloud vectorization.
        * **additional\_config** ([*AdditionalConfig*](#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") *|* *None*) – This includes many additional, rarely used config options. use wvc.init.AdditionalConfig() to configure.
        * **skip\_init\_checks** (*bool*) – Whether to skip the initialization checks when connecting to Weaviate.

    Returns:
    :   The client connected to the cluster with the required parameters set appropriately.

    Return type:
    :   [*WeaviateClient*](#weaviate.WeaviateClient "weaviate.client.WeaviateClient")

    Examples

    ```
    >>> ################## Without Context Manager #############################
    >>> import weaviate
    >>> client = weaviate.connect_to_weaviate_cloud(
    ...     cluster_url="rAnD0mD1g1t5.something.weaviate.cloud",
    ...     auth_credentials=weaviate.classes.init.Auth.api_key("my-api-key"),
    ... )
    >>> client.is_ready()
    True
    >>> client.close() # Close the connection when you are done with it.
    >>> ################## With Context Manager #############################
    >>> import weaviate
    >>> with weaviate.connect_to_weaviate_cloud(
    ...     cluster_url="rAnD0mD1g1t5.something.weaviate.cloud",
    ...     auth_credentials=weaviate.classes.init.Auth.api_key("my-api-key"),
    ... ) as client:
    ...     client.is_ready()
    True
    >>> # The connection is automatically closed when the context is exited.
    ```

weaviate.use\_async\_with\_custom(*http\_host*, *http\_port*, *http\_secure*, *grpc\_host*, *grpc\_port*, *grpc\_secure*, *headers=None*, *additional\_config=None*, *auth\_credentials=None*, *skip\_init\_checks=False*)[[source]](_modules/weaviate/connect/helpers.html#use_async_with_custom)[](#weaviate.use_async_with_custom "Link to this definition")
:   Create an async client object ready to connect to a Weaviate instance with custom connection parameters.

    If this is not sufficient for your customization needs then instantiate a weaviate.WeaviateAsyncClient instance directly.

    This method handles creating the WeaviateAsyncClient instance with relevant options to Weaviate Cloud connections but you must manually call await client.connect().
    Once you are done with the client you should call client.close() to close the connection and free up resources. Alternatively, you can use the client as a context manager
    in an async with statement, which will automatically open/close the connection when the context is entered/exited. See the examples below for details.

    Parameters:
    :   * **http\_host** (*str*) – The host to use for the underlying REST and GraphQL API calls.
        * **http\_port** (*int*) – The port to use for the underlying REST and GraphQL API calls.
        * **http\_secure** (*bool*) – Whether to use https for the underlying REST and GraphQL API calls.
        * **grpc\_host** (*str*) – The host to use for the underlying gRPC API.
        * **grpc\_port** (*int*) – The port to use for the underlying gRPC API.
        * **grpc\_secure** (*bool*) – Whether to use a secure channel for the underlying gRPC API.
        * **headers** (*Dict**[**str**,* *str**]* *|* *None*) – Additional headers to include in the requests, e.g. API keys for Cloud vectorization.
        * **additional\_config** ([*AdditionalConfig*](#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") *|* *None*) – This includes many additional, rarely used config options. use wvc.init.AdditionalConfig() to configure.
        * **auth\_credentials** ([*\_BearerToken*](#weaviate.auth._BearerToken "weaviate.auth._BearerToken") *|* [*\_ClientPassword*](#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword") *|* [*\_ClientCredentials*](#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials") *|* [*\_APIKey*](#weaviate.auth._APIKey "weaviate.auth._APIKey") *|* *None*) – The credentials to use for authentication with your Weaviate instance. This can be an API key, in which case pass a string or use weaviate.classes.init.Auth.api\_key(),
          a bearer token, in which case use weaviate.classes.init.Auth.bearer\_token(), a client secret, in which case use weaviate.classes.init.Auth.client\_credentials()
          or a username and password, in which case use weaviate.classes.init.Auth.client\_password().
        * **skip\_init\_checks** (*bool*) – Whether to skip the initialization checks when connecting to Weaviate.

    Returns:
    :   The client connected to the instance with the required parameters set appropriately.

    Return type:
    :   [*WeaviateAsyncClient*](#weaviate.WeaviateAsyncClient "weaviate.client.WeaviateAsyncClient")

    Examples

    ```
    >>> ################## Without Context Manager #############################
    >>> import weaviate
    >>> client = weaviate.use_async_with_custom(
    ...     http_host="localhost",
    ...     http_port=8080,
    ...     http_secure=False,
    ...     grpc_host="localhost",
    ...     grpc_port=50051,
    ...     grpc_secure=False,
    ... )
    >>> await client.is_ready()
    False # The connection is not ready yet, you must call `await client.connect()` to connect.
    ... await client.connect()
    >>> await client.is_ready()
    True
    >>> await client.close() # Close the connection when you are done with it.
    >>> ################## Async With Context Manager #############################
    >>> import weaviate
    >>> async with weaviate.use_async_with_custom(
    ...     http_host="localhost",
    ...     http_port=8080,
    ...     http_secure=False,
    ...     grpc_host="localhost",
    ...     grpc_port=50051,
    ...     grpc_secure=False,
    ... ) as client:
    ...     await client.is_ready()
    True
    >>> # The connection is automatically closed when the context is exited.
    ```

weaviate.use\_async\_with\_embedded(*hostname='127.0.0.1'*, *port=8079*, *grpc\_port=50050*, *headers=None*, *additional\_config=None*, *version='1.30.5'*, *persistence\_data\_path=None*, *binary\_path=None*, *environment\_variables=None*)[[source]](_modules/weaviate/connect/helpers.html#use_async_with_embedded)[](#weaviate.use_async_with_embedded "Link to this definition")
:   Create an async client object ready to connect to an embedded Weaviate instance.

    If this is not sufficient for your customization needs then instantiate a weaviate.WeaviateAsyncClient instance directly.

    This method handles creating the WeaviateAsyncClient instance with relevant options to Weaviate Cloud connections but you must manually call await client.connect().
    Once you are done with the client you should call client.close() to close the connection and free up resources. Alternatively, you can use the client as a context manager
    in an async with statement, which will automatically open/close the connection when the context is entered/exited. See the examples below for details.

    See [the docs](https://weaviate.io/developers/weaviate/installation/embedded#embedded-options) for more details.

    Parameters:
    :   * **hostname** (*str*) – The hostname to use for the underlying REST & GraphQL API calls.
        * **port** (*int*) – The port to use for the underlying REST and GraphQL API calls.
        * **grpc\_port** (*int*) – The port to use for the underlying gRPC API.
        * **headers** (*Dict**[**str**,* *str**]* *|* *None*) – Additional headers to include in the requests, e.g. API keys for Cloud vectorization.
        * **additional\_config** ([*AdditionalConfig*](#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") *|* *None*) – This includes many additional, rarely used config options. use wvc.init.AdditionalConfig() to configure.
        * **version** (*str*) – Weaviate version to be used for the embedded instance.
        * **persistence\_data\_path** (*str* *|* *None*) – Directory where the files making up the database are stored.
          When the XDG\_DATA\_HOME env variable is set, the default value is: XDG\_DATA\_HOME/weaviate/
          Otherwise it is: ~/.local/share/weaviate
        * **binary\_path** (*str* *|* *None*) – Directory where to download the binary. If deleted, the client will download the binary again.
          When the XDG\_CACHE\_HOME env variable is set, the default value is: XDG\_CACHE\_HOME/weaviate-embedded/
          Otherwise it is: ~/.cache/weaviate-embedded
        * **environment\_variables** (*Dict**[**str**,* *str**]* *|* *None*) – Additional environment variables to be passed to the embedded instance for configuration.

    Returns:
    :   The client connected to the embedded instance with the required parameters set appropriately.

    Return type:
    :   [*WeaviateAsyncClient*](#weaviate.WeaviateAsyncClient "weaviate.client.WeaviateAsyncClient")

    Examples

    ```
    >>> import weaviate
    >>> client = weaviate.use_async_with_embedded(
    ...     port=8080,
    ...     grpc_port=50051,
    ... )
    >>> await client.is_ready()
    False # The connection is not ready yet, you must call `await client.connect()` to connect.
    ... await client.connect()
    >>> await client.is_ready()
    True
    ################## With Context Manager #############################
    >>> import weaviate
    >>> async with weaviate.use_async_with_embedded(
    ...     port=8080,
    ...     grpc_port=50051,
    ... ) as client:
    ...     await client.is_ready()
    True
    >>> # The connection is automatically closed when the context is exited.
    ```

weaviate.use\_async\_with\_local(*host='localhost'*, *port=8080*, *grpc\_port=50051*, *headers=None*, *additional\_config=None*, *skip\_init\_checks=False*, *auth\_credentials=None*)[[source]](_modules/weaviate/connect/helpers.html#use_async_with_local)[](#weaviate.use_async_with_local "Link to this definition")
:   Create an async client object ready to connect to a local Weaviate instance deployed using Docker compose with standard port configurations.

    This method handles creating the WeaviateAsyncClient instance with relevant options to Weaviate Cloud connections but you must manually call await client.connect().
    Once you are done with the client you should call client.close() to close the connection and free up resources. Alternatively, you can use the client as a context manager
    in an async with statement, which will automatically open/close the connection when the context is entered/exited. See the examples below for details.

    Parameters:
    :   * **host** (*str*) – The host to use for the underlying REST and GraphQL API calls.
        * **port** (*int*) – The port to use for the underlying REST and GraphQL API calls.
        * **grpc\_port** (*int*) – The port to use for the underlying gRPC API.
        * **headers** (*Dict**[**str**,* *str**]* *|* *None*) – Additional headers to include in the requests, e.g. API keys for Cloud vectorization.
        * **additional\_config** ([*AdditionalConfig*](#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") *|* *None*) – This includes many additional, rarely used config options. use wvc.init.AdditionalConfig() to configure.
        * **skip\_init\_checks** (*bool*) – Whether to skip the initialization checks when connecting to Weaviate.
        * **auth\_credentials** (*str* *|* [*\_BearerToken*](#weaviate.auth._BearerToken "weaviate.auth._BearerToken") *|* [*\_ClientPassword*](#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword") *|* [*\_ClientCredentials*](#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials") *|* [*\_APIKey*](#weaviate.auth._APIKey "weaviate.auth._APIKey") *|* *None*) – The credentials to use for authentication with your Weaviate instance. This can be an API key, in which case pass a string or use weaviate.classes.init.Auth.api\_key(),
          a bearer token, in which case use weaviate.classes.init.Auth.bearer\_token(), a client secret, in which case use weaviate.classes.init.Auth.client\_credentials()
          or a username and password, in which case use weaviate.classes.init.Auth.client\_password().

    Returns:
    :   The async client ready to connect to the cluster with the required parameters set appropriately.

    Return type:
    :   [*WeaviateAsyncClient*](#weaviate.WeaviateAsyncClient "weaviate.client.WeaviateAsyncClient")

    Examples

    ```
    >>> ################## Without Context Manager #############################
    >>> import weaviate
    >>> client = weaviate.use_async_with_local(
    ...     host="localhost",
    ...     port=8080,
    ...     grpc_port=50051,
    ... )
    >>> await client.is_ready()
    False # The connection is not ready yet, you must call `await client.connect()` to connect.
    ... await client.connect()
    >>> await client.is_ready()
    True
    >>> await client.close() # Close the connection when you are done with it.
    >>> ################## With Context Manager #############################
    >>> import weaviate
    >>> async with weaviate.use_async_with_local(
    ...     host="localhost",
    ...     port=8080,
    ...     grpc_port=50051,
    ... ) as client:
    ...     await client.is_ready()
    True
    >>> # The connection is automatically closed when the context is exited.
    ```

weaviate.use\_async\_with\_weaviate\_cloud(*cluster\_url*, *auth\_credentials*, *headers=None*, *additional\_config=None*, *skip\_init\_checks=False*)[[source]](_modules/weaviate/connect/helpers.html#use_async_with_weaviate_cloud)[](#weaviate.use_async_with_weaviate_cloud "Link to this definition")
:   Create an async client object ready to connect to a Weaviate Cloud (WCD) instance.

    This method handles creating the WeaviateAsyncClient instance with relevant options to Weaviate Cloud connections but you must manually call await client.connect().
    Once you are done with the client you should call client.close() to close the connection and free up resources. Alternatively, you can use the client as a context manager
    in an async with statement, which will automatically open/close the connection when the context is entered/exited. See the examples below for details.

    Parameters:
    :   * **cluster\_url** (*str*) – The WCD cluster URL or hostname to connect to. Usually in the form: rAnD0mD1g1t5.something.weaviate.cloud
        * **auth\_credentials** ([*\_BearerToken*](#weaviate.auth._BearerToken "weaviate.auth._BearerToken") *|* [*\_ClientPassword*](#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword") *|* [*\_ClientCredentials*](#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials") *|* [*\_APIKey*](#weaviate.auth._APIKey "weaviate.auth._APIKey") *|* *None*) – The credentials to use for authentication with your Weaviate instance. This can be an API key, in which case pass a string or use weaviate.classes.init.Auth.api\_key(),
          a bearer token, in which case use weaviate.classes.init.Auth.bearer\_token(), a client secret, in which case use weaviate.classes.init.Auth.client\_credentials()
          or a username and password, in which case use weaviate.classes.init.Auth.client\_password().
        * **headers** (*Dict**[**str**,* *str**]* *|* *None*) – Additional headers to include in the requests, e.g. API keys for third-party Cloud vectorization.
        * **additional\_config** ([*AdditionalConfig*](#weaviate.config.AdditionalConfig "weaviate.config.AdditionalConfig") *|* *None*) – This includes many additional, rarely used config options. use wvc.init.AdditionalConfig() to configure.
        * **skip\_init\_checks** (*bool*) – Whether to skip the initialization checks when connecting to Weaviate.

    Returns:
    :   The async client ready to connect to the cluster with the required parameters set appropriately.

    Return type:
    :   [*WeaviateAsyncClient*](#weaviate.WeaviateAsyncClient "weaviate.client.WeaviateAsyncClient")

    Examples

    ```
    >>> ################## Without Context Manager #############################
    >>> import weaviate
    >>> client = weaviate.use_async_with_weaviate_cloud(
    ...     cluster_url="rAnD0mD1g1t5.something.weaviate.cloud",
    ...     auth_credentials=weaviate.classes.init.Auth.api_key("my-api-key"),
    ... )
    >>> await client.is_ready()
    False # The connection is not ready yet, you must call `await client.connect()` to connect.
    ... await client.connect()
    >>> await client.is_ready()
    True
    >>> await client.close() # Close the connection when you are done with it.
    >>> ################## With Context Manager #############################
    >>> import weaviate
    >>> async with weaviate.use_async_with_weaviate_cloud(
    ...     cluster_url="rAnD0mD1g1t5.something.weaviate.cloud",
    ...     auth_credentials=weaviate.classes.init.Auth.api_key("my-api-key"),
    ... ) as client:
    ...     await client.is_ready()
    True
    ```

# Subpackages[](#subpackages "Link to this heading")

* [weaviate.backup](weaviate.backup.html)
  + [`BackupStorage`](weaviate.backup.html#weaviate.backup.BackupStorage)
  + [`_BackupAsync`](weaviate.backup.html#weaviate.backup._BackupAsync)
  + [`_Backup`](weaviate.backup.html#weaviate.backup._Backup)
  + [weaviate.backup.backup](weaviate.backup.html#module-weaviate.backup.backup)
  + [weaviate.backup.backup\_location](weaviate.backup.html#module-weaviate.backup.backup_location)
* [weaviate.classes](weaviate.classes.html)
  + [`ConsistencyLevel`](weaviate.classes.html#weaviate.classes.ConsistencyLevel)
  + [weaviate.classes.aggregate](weaviate.classes.html#module-weaviate.classes.aggregate)
  + [weaviate.classes.backup](weaviate.classes.html#module-weaviate.classes.backup)
  + [weaviate.classes.batch](weaviate.classes.html#module-weaviate.classes.batch)
  + [weaviate.classes.config](weaviate.classes.html#module-weaviate.classes.config)
  + [weaviate.classes.data](weaviate.classes.html#module-weaviate.classes.data)
  + [weaviate.classes.debug](weaviate.classes.html#module-weaviate.classes.debug)
  + [weaviate.classes.generics](weaviate.classes.html#module-weaviate.classes.generics)
  + [weaviate.classes.init](weaviate.classes.html#module-weaviate.classes.init)
  + [weaviate.classes.query](weaviate.classes.html#module-weaviate.classes.query)
  + [weaviate.classes.rbac](weaviate.classes.html#module-weaviate.classes.rbac)
  + [weaviate.classes.tenants](weaviate.classes.html#weaviate-classes-tenants)
* [weaviate.cluster](weaviate.cluster.html)
  + [`_ClusterAsync`](weaviate.cluster.html#weaviate.cluster._ClusterAsync)
  + [`_Cluster`](weaviate.cluster.html#weaviate.cluster._Cluster)
  + [weaviate.cluster.types](weaviate.cluster.html#module-weaviate.cluster.types)
* [weaviate.collections](weaviate.collections.html)
  + [`BatchCollection`](weaviate.collections.html#weaviate.collections.BatchCollection)
  + [`Collection`](weaviate.collections.html#weaviate.collections.Collection)
  + [`CollectionAsync`](weaviate.collections.html#weaviate.collections.CollectionAsync)
  + [Subpackages](weaviate.collections.html#subpackages)
* [weaviate.connect](weaviate.connect.html)
  + [`ConnectionV4`](weaviate.connect.html#weaviate.connect.ConnectionV4)
  + [`ConnectionParams`](weaviate.connect.html#weaviate.connect.ConnectionParams)
  + [`ProtocolParams`](weaviate.connect.html#weaviate.connect.ProtocolParams)
* [weaviate.debug](weaviate.debug.html)
  + [`_Debug`](weaviate.debug.html#weaviate.debug._Debug)
  + [`_DebugAsync`](weaviate.debug.html#weaviate.debug._DebugAsync)
  + [weaviate.debug.types](weaviate.debug.html#module-weaviate.debug.types)
* [weaviate.gql](weaviate.gql.html)
  + [weaviate.gql.aggregate](weaviate.gql.html#module-weaviate.gql.aggregate)
  + [weaviate.gql.filter](weaviate.gql.html#module-weaviate.gql.filter)
* [weaviate.outputs](weaviate.outputs.html)
  + [weaviate.outputs.aggregate](weaviate.outputs.html#module-weaviate.outputs.aggregate)
  + [weaviate.outputs.backup](weaviate.outputs.html#module-weaviate.outputs.backup)
  + [weaviate.outputs.batch](weaviate.outputs.html#module-weaviate.outputs.batch)
  + [weaviate.outputs.cluster](weaviate.outputs.html#module-weaviate.outputs.cluster)
  + [weaviate.outputs.config](weaviate.outputs.html#module-weaviate.outputs.config)
  + [weaviate.outputs.data](weaviate.outputs.html#module-weaviate.outputs.data)
  + [weaviate.outputs.query](weaviate.outputs.html#module-weaviate.outputs.query)
  + [weaviate.outputs.rbac](weaviate.outputs.html#module-weaviate.outputs.rbac)
  + [weaviate.outputs.tenants](weaviate.outputs.html#module-weaviate.outputs.tenants)
* [weaviate.rbac](weaviate.rbac.html)
  + [`_RolesAsync`](weaviate.rbac.html#weaviate.rbac._RolesAsync)
  + [`_Roles`](weaviate.rbac.html#weaviate.rbac._Roles)
  + [weaviate.rbac.models](weaviate.rbac.html#module-weaviate.rbac.models)
  + [weaviate.rbac.roles](weaviate.rbac.html#weaviate-rbac-roles)
* [weaviate.users](weaviate.users.html)
  + [`_UsersAsync`](weaviate.users.html#weaviate.users._UsersAsync)
  + [`_Users`](weaviate.users.html#weaviate.users._Users)

## weaviate.auth[](#module-weaviate.auth "Link to this heading")

Authentication class definitions.

*class* weaviate.auth.\_ClientCredentials(*client\_secret*, *scope=None*)[[source]](_modules/weaviate/auth.html#_ClientCredentials)[](#weaviate.auth._ClientCredentials "Link to this definition")
:   Authenticate for the Client Credential flow using client secrets.

    Acquire the client secret from your identify provider and set the appropriate scope. The client includes hardcoded
    scopes for Azure, otherwise it needs to be supplied.
    Scopes can be given as:

    > * List of strings: [“scope1”, “scope2”]
    > * space separated string: “scope1 scope2”

    Parameters:
    :   * **client\_secret** (*str*)
        * **scope** (*str* *|* *List**[**str**]* *|* *None*)

    client\_secret*: str*[](#weaviate.auth._ClientCredentials.client_secret "Link to this definition")

    scope*: str | List[str] | None* *= None*[](#weaviate.auth._ClientCredentials.scope "Link to this definition")

*class* weaviate.auth.\_ClientPassword(*username*, *password*, *scope=None*)[[source]](_modules/weaviate/auth.html#_ClientPassword)[](#weaviate.auth._ClientPassword "Link to this definition")
:   Using username and password for authentication with Resource Owner Password flow.

    For some providers the scope needs to contain “offline\_access” (and “openid” which is automatically added) to return
    a refresh token. Without a refresh token the authentication will expire once the lifetime of the access token is up.
    Scopes can be given as:

    > * List of strings: [“scope1”, “scope2”]
    > * space separated string: “scope1 scope2”

    Parameters:
    :   * **username** (*str*)
        * **password** (*str*)
        * **scope** (*str* *|* *List**[**str**]* *|* *None*)

    username*: str*[](#weaviate.auth._ClientPassword.username "Link to this definition")

    password*: str*[](#weaviate.auth._ClientPassword.password "Link to this definition")

    scope*: str | List[str] | None* *= None*[](#weaviate.auth._ClientPassword.scope "Link to this definition")

*class* weaviate.auth.\_BearerToken(*access\_token*, *expires\_in=60*, *refresh\_token=None*)[[source]](_modules/weaviate/auth.html#_BearerToken)[](#weaviate.auth._BearerToken "Link to this definition")
:   Using a preexisting bearer/access token for authentication.

    The expiration time of access tokens is given in seconds.

    Only the access token is required. However, when no refresh token is
    given, the authentication will expire once the lifetime of the
    access token is up.

    Parameters:
    :   * **access\_token** (*str*)
        * **expires\_in** (*int*)
        * **refresh\_token** (*str* *|* *None*)

    access\_token*: str*[](#weaviate.auth._BearerToken.access_token "Link to this definition")

    expires\_in*: int* *= 60*[](#weaviate.auth._BearerToken.expires_in "Link to this definition")

    refresh\_token*: str | None* *= None*[](#weaviate.auth._BearerToken.refresh_token "Link to this definition")

*class* weaviate.auth.\_APIKey(*api\_key*)[[source]](_modules/weaviate/auth.html#_APIKey)[](#weaviate.auth._APIKey "Link to this definition")
:   Using the given API key to authenticate with weaviate.

    Parameters:
    :   **api\_key** (*str*)

    api\_key*: str*[](#weaviate.auth._APIKey.api_key "Link to this definition")

*class* weaviate.auth.Auth[[source]](_modules/weaviate/auth.html#Auth)[](#weaviate.auth.Auth "Link to this definition")
:   *static* api\_key(*api\_key*)[[source]](_modules/weaviate/auth.html#Auth.api_key)[](#weaviate.auth.Auth.api_key "Link to this definition")
    :   Parameters:
        :   **api\_key** (*str*)

        Return type:
        :   [*\_APIKey*](#weaviate.auth._APIKey "weaviate.auth._APIKey")

    *static* client\_credentials(*client\_secret*, *scope=None*)[[source]](_modules/weaviate/auth.html#Auth.client_credentials)[](#weaviate.auth.Auth.client_credentials "Link to this definition")
    :   Parameters:
        :   * **client\_secret** (*str*)
            * **scope** (*str* *|* *List**[**str**]* *|* *None*)

        Return type:
        :   [*\_ClientCredentials*](#weaviate.auth._ClientCredentials "weaviate.auth._ClientCredentials")

    *static* client\_password(*username*, *password*, *scope=None*)[[source]](_modules/weaviate/auth.html#Auth.client_password)[](#weaviate.auth.Auth.client_password "Link to this definition")
    :   Parameters:
        :   * **username** (*str*)
            * **password** (*str*)
            * **scope** (*str* *|* *List**[**str**]* *|* *None*)

        Return type:
        :   [*\_ClientPassword*](#weaviate.auth._ClientPassword "weaviate.auth._ClientPassword")

    *static* bearer\_token(*access\_token*, *expires\_in=60*, *refresh\_token=None*)[[source]](_modules/weaviate/auth.html#Auth.bearer_token)[](#weaviate.auth.Auth.bearer_token "Link to this definition")
    :   Parameters:
        :   * **access\_token** (*str*)
            * **expires\_in** (*int*)
            * **refresh\_token** (*str* *|* *None*)

        Return type:
        :   [*\_BearerToken*](#weaviate.auth._BearerToken "weaviate.auth._BearerToken")

weaviate.auth.AuthApiKey[](#weaviate.auth.AuthApiKey "Link to this definition")
:   Deprecated since version 4.0.0: Use [`api_key()`](#weaviate.auth.Auth.api_key "weaviate.auth.Auth.api_key") instead.

weaviate.auth.AuthBearerToken[](#weaviate.auth.AuthBearerToken "Link to this definition")
:   Deprecated since version 4.0.0: Use [`bearer_token()`](#weaviate.auth.Auth.bearer_token "weaviate.auth.Auth.bearer_token") instead.

weaviate.auth.AuthClientCredentials[](#weaviate.auth.AuthClientCredentials "Link to this definition")
:   Deprecated since version 4.0.0: Use [`client_credentials()`](#weaviate.auth.Auth.client_credentials "weaviate.auth.Auth.client_credentials") instead.

weaviate.auth.AuthClientPassword[](#weaviate.auth.AuthClientPassword "Link to this definition")
:   Deprecated since version 4.0.0: Use [`client_password()`](#weaviate.auth.Auth.client_password "weaviate.auth.Auth.client_password") instead.

## weaviate.config[](#module-weaviate.config "Link to this heading")

*class* weaviate.config.ConnectionConfig(*session\_pool\_connections: int = 20*, *session\_pool\_maxsize: int = 100*, *session\_pool\_max\_retries: int = 3*, *session\_pool\_timeout: int = 5*)[[source]](_modules/weaviate/config.html#ConnectionConfig)[](#weaviate.config.ConnectionConfig "Link to this definition")
:   Parameters:
    :   * **session\_pool\_connections** (*int*)
        * **session\_pool\_maxsize** (*int*)
        * **session\_pool\_max\_retries** (*int*)
        * **session\_pool\_timeout** (*int*)

    session\_pool\_connections*: int* *= 20*[](#weaviate.config.ConnectionConfig.session_pool_connections "Link to this definition")

    session\_pool\_maxsize*: int* *= 100*[](#weaviate.config.ConnectionConfig.session_pool_maxsize "Link to this definition")

    session\_pool\_max\_retries*: int* *= 3*[](#weaviate.config.ConnectionConfig.session_pool_max_retries "Link to this definition")

    session\_pool\_timeout*: int* *= 5*[](#weaviate.config.ConnectionConfig.session_pool_timeout "Link to this definition")

*class* weaviate.config.Config(*grpc\_port\_experimental: Optional[int] = None*, *grpc\_secure\_experimental: bool = False*, *connection\_config: weaviate.config.ConnectionConfig = <factory>*)[[source]](_modules/weaviate/config.html#Config)[](#weaviate.config.Config "Link to this definition")
:   Parameters:
    :   * **grpc\_port\_experimental** (*int* *|* *None*)
        * **grpc\_secure\_experimental** (*bool*)
        * **connection\_config** ([*ConnectionConfig*](#weaviate.config.ConnectionConfig "weaviate.config.ConnectionConfig"))

    grpc\_port\_experimental*: int | None* *= None*[](#weaviate.config.Config.grpc_port_experimental "Link to this definition")

    grpc\_secure\_experimental*: bool* *= False*[](#weaviate.config.Config.grpc_secure_experimental "Link to this definition")

    connection\_config*: [ConnectionConfig](#weaviate.config.ConnectionConfig "weaviate.config.ConnectionConfig")*[](#weaviate.config.Config.connection_config "Link to this definition")

*pydantic model* weaviate.config.Timeout[[source]](_modules/weaviate/config.html#Timeout)[](#weaviate.config.Timeout "Link to this definition")
:   Timeouts for the different operations in the client.

    Create a new model by parsing and validating input data from keyword arguments.

    Raises [ValidationError][pydantic\_core.ValidationError] if the input data cannot be
    validated to form a valid model.

    self is explicitly positional-only to allow self as a field name.

    *field* init*: int | float* *= 2*[](#weaviate.config.Timeout.init "Link to this definition")
    :   Constraints:
        :   * **ge** = 0

    *field* insert*: int | float* *= 90*[](#weaviate.config.Timeout.insert "Link to this definition")
    :   Constraints:
        :   * **ge** = 0

    *field* query*: int | float* *= 30*[](#weaviate.config.Timeout.query "Link to this definition")
    :   Constraints:
        :   * **ge** = 0

*pydantic model* weaviate.config.Proxies[[source]](_modules/weaviate/config.html#Proxies)[](#weaviate.config.Proxies "Link to this definition")
:   Proxy configurations for sending requests to Weaviate through a proxy.

    Create a new model by parsing and validating input data from keyword arguments.

    Raises [ValidationError][pydantic\_core.ValidationError] if the input data cannot be
    validated to form a valid model.

    self is explicitly positional-only to allow self as a field name.

    *field* grpc*: str | None* *= None*[](#weaviate.config.Proxies.grpc "Link to this definition")

    *field* http*: str | None* *= None*[](#weaviate.config.Proxies.http "Link to this definition")

    *field* https*: str | None* *= None*[](#weaviate.config.Proxies.https "Link to this definition")

*pydantic model* weaviate.config.AdditionalConfig[[source]](_modules/weaviate/config.html#AdditionalConfig)[](#weaviate.config.AdditionalConfig "Link to this definition")
:   Use this class to specify the connection and proxy settings for your client when connecting to Weaviate.

    When specifying the timeout, you can either provide a tuple with the query and insert timeouts, or a Timeout object.
    The Timeout object gives you additional option to configure the init timeout, which controls how long the client
    initialisation checks will wait for before throwing. This is useful when you have a slow network connection.

    When specifying the proxies, be aware that supplying a URL (str) will populate all of the http, https, and grpc proxies.
    In order for this to be possible, you must have a proxy that is capable of handling simultaneous HTTP/1.1 and HTTP/2 traffic.

    Create a new model by parsing and validating input data from keyword arguments.

    Raises [ValidationError][pydantic\_core.ValidationError] if the input data cannot be
    validated to form a valid model.

    self is explicitly positional-only to allow self as a field name.

    *field* connection*: [ConnectionConfig](#weaviate.config.ConnectionConfig "weaviate.config.ConnectionConfig")* *[Optional]*[](#weaviate.config.AdditionalConfig.connection "Link to this definition")

    *field* proxies*: str | [Proxies](#weaviate.config.Proxies "weaviate.config.Proxies") | None* *= None*[](#weaviate.config.AdditionalConfig.proxies "Link to this definition")

    *field* timeout\_*: Tuple[int, int] | [Timeout](#weaviate.config.Timeout "weaviate.config.Timeout")* *[Optional]* *(alias 'timeout')*[](#weaviate.config.AdditionalConfig.timeout_ "Link to this definition")

    *field* trust\_env*: bool* *= False*[](#weaviate.config.AdditionalConfig.trust_env "Link to this definition")

    *property* timeout*: [Timeout](#weaviate.config.Timeout "weaviate.config.Timeout")*[](#weaviate.config.AdditionalConfig.timeout "Link to this definition")

## weaviate.embedded[](#module-weaviate.embedded "Link to this heading")

*class* weaviate.embedded.EmbeddedOptions(*persistence\_data\_path: str = '/home/docs/.local/share/weaviate'*, *binary\_path: str = '/home/docs/.cache/weaviate-embedded'*, *version: str = '1.30.5'*, *port: int = 8079*, *hostname: str = '127.0.0.1'*, *additional\_env\_vars: Dict[str, str] | None = None*, *grpc\_port: int = 50060*)[[source]](_modules/weaviate/embedded.html#EmbeddedOptions)[](#weaviate.embedded.EmbeddedOptions "Link to this definition")
:   Parameters:
    :   * **persistence\_data\_path** (*str*)
        * **binary\_path** (*str*)
        * **version** (*str*)
        * **port** (*int*)
        * **hostname** (*str*)
        * **additional\_env\_vars** (*Dict**[**str**,* *str**]* *|* *None*)
        * **grpc\_port** (*int*)

    persistence\_data\_path*: str* *= '/home/docs/.local/share/weaviate'*[](#weaviate.embedded.EmbeddedOptions.persistence_data_path "Link to this definition")

    binary\_path*: str* *= '/home/docs/.cache/weaviate-embedded'*[](#weaviate.embedded.EmbeddedOptions.binary_path "Link to this definition")

    version*: str* *= '1.30.5'*[](#weaviate.embedded.EmbeddedOptions.version "Link to this definition")

    port*: int* *= 8079*[](#weaviate.embedded.EmbeddedOptions.port "Link to this definition")

    hostname*: str* *= '127.0.0.1'*[](#weaviate.embedded.EmbeddedOptions.hostname "Link to this definition")

    additional\_env\_vars*: Dict[str, str] | None* *= None*[](#weaviate.embedded.EmbeddedOptions.additional_env_vars "Link to this definition")

    grpc\_port*: int* *= 50060*[](#weaviate.embedded.EmbeddedOptions.grpc_port "Link to this definition")

weaviate.embedded.get\_random\_port()[[source]](_modules/weaviate/embedded.html#get_random_port)[](#weaviate.embedded.get_random_port "Link to this definition")
:   Return type:
    :   int

*class* weaviate.embedded.EmbeddedV3(*options*)[[source]](_modules/weaviate/embedded.html#EmbeddedV3)[](#weaviate.embedded.EmbeddedV3 "Link to this definition")
:   Parameters:
    :   **options** ([*EmbeddedOptions*](#weaviate.embedded.EmbeddedOptions "weaviate.embedded.EmbeddedOptions"))

    is\_listening()[[source]](_modules/weaviate/embedded.html#EmbeddedV3.is_listening)[](#weaviate.embedded.EmbeddedV3.is_listening "Link to this definition")
    :   Return type:
        :   bool

    start()[[source]](_modules/weaviate/embedded.html#EmbeddedV3.start)[](#weaviate.embedded.EmbeddedV3.start "Link to this definition")
    :   Return type:
        :   None

weaviate.embedded.EmbeddedDB[](#weaviate.embedded.EmbeddedDB "Link to this definition")
:   alias of [`EmbeddedV3`](#weaviate.embedded.EmbeddedV3 "weaviate.embedded.EmbeddedV3")

*class* weaviate.embedded.EmbeddedV4(*options*)[[source]](_modules/weaviate/embedded.html#EmbeddedV4)[](#weaviate.embedded.EmbeddedV4 "Link to this definition")
:   Parameters:
    :   **options** ([*EmbeddedOptions*](#weaviate.embedded.EmbeddedOptions "weaviate.embedded.EmbeddedOptions"))

    is\_listening()[[source]](_modules/weaviate/embedded.html#EmbeddedV4.is_listening)[](#weaviate.embedded.EmbeddedV4.is_listening "Link to this definition")
    :   Return type:
        :   bool

    start()[[source]](_modules/weaviate/embedded.html#EmbeddedV4.start)[](#weaviate.embedded.EmbeddedV4.start "Link to this definition")
    :   Return type:
        :   None