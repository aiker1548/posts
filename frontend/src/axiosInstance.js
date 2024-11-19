import axios from 'axios';

// Создаем экземпляр Axios с базовым URL
const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000', // Задаем базовый URL
});

export default axiosInstance;