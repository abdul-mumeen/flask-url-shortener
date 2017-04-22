import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'
import {Panel, ListGroup, ListGroupItem} from 'react-bootstrap'
import * as urlActions from '../../actions/urlActions'

class PopularUrlPanel extends Component {
  constructor (props) {
    super(props)
  }

  componentWillMount () {
    this.props.loadPopularUrls()
  }

  render () {
    const {popularUrls} = this.props
    return (
      <Panel collapsible defaultExpanded header="Popular URLs">
        <ListGroup fill>
          {popularUrls.map(popularUrl =>
            <ListGroupItem key={popularUrl.short_url}>{popularUrl.short_url}</ListGroupItem>)}
        </ListGroup>
      </Panel>
    )
  }
}

PopularUrlPanel.propTypes = {
  popularUrls: PropTypes.array.isRequired
}

function mapStateToProps (state, ownProps) {
  return {
    popularUrls: state.urls.popularUrls
  }
}

function mapDispatchToProps (dispatch) {
  return bindActionCreators(urlActions, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(PopularUrlPanel)
