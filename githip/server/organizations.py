import asyncio

from . import github


REPO_KEYS = set(['fork', 'forks_count', 'commits_url', 'created_at',
                 'description', 'full_name', 'has_issues', 'language',
                 'name', 'open_issues_count', 'stargazers_count',
                 'watchers_count', 'url'])

MEMBER_KEYS = set(['id', 'login', 'type', 'url'])

COMMIT_KEYS = set(['sha', 'url', 'html_url', 'author', 'commit.message',
                   'commit.author', 'commit.comment_count'])


def calculate_commits_per_week(contrib_stats, members):
    commits_per_week = 0
    member_commits = 0
    non_member_commits = 0
    num_weeks = 0

    for stats in contrib_stats:
        author = stats['author']['login']
        num_weeks = len(stats['weeks'])
        for week in stats['weeks']:
            # Total per week
            commits_per_week += week['c']

            if author in members:
                # Total per week for members
                member_commits += week['c']
            else:
                # Total per week for non_members
                non_member_commits += week['c']

    avg_per_week = float(commits_per_week) / float(num_weeks)

    return (
        avg_per_week,
        member_commits,
        non_member_commits,
    )


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


async def get_members(org_name):
    members = await github.get_organization_members(org_name)
    members = list(map(select_member_keys, members))
    return members


async def get_repos(org_name):
    repos = await github.get_organization_repos(org_name)
    repos = list(map(select_repo_keys, repos))
    repos = sorted(repos, key=get_repo_sort_key, reverse=True)
    return repos


async def get_osi(org_name, repo):
    members, contrib_stats = await asyncio.gather(
        github.get_repo_contributor_stats(org_name, repo),
        get_members(org_name)
    )

    members = set([member['login'] for member in members])

    average, member, non_member = calculate_commits_per_week(
        contrib_stats,
        members
    )

    osi = float(non_member) / float(member) * average

    return osi


async def get_commits(org_name, repo):
    commits = await github.get_repo_commits(org_name, repo)
    commits = map(format_commit, commits)
    return commits
