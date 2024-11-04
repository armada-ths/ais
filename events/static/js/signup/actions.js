export const INIT = 'INIT';
export const SET_TEAMS = 'SET_TEAMS';
export const LEAVE_TEAM = 'LEAVE_TEAM';
export const JOIN_TEAM = 'JOIN_TEAM';
export const UPDATE_PARTICIPANT = 'UPDATE_PARTICIPANT';
export const DEREGISTER = 'DEREGISTER';

export const init = (participant, teams) => ({
  type: INIT,
  participant,
  teams
});

export const updateParticipant = (participant) => ({
  type: UPDATE_PARTICIPANT,
  participant
});

export const setTeams = (teams, participant) => ({
  type: SET_TEAMS,
  teams,
  participant
});

export const leaveTeam = (teams) => ({
  type: LEAVE_TEAM,
  teams
});

export const joinTeam = (teams, teamId) => ({
  type: JOIN_TEAM,
  teams,
  teamId
});

export const deregister = (participant) => ({
  type: DEREGISTER,
  participant
});