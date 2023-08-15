import axios from 'axios';
import Cookie from 'js-cookie';

const client = axios.create({
  baseURL: '/api/exhibitors',
  withCredentials: true,
  headers: {
    "X-CSRFToken": Cookie.get('csrftoken')
  }
});

export const createBooth = (locationId, boothName, boundaries) => {
  return client.post(`locations/${locationId}/create_booth`, {
    name: boothName,
    boundaries: boundaries
  });
};

