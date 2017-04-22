import React, {Component} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'
import {FormGroup, Form, Button, Checkbox, FormControl, ControlLabel, Col} from 'react-bootstrap'
import * as loginActions from '../../actions/authActions'

class LoginPage extends Component {
  constructor (props) {
    super(props)
    const redirectRoute = '/login'
    this.state = {
      email: '',
      password: '',
      email_error_text: null,
      password_error_text: null,
      redirectTo: redirectRoute,
      disabled: true
    }
  }
  changeValue (e, type) {
    const value = e.target.value
    const next_state = {}
    next_state[type] = value
    this.setState(next_state)
  }

  _handleKeyPress (e) {
    if (e.key === 'Enter') {
      if (!this.state.disabled) {
        this.login(e)
      }
    }
  }

  login (e) {
    e.preventDefault()
    this.props.loginUser(this.state.email, this.state.password)
  }
  render () {
    return (
      <Form horizontal>
        <FormGroup controlId="formHorizontalEmail">
          <Col sm={12}>
            {this.props.statusText}
          </Col>
        </FormGroup>
        <FormGroup controlId="formHorizontalEmail">
          <Col componentClass={ControlLabel} sm={2}>
            Email
          </Col>
          <Col sm={10}>
            <FormControl type="text" placeholder="Email" onChange={(e) => this.changeValue(e, 'email')} />
          </Col>
        </FormGroup>

        <FormGroup controlId="formHorizontalPassword">
          <Col componentClass={ControlLabel} sm={2}>
            Password
          </Col>
          <Col sm={10}>
            <FormControl type="password" placeholder="Password" onChange={(e) => this.changeValue(e, 'password')} />
          </Col>
        </FormGroup>

        <FormGroup>
          <Col smOffset={2} sm={10}>
            <Checkbox>Remember me</Checkbox>
          </Col>
        </FormGroup>

        <FormGroup>
          <Col smOffset={2} sm={10}>
            <Button type="submit" onClick={(e) => this.login(e)}>
              Sign in
            </Button>
          </Col>
        </FormGroup>
      </Form>
    )
  }
}

function mapStateToProps (state) {
  return {
    isAuthenticating: state.auth.isAuthenticating,
    statusText: state.auth.statusText
  }
}

function mapDispatchToProps (dispatch) {
  return bindActionCreators(loginActions, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(LoginPage)
