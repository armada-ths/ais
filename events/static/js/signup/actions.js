export const INIT = 'INIT';
export const SET_TEAMS = 'SET_TEAMS';
export const UPDATE_PARTICIPANT = 'UPDATE_PARTICIPANT';

export const init = (participant, teams) => ({
  type: INIT,
  participant,
  teams
});

export const updateParticipant = (participant) => ({
  type: UPDATE_PARTICIPANT,
  participant
});

export const setTeams = (teams) => ({
  type: SET_TEAMS,
  teams
});
