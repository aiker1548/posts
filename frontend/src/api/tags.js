import axiosInstance from '@/axiosInstance';

export const getTags = async () => {
    const response = await axiosInstance.get('/tags/all');
    return response.data;
};

