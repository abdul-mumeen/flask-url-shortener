import React, {Component} from 'react'
import {Link} from 'react-router'
import {Grid, Col, Row, Clearfix} from 'react-bootstrap'
import PopularUrlPanel from './PopularUrlPanel'
import MostRecentUrlPanel from './MostRecentUrlPanel'
import InfluentialUsersPanel from './InfluentialUsersPanel'

class HomePage extends Component {
  render () {
    return (
      <Grid fill>
        <Row>
          <div className="jumbotron">
            <h1>Flask and React URL Shortener Application</h1>
            <p>This is the place where the journey begins</p>
            <Link to="about" className="btn btn-primary btn-lg">Learn more</Link>
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
        <Row> foorurur</Row>
      </Grid>
    )
  }
}

export default HomePage
