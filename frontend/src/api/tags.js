import axios from 'axios';

export const getTags = async () => {
    const response = await axios.get('http://localhost:8000/tags/all');
    return response.data;
};

