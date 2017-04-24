import React, {Component, PropTypes} from 'react'
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'
import {Link} from 'react-router'
import {Grid, Col, Row, Clearfix, FormGroup, Form, Fade, ControlLabel, Collapse,
  Glyphicon, InputGroup, Button, FormControl} from 'react-bootstrap'
import PopularUrlPanel from './PopularUrlPanel'
import MostRecentUrlPanel from './MostRecentUrlPanel'
import InfluentialUsersPanel from './InfluentialUsersPanel'
import * as urlActions from '../../actions/urlActions'
import { validateUrl } from '../../utils/misc'

class HomePage extends Component {
  constructor (props) {
    super(props)
    this.state = {
      longUrl: '',
      shortUrl: '',
      shortened: false,
      displayStatusText: false,
      shortenStatusText: ''
    }
  }

  changeValue (e, type) {
    const value = e.target.value
    const nextState = {}
    nextState[type] = value
    nextState.displayStatusText = false
    nextState.shortened = false
    this.setState(nextState)
    this.props.updateState(nextState)
  }

  _handleKeyPress (e) {
    if (e.key === 'Enter') {
      this.shorten(e)
    }
  }

  componentWillReceiveProps (nextProps) {
    if (this.props !== nextProps) {
      this.setState({
        shortUrl: nextProps.shortUrl,
        shortened: nextProps.shortened,
        displayStatusText: nextProps.displayStatusText,
        shortenStatusText: nextProps.shortenStatusText
      })
    }
    console.log(this.state)
    console.log(this.props)
    console.log(nextProps)
  }

  shorten (e) {
    e.preventDefault()
    if (validateUrl(this.state.longUrl)) {
      this.props.shortenUrl(this.state.longUrl)
    } else {
      this.setState({
        displayStatusText: true,
        shortenStatusText: 'Enter a valid URL'
      })
    }
  }

  render () {
    return (
      <Grid fill>
        <Row>
          <div>
            <div className="text-center">
              <h1 className="center-block">FRUS</h1>
              <h3>This is the place where the journey begins</h3>
            </div>
            <div>
              <div className="col-sm-8 col-sm-offset-2">
                <Collapse in={this.state.displayStatusText}>
                  <div className="col-sm-8 col-sm-offset-2">
                    <FormGroup className="text-center">
                      <ControlLabel className="text-danger">{this.state.shortenStatusText}</ControlLabel>
                    </FormGroup>
                  </div>
                </Collapse>
                <Collapse in={this.state.shortened}>
                  <div className="col-sm-8 col-sm-offset-2">
                    <FormGroup >
                      <InputGroup>
                        <FormControl type="text" value={this.props.shortUrl} disabled />
                        <InputGroup.Button>
                          <Button><Glyphicon glyph="copy" /></Button>
                        </InputGroup.Button>
                      </InputGroup>
                    </FormGroup>
                  </div>
                </Collapse>
                <FormGroup controlId="formValidationSuccess1" validationState="success">
                  <InputGroup bsSize="large">
                    <FormControl type="text" bsStyle="success" className="text-success"
                      placeholder="http://www.example.com/gratitude/praises"
                      onChange={(e) => this.changeValue(e, 'longUrl')} />
                    <InputGroup.Button>
                      <Button bsStyle="success" onClick={(e) => this.shorten(e)}>Shorten</Button>
                    </InputGroup.Button>
                  </InputGroup>
                </FormGroup>
              </div>
            </div>
          </div>
        </Row>
        <Row className="show-grid">
          <Col sm={6} md={4}>
            <PopularUrlPanel />
          </Col>
          <Clearfix visibleSmBlock><code>&lt;{'Clearfix visibleSmBlock'} /&gt;</code></Clearfix>
          <Col sm={6} md={4}><MostRecentUrlPanel /></Col>
          <Col sm={6} md={4}><InfluentialUsersPanel /></Col>
        </Row>
      </Grid>
    )
  }
}

HomePage.propTypes = {
  shortUrl: PropTypes.string.isRequired,
  shortened: PropTypes.bool.isRequired,
  displayStatusText: PropTypes.bool.isRequired,
  shortenStatusText: PropTypes.string.isRequired,
  shortenUrl: PropTypes.func.isRequired
}

function mapStateToProps (state) {
  return {
    shortUrl: state.urls.shortUrl,
    shortened: state.urls.shortened,
    displayStatusText: state.urls.displayStatusText,
    shortenStatusText: state.urls.shortenStatusText
  }
}

function mapDispatchToProps (dispatch) {
  return bindActionCreators(urlActions, dispatch)
}

export default connect(mapStateToProps, mapDispatchToProps)(HomePage)
