import {INIT, SET_TEAMS, UPDATE_PARTICIPANT} from "./actions";

const initialState = {
  teams: {},
  participant: {}
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case INIT:
      return {
        participant: action.participant,
        teams: action.teams,
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