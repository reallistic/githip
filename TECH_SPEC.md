# Tech Spec


# What
This repo will be gathering data from a given github organization and displaying it in a meaningful way via a web based application.

# Who
The target user is a member of a given organization looking to better understand how their repositories are connected to the open source community at large.

# Spec

## Server
### Framework
The server will be a Python 3.6 async/await server utilizing [Sanic](https://github.com/channelcat/sanic) for serving api requests.
Sanic was chosen because it is lightweight and extremely fast when handling I/O bound applications. Plus it is cool :).

Sanic is written on top of UVLOOP and has its own built-in server. It is a slightly more mature asyncio python server in that it has a healthy set of [extensions](https://github.com/channelcat/sanic/wiki/Extensions) and a couple projects in [production](https://github.com/channelcat/sanic/wiki/Projects).

### Entry
The internal implementation is held in `githip/server/app.py` where we utilize a factory function `create_app` to configure and return a sanic app instance.

The entry point for the server is located at `server.py` in the top level folder. This calls the factory function and starts the built-in sanic server.


### Logging
`githip/server/app.py is also where logging is setup. For this we call into the `githip/server/logging.py` module to configure sanic's built in logger which is used throughout the project.
By default, we use the INFO log level, but this can be controlled using a environment variable called `LOG_LEVEL`. More details on how the config is used are below.


### Config
`githip/server/config.py` contains two config classes: `Dev` and `Prod`. For now they are not much different.
Some unpythonic (magical) helper class methods and overrides are used to handle casting and validation of config at start time to ensure the app doesn't boot without valid config, thus reducing the potential of Runtime issues.


### Routes and Views
All HTTP routes that handle api calls are located in `githip/server/routes.py` HTTP routes that return html templates are located in `githip/server/views.py`.
Both of these utilize a `Blueprint` for easier organization as well as to specify a `url_prefix` on the `/api` calls.
Most of the routes are kept pure and RESTful. Their implementation details are located in a namespaced file.
For example, the implementation of `/api/organization` (which returns high level organization data) is located in `githip/server/organizations.py`.


### Data crunching and retrieval
GitHip uses the v3 github api to fetch all of its data. For data that does not often change (like members of a organization), a simple [`lru_cache`](https://docs.python.org/3/library/functools.html?highlight=lru_cache#functools.lru_cache) is used.
All data is crunched on the server so that the javascript code just needs to read and display it.
The organization members api is used to display members, thus if you are looking at a org you are not a member of, concealed members are not displayed.

### OSI calculation
First, we retreive a list of all members of a organization, in parallel we also get a list of all public repositories.
Once we have a list of repositories, we only keep forks with at least 10 stars + watchers. (This was arbitrary and may change later)
For each repository we kept, we go and fetch the `repo/stats/contributors` information to get the commits per week per contributor.

Next, we calculate the total number of commits per week by adding up for each contributer O(n).
In the same loop using the org member data, we keep track of how many commits were made per week by org members vs non-members.
We then calculate average commits per week for the following groups: all contributors, non-org member contributors, and org member contributores and return this information to the client.
