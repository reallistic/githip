import asyncio

from sanic import Blueprint

from . import github
from .response import make_json_response

blueprint = Blueprint(__name__, url_prefix='/api')


@blueprint.route('/organization/<org_name>/members', methods=['GET'])
async def get_org_members(_, org_name=None):
    members = await github.get_organization_members(org_name)
    return make_json_response(members=members)


@blueprint.route('/organization/<org_name>', methods=['GET'])
async def get_org_data(_, org_name=None):
    members, repos = await asyncio.gather(
        github.get_organization_members(org_name),
        github.get_organization_repos(org_name)
    )
    return make_json_response(members=members, repos=repos)


@blueprint.route('/organization/<org_name>/<repo>', methods=['GET'])
async def get_repo_commits(_, org_name=None, repo=None):
    commits = await github.get_repo_commits(org_name, repo)
    return make_json_response(commits=commits)
