<template>
  <div class="app">
    <div v-if="!isLoggedIn && !showRegistration" class="container">
      <div class="login-box">
        <h2>Авторизация</h2>
        <form @submit.prevent="login">
          <div class="input-box">
            <label for="email"><i class="fas fa-envelope"></i></label>
            <input type="email" id="email" v-model="email" placeholder="Email" required>
          </div>
          <div class="input-box">
            <label for="password"><i class="fas fa-lock"></i></label>
            <input type="password" id="password" v-model="password" placeholder="Пароль" required>
          </div>
          <button type="submit" class="btn">Войти</button>
        </form>
        <div class="register-link">
          <a href="#" @click="showRegistration = true" class="register-link__btn">Зарегистрироваться</a>
        </div>
      </div>
    </div>
    <div v-else-if="showRegistration" class="container">
      <div class="login-box">
        <h2>Регистрация</h2>
        <form @submit.prevent="register">
          <div class="input-box">
            <label for="username"><i class="fas fa-user"></i></label>
            <input type="text" id="username" v-model="username" placeholder="Имя пользователя" required>
          </div>
          <div class="input-box">
            <label for="reg-email"><i class="fas fa-envelope"></i></label>
            <input type="email" id="reg-email" v-model="email" placeholder="Email" required>
          </div>
          <div class="input-box">
            <label for="reg-password"><i class="fas fa-lock"></i></label>
            <input type="password" id="reg-password" v-model="password" placeholder="Пароль" required>
          </div>
          <button type="submit" class="btn">Зарегистрироваться</button>
        </form>
        <div class="register-link">
          <a href="#" @click="showRegistration = false">Уже есть аккаунт? Войти</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      username: ''
    }
  },
  methods: {
    login() {
      axios.post('http://localhost:8000/users/login', { email: this.email, password: this.password })
        .then(response => {
          this.$emit('login-success', response.data.user_id)
          this.$router.push('/')
        })
        .catch(error => {
          console.error('Ошибка при авторизации:', error)
        })

    },
    register() {
      axios.post('http://localhost:8000/users/register', { username: this.username, email: this.email, password: this.password })
        .then(response => {
          this.$emit('login-success', response.data.user_id)
          this.$router.push('/')
        })
        .catch(error => {
          console.error('Ошибка при регистрации:', error)
        })
    }
  }
}


</script>

<style scoped>
.login-box {
  width: 300px;
  margin: 20% auto;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
 
}

h2 {
  text-align: center;
  color: #333;
}

.input-box {
  width: calc(100% - 40px); /* Ширина 100% минус отступы слева и справа */
  position: relative;
  margin-bottom: 20px;
  margin-left: auto;
  margin-right: auto;
  padding: 0 20px; /* Отступы слева и справа */
}

input {
  width: 80%;
  padding: 12px 40px 12px 15px;
  border: 1px solid #ccc;
  border-radius: 25px;
  font-size: 16px;
  transition: all 0.3s ease;
  outline: none;
}

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

.btn:hover {
  background-color: #0056b3;
}

.register-link {
  text-align: center;
  margin-top: 20px;
}

.register-link a {
  color: #007bff;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}

</style>