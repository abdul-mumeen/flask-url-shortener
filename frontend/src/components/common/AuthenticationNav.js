import React, {Component, PropTypes} from 'react'
import {Nav, Button} from 'react-bootstrap'
import MainModal from './MainModal'
import AboutPage from '../about/AboutPage'
import LoginPage from '../login/LoginPage'

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
    newState.body = (newState.header === 'Login') ? <LoginPage /> : <AboutPage />
    this.setState(newState)
  }

  closeModal () {
    const newState = Object.assign({}, this.state, {show: false})
    this.setState(newState)
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
