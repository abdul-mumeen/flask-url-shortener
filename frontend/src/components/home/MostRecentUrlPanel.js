import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'
import {Panel, ListGroup, ListGroupItem} from 'react-bootstrap'
import * as urlActions from '../../actions/urlActions'

class MostRecentUrlPanel extends Component {
  constructor (props) {
    super(props)
  }

  componentWillMount () {
    this.props.loadMostRecentUrls()
  }

  render () {
    const {mostRecentUrls} = this.props
    return (
      <Panel collapsible defaultExpanded header="Recently Added URLs">
        <ListGroup fill>
          {mostRecentUrls.map(mostRecentUrl =>
            <ListGroupItem key={mostRecentUrl.short_url}>{mostRecentUrl.short_url}</ListGroupItem>)}
        </ListGroup>
      </Panel>
    )
  }
}

MostRecentUrlPanel.propTypes = {
  mostRecentUrls: PropTypes.array.isRequired
}

function mapStateToProps (state, ownProps) {
  return {
    mostRecentUrls: state.urls.mostRecentUrls
  }
}

function mapDispatchToProps (dispatch) {
  return bindActionCreators(urlActions, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(MostRecentUrlPanel)
