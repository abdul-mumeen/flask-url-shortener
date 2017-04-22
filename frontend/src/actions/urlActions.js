import {
  LOAD_POPULAR_URL_SUCCESS,
  LOAD_MOST_RECENT_URL_SUCCESS,
  GET_ROUTE_TO_REDIRECT_SUCCESS,
  GET_ROUTE_TO_REDIRECT_FAILURE
} from './actionTypes'
import { parseJSON } from '../utils/misc'
import {
  getPopularUrls, getMostRecentUrls,
  visitUrl, redirectToRoute
} from '../utils/http_functions'

export function loadPopularUrlSuccess (popular_urls) {
  return {
    type: LOAD_POPULAR_URL_SUCCESS,
    payload: {
      popular_urls
    }
  }
}

export function loadMostRecentUrlSuccess (recents) {
  return {
    type: LOAD_MOST_RECENT_URL_SUCCESS,
    payload: {
      recents
    }
  }
}

export function getRouteToRedirectSuccess (long_url) {
  redirectToRoute(long_url)
  return {
    type: GET_ROUTE_TO_REDIRECT_SUCCESS,
    payload: {
      long_url
    }
  }
}

export function getRouteToRedirectFailure (message) {
  return {
    type: GET_ROUTE_TO_REDIRECT_FAILURE,
    payload: {
      message
    }
  }
}

export function loadPopularUrls () {
  return function (dispatch) {
    return getPopularUrls()
    .then(parseJSON)
    .then(response => {
      dispatch(loadPopularUrlSuccess(response.popular_urls))
    }).catch(error => {
      throw (error)
    })
  }
}

export function loadMostRecentUrls () {
  return function (dispatch) {
    return getMostRecentUrls()
    .then(parseJSON)
    .then(response => {
      dispatch(loadMostRecentUrlSuccess(response.recents))
    }).catch(error => {
      throw (error)
    })
  }
}

export function getRouteToRedirect (shortUrl) {
  return function (dispatch) {
    return visitUrl(shortUrl)
    .then(parseJSON)
    .then(response => {
      dispatch(getRouteToRedirectSuccess(response.long_url))
    })
    .catch(error => {
      dispatch(getRouteToRedirectFailure(error))
    })
  }
}
