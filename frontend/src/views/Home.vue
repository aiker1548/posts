<template>
  <div class="home">
    <h1>Домашняя страница</h1>
    <PostList/>
  </div>
</template>

<script>

import PostList from '@/components/PostList.vue';

export default {
  name: 'Home',
  components: {
    PostList
  },
  props: {
    isLoggedIn: {
      type: Boolean,
      required: true
    }
  },

  mounted() {
    if (!this.isLoggedIn) {
      this.$router.push('/login')
      console.log('Вы не авторизованы')
    }
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
</style>