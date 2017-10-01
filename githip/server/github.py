import asyncio
import aiohttp
import re
import ujson

from functools import lru_cache

from sanic.log import log

from .errors import ApiError


json_dumps = ujson.dumps  # pylint: disable=no-member
json_loads = ujson.loads  # pylint: disable=no-member


URI = 'https://api.github.com'
DEFAULT_HEADERS = {
    'Accept': 'application/vnd.github.v3+json',
}
LINK_RE = re.compile(r'^<(.*)>;.*rel="([a-z]+)"$')


def parse_links(links):
    if not links:
        return None, None

    links = links.split(',')
    link_map = {}
    for link in links:
        link = link.strip()
        url, rel = LINK_RE.match(link).groups()
        link_map[rel] = url

    return link_map.get('prev'), link_map.get('next')


async def _make_request(session, url, method, params, json):
    async with session.request(method, url, params=params, json=json) as resp:
        try:
            resp.raise_for_status()
        except aiohttp.ClientResponseError:
            log.exception('error making request %s %s %s', url,
                          (params or json), resp.headers)
            raise ApiError('Bad Request', code='GithubError')

        data = await resp.json(loads=json_loads)
        return resp.headers, data


async def make_request(endpoint, method='GET', *, headers=None, params=None,
                       json=None, follow_pages=True):
    """
    Makes a github request.
    NOTE: aiohttp.request will use asyncio.get_event_loop.
    The ONLY reason this works is because we mount the app
    using app.run in server.py

    If the response isn't json, a ValueError is raised.
    Sanic will convert that to a 500 and
    it will be logged in the error handler
    which is what we want
    """

    url = '%s%s' % (URI, endpoint)
    headers = headers if headers else {}
    headers.update(DEFAULT_HEADERS)
    results = []
    async with aiohttp.ClientSession(headers=headers, read_timeout=3,
                                     json_serialize=json_dumps,
                                     conn_timeout=1) as session:

        headers, data = await _make_request(session, url, method, params, json)

        if isinstance(data, list):
            results.extend(data)
        else:
            return data

        if follow_pages:
            links = headers.get('Link')
            _, next_link = parse_links(links)

            while next_link:
                headers, data = await _make_request(session, next_link,
                                                    method, params, json)
                results.extend(data)

                links = headers.get('Link')
                _, next_link = parse_links(links)

    return results


"""
NOTES on caching:

    By adding ensure_future, we convert the
    coroutine to a asyncio.Task which can be
    `await`ed multiple times and return the same results.
    This allows the lru_cache to work because the Task
    object is what gets stored in the cache.
"""


@lru_cache(maxsize=256)
def get_organization_members(org_name):
    return asyncio.ensure_future(make_request(
        '/orgs/%s/members' % org_name,
        params=dict(filter='all', role='all')
    ))


@lru_cache(maxsize=256)
def get_organization_repos(org_name):
    return asyncio.ensure_future(make_request(
        '/orgs/%s/repos' % org_name,
        params=dict(type='public')
    ))


async def get_repo_contributor_stats(org_name, repo):
    return await make_request(
        '/repos/%s/%s/stats/contributors' % (org_name, repo)
    )


async def get_repo_commits(org_name, repo):
    return await make_request(
        '/repos/%s/%s/commits' % (org_name, repo),
        follow_pages=False
    )
