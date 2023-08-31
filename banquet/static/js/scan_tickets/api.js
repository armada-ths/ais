import axios from 'axios';
import Cookie from 'js-cookie';

const client = axios.create({
  baseURL: '/api/banquet',
  withCredentials: true,
  headers: {
    "X-CSRFToken": Cookie.get('csrftoken')
  }
});

export const search = (query) => {
  return client.get(`tickets/search?query=${query}`)
};

export const checkIn = (ticketId) => {
  return client.post(`tickets/check_in/${ticketId}`);
};

export const checkOut = (ticketId) => {
  return client.post(`tickets/check_out/${ticketId}`);
};

export const checkInByToken = (token) => {
  return client.get(`tickets/check_in_by_token?token=${token}`);
};
