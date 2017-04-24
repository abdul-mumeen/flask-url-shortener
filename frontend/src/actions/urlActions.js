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
} from './actionTypes'
import { parseJSON } from '../utils/misc'
import {
  getPopularUrls, getMostRecentUrls, shortenLongUrl,
  visitUrl, redirectToRoute
} from '../utils/http_functions'

export function updateState (newState) {
  return {
    type: UPDATE_STATE,
    payload: {
      newState
    }
  }
}

export function shortenLongUrlSuccess (shortUrl) {
  return {
    type: SHORTEN_LONG_URL_SUCCESS,
    payload: {
      shortUrl
    }
  }
}

export function shortenLongUrlFailure (errorMessage) {
  return {
    type: SHORTEN_LONG_URL_FAILURE,
    payload: {
      errorMessage
    }
  }
}

export function shortenLongUrlUserSuccess (shortUrl, info) {
  return {
    type: SHORTEN_LONG_URL_USER_SUCCESS,
    payload: {
      shortUrl,
      info
    }
  }
}

export function shortenLongUrlUserFailure (errorMessage) {
  return {
    type: SHORTEN_LONG_URL_USER_FAILURE,
    payload: {
      errorMessage
    }
  }
}

export function loadPopularUrlSuccess (popular_urls) { // eslint-disable-line
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
      const popular_urls = [{short_url: 'No URL on this list'}]
      dispatch(loadPopularUrlSuccess(popular_urls))
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
      const recents = [{short_url: 'No URL on this list'}]
      dispatch(loadMostRecentUrlSuccess(recents))
    })
  }
}

export function shortenUrl (longUrl, vanity) {
  return function (dispatch) {
    return shortenLongUrl(longUrl, vanity)
    .then(parseJSON)
    .then(response => {
      if (localStorage.getItem('token'))
      {
        const info = response.info ? response.info : null
        dispatch(shortenLongUrlUserSuccess(response.url.short_url, info))
      } else {
        console.log(response)
        dispatch(shortenLongUrlSuccess(response.url.short_url))
      }
    }).catch(error => {
      if (localStorage.getItem('token'))
      {
        dispatch(shortenLongUrlUserFailure(error.response.data.message[0]))
      } else {
        console.log(error.response.data.message[0])
        dispatch(shortenLongUrlFailure(error.response.data.message[0]))
      }
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
