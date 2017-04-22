import React, {Component, PropTypes} from 'react'
import NavBar from './common/NavBar'

class App extends Component {
  render () {
    return (
      <div className="container-fluid">
        <NavBar />
        {this.props.children}
      </div>
    )
  }
}

App.propTypes = {
  children: PropTypes.object.isRequired
}

export default App
