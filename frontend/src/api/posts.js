import axios from 'axios';

export const getPosts = async () => {
    const response = await axios.get('http://localhost:8000/posts/all');
    return response.data;
};

export const getPostById = async (id) => {
    const response = await axios.get(`http://localhost:8000/posts/${id}`);
    return response.data;
};

export const createPost = async (post) => {
    const response = await axios.post('http://localhost:8000/posts/create', post);
    return response.data;
};

export const updatePost = async (id, post) => {
    const response = await axios.put(`http://localhost:8000/posts/${id}`, post);
    return response.data;
};

export const deletePost = async (id) => {
    const response = await axios.delete(`http://localhost:8000/posts/${id}`);
    return response.data;
};

export const getPostsByUser = async (id) => {
    const response = await axios.get(`http://localhost:8000/posts/user/${id}`);
    return response.data;
};
