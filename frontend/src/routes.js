import React from 'react'
import { Route, IndexRoute } from 'react-router'
import App from './components/App'
import HomePage from './components/home/HomePage'
import AboutPage from './components/about/AboutPage'
import RedirectPage from './components/service/RedirectPage'

export default (
  <Route path="/main/" component={App}>
    <IndexRoute component={HomePage} />
    <Route path="/" component={RedirectPage} />
    <Route path="/:vs" component={RedirectPage} />
    <Route path="about" component={AboutPage} />
  </Route>
)
