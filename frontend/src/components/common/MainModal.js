import React, {Component, PropTypes} from 'react'
import {Modal} from 'react-bootstrap'

class MainModal extends Component {
  render () {
    return (
      <Modal {...this.props} bsSize="large" aria-labelledby="contained-modal-title-lg">
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-lg">{this.props.header}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {this.props.body}
        </Modal.Body>
      </Modal>
    )
  }
}

MainModal.propTypes = {
  header: PropTypes.string.isRequired,
  show: PropTypes.bool.isRequired,
  onHide: PropTypes.func.isRequired,
  body: PropTypes.object.isRequired
}

export default MainModal
