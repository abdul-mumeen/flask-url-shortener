import React, {Component, PropTypes} from 'react'
import {NavDropdown, MenuItem} from 'react-bootstrap'

class UserDetailNav extends Component {
  render () {
    return (
      <NavDropdown eventKey={3} title="Olasode Mumeen" id="basic-nav-dropdown">
        <MenuItem eventKey={3.1}>User Profile</MenuItem>
        <MenuItem eventKey={3.2}>Settings</MenuItem>
        <MenuItem divider />
        <MenuItem eventKey={3.3}>Logout</MenuItem>
      </NavDropdown>
    )
  }
}

export default UserDetailNav
