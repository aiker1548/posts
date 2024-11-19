import axiosInstance from '@/axiosInstance';

export const getPosts = async () => {
    const response = await axiosInstance.get('/posts/all');
    return response.data;
};

export const getPostById = async (id) => {
    const response = await axiosInstance.get(`/posts/${id}`);
    return response.data;
};

export const createPost = async (post) => {
    const response = await axiosInstance.post('/posts/create', post);
    return response.data;
};

export const updatePost = async (id, post) => {
    const response = await axiosInstance.put(`/posts/${id}`, post);
    return response.data;
};

export const deletePost = async (id) => {
    const response = await axiosInstance.delete(`/posts/${id}`);
    return response.data;
};

export const getPostsByUser = async (id) => {
    const response = await axiosInstance.get(`/posts/user/${id}`);
    return response.data;
};

export const createPostWithImage = (formData) => {
    return axiosInstance.post('/posts/create', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
}