import React from 'react';
import { Jumbotron, Grid, PageHeader, Button } from 'react-bootstrap';

import BackIcon from './BackIcon';
import CommitList from './CommitList';

import './RepoStats.css';

function RepoHeader({organization, onReset, repo}) {
  return (
    <div className="header">
      <span className="align-middle header-back-button">
        <Button bsStyle="link" onClick={onReset}>
          <BackIcon />Pick another repo
        </Button>
      </span>
      <PageHeader>{organization} / {repo.name}</PageHeader>
    </div>
  );
}

export default function RepoStats({repo, repoStats, organization, onReset, repoCommits}) {

  return (
    <Grid>
      <RepoHeader
        organization={organization}
        repo={repo}
        onReset={onReset}
      />
      <Jumbotron>
        <h1>{repo.name}</h1>
        <p>{repo.description}</p>
        <div className="jumbotron-body">
          <ul>
            <li><strong>OSI score:</strong> {repoStats.osi}</li>
            <li><strong>Commit ratio:</strong> {repoStats.ratio}</li>
            <li><strong>Avg commits per week:</strong> {repoStats.commit_avg}</li>
            <li><strong>Avg commits per week by org members:</strong> {repoStats.member_commit_avg}</li>
            <li><strong>Avg commits per week by non org members:</strong> {repoStats.non_member_commit_avg}</li>
            <li><strong>Watchers:</strong> {repo.watchers_count}</li>
            <li><strong>Stars:</strong> {repo.stargazers_count}</li>
          </ul>
        </div>
      </Jumbotron>
      <PageHeader>Recent Commits</PageHeader>
      <section className="commit-list">
        <CommitList commits={repoCommits} />
      </section>
    </Grid>
  );

}
