
import { createReducer } from '../utils/misc'
import {
  LOAD_INFLUENTIAL_USERS_SUCCESS
} from '../actions/actionTypes'

const initialState = {
  influentialUsers: []
}

export default createReducer(initialState, {
  [LOAD_INFLUENTIAL_USERS_SUCCESS]: (state, payload) => (
      Object.assign({}, state, {
        influentialUsers: payload.users
      })
    )
})
