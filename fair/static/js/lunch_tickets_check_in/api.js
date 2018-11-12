import axios from 'axios';
import Cookie from 'js-cookie';

const client = axios.create({
  baseURL: '/api/fair',
  withCredentials: true,
  headers: {
    "X-CSRFToken": Cookie.get('csrftoken')
  }
});

export const search = (query) => {
  return client.get(`lunchtickets/search?query=${query}`)
};

export const checkIn = (ticketId) => {
  return client.post(`lunchtickets/check_in/${ticketId}`);
};

export const checkOut = (ticketId) => {
  return client.post(`lunchtickets/check_out/${ticketId}`);
};

export const getByToken = (token) => {
  return client.get(`lunchtickets/get_by_token?token=${token}`);
};
