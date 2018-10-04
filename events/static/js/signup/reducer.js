import {INIT, UPDATE_PARTICIPANT, UPDATE_TEAM} from "./actions";

const initialState = {
  teams: {},
  participant: {}
};

const reducer = (state = initialState, {type, payload}) => {
  switch (type) {
    case INIT:
      return payload;
    case UPDATE_PARTICIPANT:
      return {
        ...state,
        participant: {
          ...state.participant,
          ...payload.participant
        }
      };
    case UPDATE_TEAM:
      return {
        ...state,
        teams: {
          ...state.teams,
          [payload.team.id]: {
            ...payload.team
          }
        }
      };
    default:
      return state;
  }
};

export default reducer;