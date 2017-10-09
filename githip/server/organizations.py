import asyncio
import functools

from . import github


REPO_KEYS = set(['fork', 'forks_count', 'commits_url', 'created_at',
                 'description', 'full_name', 'has_issues', 'language',
                 'name', 'open_issues_count', 'stargazers_count',
                 'watchers_count', 'url'])

MEMBER_KEYS = set(['id', 'login', 'type', 'url'])

COMMIT_KEYS = set(['sha', 'url', 'html_url', 'author', 'commit.message',
                   'commit.author', 'commit.comment_count'])


def get_repo_sort_key(repo):
    stars = repo['stargazers_count']
    watchers = repo['watchers_count']

    return stars + watchers


def select_keys(obj, *, keys):
    result = {}
    for key in keys:
        if '.' in key:
            value = obj
            key_parts = key.split('.')
            result_key = '_'.join(key_parts)
            while True:
                try:
                    key = key_parts.pop(0)
                    value = value[key]
                except IndexError:
                    break
            result[result_key] = value
        else:
            result[key] = obj.get(key)

    return result


def select_repo_keys(obj):
    return select_keys(obj, keys=REPO_KEYS)


def select_member_keys(obj):
    return select_keys(obj, keys=MEMBER_KEYS)


def select_commit_keys(obj):
    return select_keys(obj, keys=COMMIT_KEYS)


def format_commit(commit):
    result = select_commit_keys(commit)
    if result['author']:
        result['author'] = select_member_keys(result['author'])

    return result


def add_commits(total, stats):
    return sum(map(lambda week: week['c'], stats['weeks'])) + total


def calculate_commit_avg(contrib_stats):
    if not contrib_stats:
        return 0

    total_commits = functools.reduce(add_commits, contrib_stats, 0)
    num_weeks = len(contrib_stats[0]['weeks'])
    avg_per_week = float(total_commits) / float(num_weeks)

    return avg_per_week


async def get_members(org_name):
    members = await github.get_organization_members(org_name)
    members = list(map(select_member_keys, members))
    return members


async def get_repos(org_name):
    repos = await github.get_organization_repos(org_name)
    repos = list(map(select_repo_keys, repos))
    repos = sorted(repos, key=get_repo_sort_key, reverse=True)
    return repos


async def get_stats(org_name, repo):
    members, contrib_stats = await asyncio.gather(
        get_members(org_name),
        github.get_repo_contributor_stats(org_name, repo)
    )

    members = set([member['login'] for member in members])
    member_stats = []
    non_member_stats = []

    for stats in contrib_stats:
        if stats['author']['login'] in members:
            member_stats.append(stats)
        else:
            non_member_stats.append(stats)

    average = calculate_commit_avg(contrib_stats)
    member_average = calculate_commit_avg(member_stats)
    non_member_average = calculate_commit_avg(non_member_stats)
    if member_average == 0:
        ratio = non_member_average
    else:
        ratio = non_member_average / member_average
    osi = ratio * average

    stats = dict(
        osi=osi,
        ratio=ratio,
        commit_avg=average,
        member_commit_avg=member_average,
        non_member_commit_avg=non_member_average
    )

    return stats


async def get_commits(org_name, repo):
    commits = await github.get_repo_commits(org_name, repo)
    commits = map(format_commit, commits)
    return commits
