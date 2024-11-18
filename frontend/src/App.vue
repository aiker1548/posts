<template>
  <div class="app">
    <TopBar @logout="logout" v-if="isLoggedIn" @logoutEvent="logout"/>
    <div class="app-layout">
      <Sidebar v-if="isLoggedIn" />
      <main class="main-content">
        <router-view 
          @login-success="handleLoginSuccess"
          :isLoggedIn="isLoggedIn"
          :userId="userId"
        ></router-view>
      </main>
    </div>
  </div>
</template>

<script>
import TopBar from './components/TopBar.vue';

export default {
  components: {
    TopBar
  },
  data() {
    return {
      isLoggedIn: false,
      userId: null // Добавьте это поле для хранения ID пользователя
    }
  },
  methods: {
    logout() {
      this.isLoggedIn = false
      this.userId = null // Очищаем ID пользователя при выходе
      this.$router.push('/login')
    },
    handleLoginSuccess(userId) {
      this.isLoggedIn = true
      this.userId = userId
    },
  }
}

</script>

<style>


.btn {
  width: 60%;
  padding: 10px;
  margin: 0 20%;
  background-color: #007bff;
  color: #ffffff;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

</style>