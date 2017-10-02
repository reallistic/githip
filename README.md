# githip
Git hip to the popularity of your organization's project on github


# About
GitHip will list all of the *public* repositories in your github organization ordered by watchers + stargazers in descending order.
Upon clicking through to a repo, it will show you some stats and the recent commits.
GitHip introduces a stat called *open source index* or OSI for short.
The OSI is determined by *the ratio of average commits per week from non-organization members vs organization members multiplied by the average number of commits per week*.

The idea is that repositories with a higher non-member/member commit ratio and a lot of activity will be more popular in the open source community.
This project will test that assumption.


# Building
This project uses python3.6.
To skip python3.6 installation use the included Dockerfile.

## Installation
```
git clone https://github.com/reallistic/githip.git
cd githip
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

# Running
```
cd githip
. venv/bin/activate
python server.py
```

or using docker-compose

```
docker-compose up
```
