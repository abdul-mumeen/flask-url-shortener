import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'
import { browserHistory } from 'react-router'
import {Panel, ListGroup, ListGroupItem} from 'react-bootstrap'
import * as urlActions from '../../actions/urlActions'

class RedirectPage extends Component {
  constructor (props, context) {
    super(props, context)
  }

  componentWillMount () {
    if (this.props.params.vs !== '') {
      const shortUrl = 'bit.ly/' + this.props.params.vs
      this.props.getRouteToRedirect(shortUrl)
    } else {
      browserHistory.push('/main/')
    }
  }

  displayErrorPage () {
    const {visitDetails} = this.props
    let errorPageHeader = ''
    switch (visitDetails.message) {
      case 'No matching URL found':
        errorPageHeader = 'No matching URL found!'
        break
      case 'URL has been deleted':
        errorPageHeader = 'URL has been deleted!'
        break
      case 'URL has been deactivated':
        errorPageHeader = 'URL has been deactivated!'
        break
      case '':
        errorPageHeader = ''
        break
      default:
        errorPageHeader = 'Bad request!'
    }
    return errorPageHeader
  }

  render () {
    return (
      <div>
        <h1>{this.displayErrorPage()}</h1>
      </div>
    )
  }
}

function mapStateToProps (state, ownProps) {
  return {
    visitDetails: state.urls.visitDetails
  }
}

function mapDispatchToProps (dispatch) {
  return bindActionCreators(urlActions, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(RedirectPage)
