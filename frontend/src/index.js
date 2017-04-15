import 'babel-polyfill'
import React from 'react'
import { render } from 'react-dom'
import {Provider} from 'react-redux'
import { Router, browserHistory } from 'react-router'

render(
  <Provider >
    <Router history={browserHistory} />
  </Provider>,
  document.getElementById('app')
)
