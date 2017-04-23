import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'
import {FormGroup, Form, Button, Checkbox, HelpBlock, FormControl,
  ControlLabel, Col} from 'react-bootstrap'
import * as loginActions from '../../actions/authActions'
import { validateEmail } from '../../utils/misc'

class RegisterPage extends Component {
  constructor (props) {
    super(props)
    const redirectRoute = '/login'
    this.state = {
      email: '',
      password: '',
      firstName: '',
      lastName: '',
      confirmPassword: '',
      statusText: this.props.registerStatusText,
      redirectTo: redirectRoute,
      disabled: true,
      submit: this.props.submit
    }
  }

  isDisabled () {
    let emailIsValid = false
    let passwordIsValid = false
    let passwordMatch = false
    let userDetails = false

    if (this.state.password === this.state.confirmPassword) {
      passwordMatch = true
    } else {
      this.setState({
        statusText: 'Passwords must be a match!'
      })
    }
    if (this.state.password.length >= 6) {
      passwordIsValid = true
    } else {
      this.setState({
        statusText: 'Password must be at least 6 characters!'
      })
    }
    if (validateEmail(this.state.email)) {
      emailIsValid = true
    } else {
      this.setState({
        statusText: 'Enter a valid email!'
      })
    }
    if (this.state.firstName && this.state.lastName) {
      userDetails = true
    } else {
      this.setState({
        statusText: 'All fields are required!'
      })
    }

    if (emailIsValid && passwordIsValid && passwordMatch && userDetails) {
      this.setState({
        disabled: false
      })
    }
    this.setState({
      submit: false
    })
  }

  changeValue (e, type) {
    const value = e.target.value
    const nextState = {}
    nextState[type] = value
    this.setState(nextState, () => {
      this.isDisabled()
    })
  }

  _handleKeyPress (e) {
    if (e.key === 'Enter') {
      this.register(e)
    }
  }

  register (e) {
    e.preventDefault()
    this.setState({
      submit: true
    })
    if (!this.state.disabled) {
      this.setState({
        statusText: null
      })
      this.props.registerUser(this.state.firstName, this.state.lastName,
        this.state.email, this.state.password, this.state.confirmPassword)
    }
  }
  render () {
    return (
      <Form horizontal>
        <FormGroup controlId="" bsSize="large" bsStyle="centered">
          <Col smOffset={4} sm={8} smSize="large">
            {(this.state.submit) ? this.state.statusText : ''}
          </Col>
        </FormGroup>
        <FormGroup controlId="formHorizontalFirstName">
          <Col componentClass={ControlLabel} sm={4}>
            First Name
          </Col>
          <Col sm={6}>
            <FormControl type="text" placeholder="First Name"
              onChange={(e) => this.changeValue(e, 'firstName')} />
          </Col>
        </FormGroup>

        <FormGroup controlId="formHorizontalLastName">
          <Col componentClass={ControlLabel} sm={4}>
            Last Name
          </Col>
          <Col sm={6}>
            <FormControl type="text" placeholder="Last Name"
              onChange={(e) => this.changeValue(e, 'lastName')} />
          </Col>
        </FormGroup>
        <FormGroup controlId="formHorizontalEmail">
          <Col componentClass={ControlLabel} sm={4}>
            Email
          </Col>
          <Col sm={6}>
            <FormControl type="text" placeholder="Email"
              onChange={(e) => this.changeValue(e, 'email')} />
          </Col>
        </FormGroup>

        <FormGroup controlId="formHorizontalPassword">
          <Col componentClass={ControlLabel} sm={4}>
            Password
          </Col>
          <Col sm={6}>
            <FormControl type="password" placeholder="Password"
              onChange={(e) => this.changeValue(e, 'password')} />
          </Col>
        </FormGroup>
        <FormGroup controlId="formHorizontalConfirmPassword">
          <Col componentClass={ControlLabel} sm={4}>
            Confirm Password
          </Col>
          <Col sm={6}>
            <FormControl type="password" placeholder="Confirm Password"
              onChange={(e) => this.changeValue(e, 'confirmPassword')} />
          </Col>
        </FormGroup>
        <FormGroup>
          <Col smOffset={4} sm={10}>
            <Button type="submit" bsStyle="success" onClick={(e) => this.register(e)}>
              Register
            </Button>
          </Col>
        </FormGroup>
      </Form>
    )
  }
}

RegisterPage.propTypes = {
  registerUser: PropTypes.func,
  registerStatusText: PropTypes.string
}

function mapStateToProps (state) {
  return {
    isRegistering: state.auth.isRegistering,
    registerStatusText: state.auth.registerStatusText
  }
}

function mapDispatchToProps (dispatch) {
  return bindActionCreators(loginActions, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(RegisterPage)
