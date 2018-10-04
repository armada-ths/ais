import axios from 'axios';
import Cookie from 'js-cookie';

const client = axios.create({
  baseURL: '/api',
  withCredentials: true,
  headers: {
    "X-CSRFToken": Cookie.get('csrftoken')
  }
});

const joinTeam = (eventId, teamId) => {
  return client.post(`events/${eventId}/teams/${teamId}`);
};

const createTeam = (eventId, teamName) => {
  return client.post(`events/${eventId}/teams`, {name: teamName});
};

export {joinTeam, createTeam};
