
import { createReducer } from '../utils/misc'
import {
  LOAD_POPULAR_URL_SUCCESS,
  LOAD_MOST_RECENT_URL_SUCCESS,
  GET_ROUTE_TO_REDIRECT_SUCCESS,
  GET_ROUTE_TO_REDIRECT_FAILURE,
  SHORTEN_LONG_URL_SUCCESS,
  SHORTEN_LONG_URL_FAILURE,
  SHORTEN_LONG_URL_USER_FAILURE,
  SHORTEN_LONG_URL_USER_SUCCESS,
  UPDATE_STATE
} from '../actions/actionTypes'

const initialState = {
  popularUrls: [],
  mostRecentUrls: [],
  visitDetails: {
    route: null,
    errorMessage: ''
  },
  shortUrl: '',
  shortened: false,
  displayStatusText: false,
  shortenStatusText: 'Enter a valid URL'
}

export default createReducer(initialState, {
  [LOAD_POPULAR_URL_SUCCESS]: (state, payload) => (
      Object.assign({}, state, {
        popularUrls: payload.popular_urls
      })
    ),
  [LOAD_MOST_RECENT_URL_SUCCESS]: (state, payload) => (
      Object.assign({}, state, {
        mostRecentUrls: payload.recents
      })
    ),
  [GET_ROUTE_TO_REDIRECT_SUCCESS]: (state, payload) => (
      Object.assign({}, state, {
        visitDetails: {
          route: payload.long_url,
          errorMessage: ''
        }
      })
    ),
  [GET_ROUTE_TO_REDIRECT_FAILURE]: (state, payload) => (
      Object.assign({}, state, {
        visitDetails: {
          route: null,
          errorMessage: payload.message
        }
      })
    ),
  [SHORTEN_LONG_URL_SUCCESS]: (state, payload) => (
      Object.assign({}, state, {
        shortUrl: payload.shortUrl,
        shortened: true,
        displayStatusText: true,
        shortenStatusText: ''
      })
    ),
  [SHORTEN_LONG_URL_FAILURE]: (state, payload) => (
      Object.assign({}, state, {
        shortenStatusText: payload.errorMessage,
        displayStatusText: true
      })
    ),
  [UPDATE_STATE]: (state, payload) => (
      Object.assign({}, state, payload.newState)
    )
})
