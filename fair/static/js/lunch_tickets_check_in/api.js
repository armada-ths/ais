import axios from 'axios';
import Cookie from 'js-cookie';

const client = axios.create({
  baseURL: '/api',
  withCredentials: true,
  headers: {
    "X-CSRFToken": Cookie.get('csrftoken')
  }
});

export const search = (query) => {
  return client.get(`fair/lunchtickets/search?query=${query}`)
};

/*

export const checkIn = (eventId, participantId) => {
  return client.post(`events/${eventId}/check_in/${participantId}`);
};

export const checkOut = (eventId, participantId) => {
  return client.post(`events/${eventId}/check_out/${participantId}`);
};

export const getByCheckInToken = (eventId, checkInToken) => {
  return client.post(`events/${eventId}/get_by_token/${checkInToken}`);
};

*/
