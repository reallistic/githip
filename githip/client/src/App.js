import React, { Component } from 'react';
import { ProgressBar } from 'react-bootstrap';

import OrganizationPicker from './OrganizationPicker';
import RepoBrowser from './RepoBrowser';
import RepoStats from './RepoStats';

import { fetchRepos, fetchRepoStats } from './actions';

import './App.css';


class App extends Component {
  constructor(props) {
    super(props);

    this.state = this._getInitialState();

    this.onSetOrg = this.onSetOrg.bind(this);
    this.onSetRepo = this.onSetRepo.bind(this);
    this.onReset = this.onReset.bind(this);
  }

  _getInitialState() {
    return {
      organization: '',
      repo: '',
      repoStats: {},
      repoCommits: [],
      repos: [],
      isLoading: false,
      error: null
    };
  }

  onSetOrg(organization) {
    fetchRepos(organization).then(({repos}) => {
      this.setState({repos, isLoading: false, error: null});
    },
    error => {
      let nextState = this._getInitialState();
      this.setState(Object.assign({}, nextState, {error, organization}));
    });
    this.setState({organization, isLoading: true});
  }

  onSetRepo(repo) {
    let organization = this.state.organization;
    fetchRepoStats(organization, repo).then(({commits, stats}) => {
      this.setState({
        repoStats: stats,
        repoCommits: commits,
        isLoading: false,
        error: null
      });
    },
    error => {
      let nextState = this._getInitialState();
      this.setState(
        Object.assign({}, nextState, {error, organization})
      );
    });
    this.setState({repo, isLoading: true});
  }

  onReset(e, keepOrg = false) {
    let nextState = this._getInitialState();
    if (keepOrg) {
      nextState.organization = this.state.organization;
      nextState.repos = this.state.repos;
    }
    this.setState(nextState);
  }

  getContent() {
    if (this.state.isLoading) {
      return (
        <div className="cover-container">
          <div className="inner cover">
            <ProgressBar active now={100} />
          </div>
        </div>
      );
    }
    else if (this.state.organization === '' || this.state.error) {
      return (
        <OrganizationPicker
          organization={this.state.organization}
          onSetOrg={this.onSetOrg}
          error={this.state.error}
        />
      );
    }
    else if (this.state.repo) {
      const repo = this.state.repos.find(repo => repo.name === this.state.repo);
      return (
        <RepoStats
            organization={this.state.organization}
            repo={repo}
            repoStats={this.state.repoStats}
            repoCommits={this.state.repoCommits}
            onReset={() => this.onReset(null, true)}
        />
      );
    }
    else {
      return (
        <RepoBrowser
          organization={this.state.organization}
          repos={this.state.repos}
          onReset={this.onReset}
          onSetRepo={this.onSetRepo}
        />
      );
    }
  }

  render() {
    return (
      <div className="site">
        <div className="site-inner">
          {this.getContent()}
        </div>
      </div>
    );
  }
}

export default App;
