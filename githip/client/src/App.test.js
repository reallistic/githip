import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<App />, div);
});


describe('App', () => {
  let div, component;
  beforeEach(() => {
    div = document.createElement('div');
    component = ReactDOM.render(<App />, div);
  });

  describe('orgpicker', () => {
    it('shows orgpicker by default', () => {
      expect(div.querySelector('.form-control').placeholder).toBe("Github Organization");
    });

    it('shows orgpicker with error', done => {
      component.setState({error: 'test', organization: 'blah', repo: 'blah'}, () => {
        expect(div.querySelector('.form-control').placeholder).toBe("Github Organization");
        expect(div.querySelector('.alert-danger pre').innerHTML).toBe("test");
        done();
      });
    });
  });

  describe('repobrowser', () => {
    it('shows when there is an organization', done => {
      component.setState({organization: 'test'}, () => {
        expect(div.querySelector('.page-header').innerHTML).toBe("<h1>Notable repos for test</h1>");
        done();
      });
    });
  });

  describe('repostats', () => {
    it('shows when there is an repo', done => {
      component.setState({
        organization: 'test',
        repo: 'blue',
        repos: [{
          name: 'blue',
          description: 'blue repo',
          watchers_count: 0,
          stargazers_count: 0
        }],
        repoStats: {
          osi: 0,
          ratio: 0,
          commit_avg: 0,
          member_commit_avg: 0,
          non_member_commit_avg: 0
        }
      }, () => {
        expect(div.querySelector('.page-header').innerHTML).toBe("<h1>test / blue</h1>");
        done();
      });
    });
  });
});
