import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'
import {Panel, ListGroup, ListGroupItem} from 'react-bootstrap'
import * as userActions from '../../actions/userActions'

class InfluentialUsersPanel extends Component {
  constructor (props) {
    super(props)
  }

  componentWillMount () {
    this.props.loadInfluentialUsers()
  }

  render () {
    const {influentialUsers} = this.props
    console.log(influentialUsers)
    return (
      <Panel collapsible defaultExpanded header="Influential Users">
        <ListGroup fill>
          {influentialUsers.map(influentialUser =>
            <ListGroupItem key={influentialUser.first_name}>
              {influentialUser.first_name}{" "}{influentialUser.last_name}
            </ListGroupItem>)}
        </ListGroup>
      </Panel>
    )
  }
}

InfluentialUsersPanel.propTypes = {
  influentialUsers: PropTypes.array.isRequired
}

function mapStateToProps (state, ownProps) {
  console.log(state.users.influentialUsers)
  return {
    influentialUsers: state.users.influentialUsers
  }
}

function mapDispatchToProps (dispatch) {
  return bindActionCreators(userActions, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(InfluentialUsersPanel)
