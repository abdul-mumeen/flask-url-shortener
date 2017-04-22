import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'
import {Link, browserHistory} from 'react-router'
import {Navbar, Nav, NavItem} from 'react-bootstrap'
import AuthenticationNav from './AuthenticationNav'
import UserDetailNav from './UserDetailNav'

class NavBar extends Component {
  constructor (props) {
    super(props)
    this.state = {
      user: {},
      isAuthenticated: true
    }
  }

  render () {
    return (
      <Navbar inverse collapseOnSelect>
        <Navbar.Header>
          <Navbar.Brand>
            <a href="#">Flask React Url Shortener</a>
          </Navbar.Brand>
          <Navbar.Toggle />
        </Navbar.Header>
        <Navbar.Collapse>
          <Nav>
            <NavItem eventKey={1}onClick={() => { browserHistory.push('/main/') }}>Home</NavItem>
            <NavItem eventKey={2} href="#">URLs</NavItem>
            <NavItem eventKey={3} onClick={() => { browserHistory.push('/main/about') }}>About</NavItem>
            <NavItem eventKey={4} href="#">Contact Us</NavItem>
          </Nav>
          <Nav pullRight>
            {
              !this.props.isAuthenticated ? <AuthenticationNav /> : <UserDetailNav userName={this.props.userName} />
            }
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    )
  }
}

function mapStateToProps (state) {
  return {
    isAuthenticated: state.auth.isAuthenticated,
    statusText: state.auth.statusText,
    userName: state.auth.userName
  }
}

export default connect(mapStateToProps)(NavBar)
