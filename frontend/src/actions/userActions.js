import {
  LOAD_INFLUENTIAL_USERS_SUCCESS
} from './actionTypes'
import { parseJSON } from '../utils/misc'
import {
  getInfluentialUsers
} from '../utils/http_functions'

export function loadInfluentialUsersSuccess (users) {
  return {
    type: LOAD_INFLUENTIAL_USERS_SUCCESS,
    payload: {
      users: users
    }
  }
}

export function loadInfluentialUsers () {
  return function (dispatch) {
    return getInfluentialUsers()
    .then(parseJSON)
    .then(response => {
      dispatch(loadInfluentialUsersSuccess(response.users))
    }).catch(error => {
      throw (error)
    })
  }
}
