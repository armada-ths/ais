import {INIT, SET_TEAMS, UPDATE_PARTICIPANT} from "./actions";

const initialState = {
  teams: {},
  participant: {
    signup_complete: false,
    fee_payed: false
  }
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case INIT:
      return {
        participant: {
          ...state.participant,
          ...action.participant
        },
        teams: {
          ...state.teams,
          ...action.teams,
        }
      };
    case UPDATE_PARTICIPANT:
      return {
        ...state,
        participant: {
          ...state.participant,
          ...action.participant
        }
      };
    case SET_TEAMS:
      return {
        ...state,
        teams: action.teams,
      };
    default:
      return state;
  }
};

export default reducer;