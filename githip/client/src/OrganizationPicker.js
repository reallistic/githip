import React, { Component } from 'react';
import { FormControl, Col, Form, Button, Row, Alert } from 'react-bootstrap';
import './OrganizationPicker.css';

class OrganizationPicker extends Component {
  constructor(props) {
    super(props);

    this.state = {
      organization: props.organization
    };

    this.onSetOrg = this.onSetOrg.bind(this);
  }

  componentWIllReceiveProps(nextProps) {
    if (nextProps.organization !== this.props.organization) {
      this.setState({organization: nextProps.organization});
    }
  }

  onSetOrg(e) {
    e.preventDefault();
    this.props.onSetOrg(this.state.organization);
  }

  render() {
    return (
      <div className="cover-container">
        <div className="inner cover">
            <h1 className="cover-heading">GitHip to your Github Organization Stats</h1>
            <p className="lead">Enter your GitHub Organization name below to learn more about your repos</p>
            <Form>
              <Row>
                <Col xs={8} md={10}>
                  <FormControl
                    type="text"
                    value={this.state.organization}
                    placeholder="Github Organization"
                    onChange={e => this.setState({organization: e.target.value})}
                  />
                </Col>
                <Col xs={4} md={2}>
                  <Button
                    bsStyle="primary"
                    type="submit"
                    onClick={this.onSetOrg}
                  >Submit</Button>
                </Col>
              </Row>
              {this.props.error ?
                  <Row>
                    <Alert bsStyle="danger">
                      <h4>An error occured</h4>
                      <p>Please check the organization name and try again. If the problem persists, contact the developer.</p>
                      <pre>{this.props.error.toString()}</pre>
                    </Alert>
                  </Row>: null}
            </Form>
        </div>
      </div>
    );
  }
}

export default OrganizationPicker;

