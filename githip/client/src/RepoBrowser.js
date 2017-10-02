import React, { Component } from 'react';
import { Grid, Col, Row, PageHeader, Panel, Button } from 'react-bootstrap';

import EyeIcon from './EyeIcon';
import StarIcon from './StarIcon';
import BackIcon from './BackIcon';

import './RepoBrowser.css';


function RepoRow ({repo, onSetRepo}) {
  return (
    <Row onClick={() => onSetRepo(repo.name)} >
      <Col xs={8} md={8}>
        <h3>{repo.name}</h3>
        <p>{repo.description}</p>
      </Col>
      <Col xs={2} md={2}>
        <EyeIcon /> {repo.watchers_count}
      </Col>
      <Col xs={2} md={2}>
        <StarIcon /> {repo.stargazers_count}
      </Col>
    </Row>
  );
}


function RepoHeader({organization, onReset}) {
  return (
    <div className="header">
      <span className="align-middle header-back-button">
        <Button bsStyle="link" onClick={onReset}>
          <BackIcon />Pick another org
        </Button>
      </span>
      <PageHeader>Notable repos for {organization}</PageHeader>
    </div>
  );
}


class RepoBrowser extends Component {
  render() {
    return (
      <Grid>
        <Panel
          header={
            <RepoHeader
              organization={this.props.organization}
              onReset={this.props.onReset}
            />
          }>
          <Grid>
            {this.props.repos.length ?
              this.props.repos.map(repo => {
                return (
                  <RepoRow
                    repo={repo}
                    key={repo.name}
                    onSetRepo={this.props.onSetRepo}
                  />
                );
              })
              :
              <h3>No Repos</h3>
            }
          </Grid>
        </Panel>
      </Grid>
    );
  }
}

export default RepoBrowser;
