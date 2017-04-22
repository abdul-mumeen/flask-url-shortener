import {createStore, applyMiddleware, compose} from 'redux'
import rootReducer from '../reducers'
import reduxImmutableStateInvariant from 'redux-immutable-state-invariant'
import thunkMiddleware from 'redux-thunk'

export default function configureStore (initialState) {
  return createStore(
    rootReducer,
    initialState, compose(
    applyMiddleware(thunkMiddleware, reduxImmutableStateInvariant()),
  window.devToolsExtension ? window.devToolsExtension() : f => f)
  )
}
