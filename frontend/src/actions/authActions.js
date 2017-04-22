import { browserHistory } from 'react-router'

import {
    LOGIN_USER_SUCCESS,
    LOGIN_USER_FAILURE,
    LOGIN_USER_REQUEST,
    LOGOUT_USER,
    REGISTER_USER_FAILURE,
    REGISTER_USER_REQUEST,
    REGISTER_USER_SUCCESS
} from './actionTypes'

import { parseJSON } from '../utils/misc'
import { getToken, createUser } from '../utils/http_functions'

export function loginUserSuccess (token) {
  localStorage.setItem('token', token)
  return {
    type: LOGIN_USER_SUCCESS,
    payload: {
      token
    }
  }
}

export function loginUserFailure (error) {
  localStorage.removeItem('token')
  return {
    type: LOGIN_USER_FAILURE,
    payload: {
      status: error.response.status,
      statusText: error.response.statusText
    }
  }
}

export function loginUserRequest () {
  return {
    type: LOGIN_USER_REQUEST
  }
}

export function logout () {
  localStorage.removeItem('token')
  return {
    type: LOGOUT_USER
  }
}

export function logoutAndRedirect () {
  return (dispatch) => {
    dispatch(logout())
    browserHistory.push('/')
  }
}

export function redirectToRoute (route) {
  return () => {
    browserHistory.push(route)
  }
}

export function loginUser (email, password) {
  return function (dispatch) {
    dispatch(loginUserRequest())
    return getToken(email, password)
      .then(parseJSON)
      .then(response => {
        try {
          // dispatch(getUserData(response.token))
          dispatch(loginUserSuccess(response.token))
          browserHistory.push('/main/about')
        } catch (e) {
          alert(e)
          dispatch(loginUserFailure({
            response: {
              status: 403,
              statusText: 'Invalid token'
            }
          }))
        }
      })
      .catch(error => {
        dispatch(loginUserFailure({
          response: {
            status: error.response.data.status_code,
            statusText: error.response.data.message
          }
        }))
      })
  }
}

export function registerUserRequest () {
  return {
    type: REGISTER_USER_REQUEST
  }
}

export function registerUserSuccess (token) {
  localStorage.setItem('token', token)
  return {
    type: REGISTER_USER_SUCCESS,
    payload: {
      token
    }
  }
}

export function registerUserFailure (error) {
  localStorage.removeItem('token')
  return {
    type: REGISTER_USER_FAILURE,
    payload: {
      status: error.response.status,
      statusText: error.response.statusText
    }
  }
}

export function registerUser (firstName, lastName, email, password, confirmPassword) {
  return function (dispatch) {
    dispatch(registerUserRequest())
    return createUser(firstName, lastName, email, password, confirmPassword)
      .then(parseJSON)
      .then(response => {
        try {
          dispatch(registerUserSuccess(response.token))
          browserHistory.push('/main')
        } catch (e) {
          dispatch(registerUserFailure({
            response: {
              status: 403,
              statusText: 'Invalid token'
            }
          }))
        }
      })
      .catch(error => {
        dispatch(registerUserFailure({
          response: {
            status: error,
            statusText: 'User with that email already exists'
          }
        }
        ))
      })
  }
}
