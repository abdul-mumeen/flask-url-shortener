import React from 'react'
import { Route, IndexRoute } from 'react-router'
import App from './components/App'
import HomePage from './components/home/HomePage'
import AboutPage from './components/about/AboutPage'
import CoursesPage from './components/courses/CoursesPage'

export default (
  <Route path="/main/" component={App}>
    <IndexRoute component={HomePage} />
    <Route path="/" component={AboutPage} />
    <Route path="courses" component={CoursesPage} />
    <Route path="about" component={AboutPage} />
  </Route>
)
