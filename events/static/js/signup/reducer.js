import {INIT, JOIN_TEAM, LEAVE_TEAM, SET_TEAMS, UPDATE_PARTICIPANT} from "./actions";

const initialState = {
  teams: {},
  participant: {
    signup_complete: false,
    fee_payed: false,
    team_id: null,
    is_team_leader: false,
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
    case LEAVE_TEAM:
      return {
        ...state,
        teams: action.teams,
        participant: {
          ...state.participant,
          team_id: null,
          is_team_leader: false,
        }
      };
    case JOIN_TEAM:
      return {
        ...state,
        teams: action.teams,
        participant: {
          ...state.participant,
          team_id: action.teamId,
          is_team_leader: false,
        }
      };
    case SET_TEAMS:
      return {
        ...state,
        teams: action.teams,
        participant: action.participant
      };
    default:
      return state;
  }
};

export default reducer;