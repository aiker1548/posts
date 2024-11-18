import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import Login from '@/views/Login.vue';
import MyPosts from '@/views/MyPosts.vue';
import PostCreate from '@/views/PostCreate.vue';
const routes = [
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/myposts',
    name: 'MyPosts',
    component: MyPosts
  },
  {
    path: '/createpost',
    name: 'CreatePost',
    component: PostCreate
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;