import axios from 'axios';

// Base API client configuration (adjust the baseURL)
const apiClient = axios.create({
    baseURL: 'http://your-python-api-url.com/api', // replace with your actual API URL
    headers: {
        'Content-Type': 'application/json',
    },
});

// Fetch all messages
export const fetchMessages = async (contactId: string) => {
    try {
        const response = await apiClient.get(`/messages?contactId=${contactId}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching messages:', error);
        throw error;
    }
};

// Send a new message
export const sendMessage = async (contactId: string, message: string) => {
    try {
        const response = await apiClient.post('/messages', {
            contactId,
            message,
        });
        return response.data;
    } catch (error) {
        console.error('Error sending message:', error);
        throw error;
    }
};
