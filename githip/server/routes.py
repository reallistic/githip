import asyncio

from sanic import Blueprint

from . import organizations
from .response import make_json_response

blueprint = Blueprint(__name__, url_prefix='/api')


@blueprint.route('/organization/<org_name>', methods=['GET'])
async def get_org_data(_, org_name=None):
    members, repos = await asyncio.gather(
        organizations.get_members(org_name),
        organizations.get_repos(org_name)
    )
    return make_json_response(members=members, repos=repos)


@blueprint.route('/organization/<org_name>/osi/<repo>', methods=['GET'])
async def get_org_repo_osi(_, org_name=None, repo=None):
    repo_osi = await organizations.get_osi(org_name, repo)
    return make_json_response(osi=repo_osi)


@blueprint.route('/organization/<org_name>/members', methods=['GET'])
async def get_org_members(_, org_name=None):
    members = await organizations.get_members(org_name)
    return make_json_response(members=members)


@blueprint.route('/organization/<org_name>/repos', methods=['GET'])
async def get_org_repos(_, org_name=None):
    repos = await organizations.get_repos(org_name)
    return make_json_response(repos=repos)


@blueprint.route('/organization/<org_name>/repos/<repo>', methods=['GET'])
async def get_repo_commits(_, org_name=None, repo=None):
    commits = await organizations.get_commits(org_name, repo)
    return make_json_response(commits=commits)
