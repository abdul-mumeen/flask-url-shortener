import { combineReducers } from 'redux'
import { routerReducer } from 'react-router-redux'
import auth from './authReducer'
import urls from './urlReducer'
import users from './userReducer'


const rootReducer = combineReducers({
  routing: routerReducer,
  /* your reducers */
  auth,
  urls,
  users
})

export default rootReducer
