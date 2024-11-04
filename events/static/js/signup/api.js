import axios from 'axios';
import Cookie from 'js-cookie';

const client = axios.create({
  baseURL: '/api',
  withCredentials: true,
  headers: {
    "X-CSRFToken": Cookie.get('csrftoken')
  }
});

export const joinTeam = (eventId, teamId) => {
  return client.post(`events/${eventId}/teams/${teamId}`);
};

export const leaveTeam = (eventId) => {
  return client.post(`events/${eventId}/teams/leave`);
};

export const createTeam = (eventId, teamName) => {
  return client.post(`events/${eventId}/teams/create`, {name: teamName});
};

export const updateTeam = (eventId, teamId, team) => {
  return client.post(`events/${eventId}/teams/${teamId}/update`, team);
};

export const deregister = (eventId, participantId) => {
  return client.post(`events/${eventId}/deregister/${participantId}`);
};
