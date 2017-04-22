import { combineReducers } from 'redux'
import { routerReducer } from 'react-router-redux'
import auth from './authReducer'
import urls from './urlReducer'

const rootReducer = combineReducers({
  routing: routerReducer,
  /* your reducers */
  auth,
  urls
})

export default rootReducer
