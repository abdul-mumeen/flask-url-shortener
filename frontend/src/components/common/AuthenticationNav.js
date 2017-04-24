import React, {Component, PropTypes} from 'react'
import {Nav, Button} from 'react-bootstrap'
import {browserHistory} from 'react-router'
import MainModal from './MainModal'
import LoginPage from '../login/LoginPage'
import RegisterPage from '../register/RegisterPage'

class AuthenticationNav extends Component {
  constructor (props) {
    super(props)
    this.state = {
      body: {},
      header: '',
      show: false
    }
    this.handleClick = this.handleClick.bind(this)
    this.closeModal = this.closeModal.bind(this)
  }
  handleClick (e) {
    const newState = Object.assign({}, this.state, {show: true})
    newState.header = e.target.value
    newState.body = (newState.header === 'Login') ? <LoginPage /> : <RegisterPage />
    this.setState(newState)
  }
  componentWillMount () {
    const routeOptions = ['login', 'signup']
    const route = window.location.href.substring('http://127.0.0.1:3000/main/'.length)
    console.log(window.location.href)
    console.log(route.replace('http://127.0.0.1:3000/main/', '-'))
    if (routeOptions.includes(route)) {
      const newState = Object.assign({}, this.state, {show: true})
      newState.header = route.charAt(0).toUpperCase() + route.slice(1)
      newState.body = (newState.header === 'Login') ? <LoginPage /> : <RegisterPage />
      this.setState(newState)
    }
  }
  closeModal () {
    const newState = Object.assign({}, this.state, {show: false})
    this.setState(newState)
    browserHistory.push('/main/')
  }
  render () {
    return (
      <Nav>
        <Button onClick={this.handleClick} value="Sign Up" type="submit">Sign Up</Button>
        {" "}
        <Button onClick={this.handleClick} value="Login" type="submit">Login</Button>
        <MainModal show={this.state.show} body={this.state.body}
          header={this.state.header} onHide={this.closeModal} />
      </Nav>
    )
  }
}

export default AuthenticationNav
