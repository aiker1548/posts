<template>
  <div class="home">
    <PostList :posts="posts"/>
  </div>
</template>

<script>

import PostList from '@/components/PostList.vue';
import axios from 'axios'

export default {
  name: 'Home',
  components: {
    PostList
  },
  props: {
    isLoggedIn: {
      type: Boolean,
      required: true
    },
  },
  data() {
    return {
      posts: []
    }
  },
  methods: {
    async fetchPosts() {
      try {
        const response = await axios.get('http://localhost:8000/posts')
        this.posts = response.data
      } catch (error) {
        console.error('Ошибка при загрузке постов:', error)
      }
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' }
      return new Date(dateString).toLocaleDateString('ru-RU', options)
    }
  },
  mounted() {
    if (!this.isLoggedIn) {
      this.$router.push('/login')
      console.log('Вы не авторизованы')
    }
    this.fetchPosts()
  }
}
</script>

<style scoped>
.post-container {
  max-width: 80%;
  margin: 0;
  padding: 20px;
}

.post-grid {
  display: flex;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  flex-direction: column;
}

.post {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}



/* ... другие стили ... */
</style>