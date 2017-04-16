import React, {Component, PropTypes} from 'react'
import {Nav, Button} from 'react-bootstrap'
import MainModal from './MainModal'
import AboutPage from '../about/AboutPage'

class AuthenticationNav extends Component {
  constructor (props) {
    super(props)
    this.state = {
      body: {},
      header: '',
      attributes: {
        show: false
      },
      show: false
    }
  }
  handleClick (e) {
    const newState = Object.assign({}, this.state, {show: true})
    newState.header = e.target.value
    newState.body = (newState.header === 'Login') ? <AboutPage /> : <AboutPage />
    this.setState(newState)
  }

  closeModal () {
    const newState = Object.assign({}, this.state, {show: false})
    this.setState(newState)
  }

  render () {
    return (
      <Nav>
        <Button onClick={(e) => this.handleClick(e)} value="Sign Up" type="submit">Sign Up</Button>
        {" "}
        <Button onClick={(e) => this.handleClick(e)} value="Login" type="submit">Login</Button>
        <MainModal show={this.state.show} body={this.state.body}
          header={this.state.header} onHide={() => this.closeModal()} />
      </Nav>
    )
  }
}

export default AuthenticationNav
