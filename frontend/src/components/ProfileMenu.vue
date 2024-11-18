<template>
    <div class="profile-menu" @mouseenter="showMenu" @mouseleave="hideMenu">
      <!-- Блок с иконкой профиля -->
      <div class="profile-icon-wrapper">
        <img :src="profileIcon" alt="Профиль" class="profile-icon" />
      </div>

      <!-- Меню -->
      <ul v-if="isMenuVisible" class="menu-dropdown">
        <li><router-link to="/profile">Профиль</router-link></li>
        <li><a href="#" @click="logout">Выход</a></li>
      </ul>
    </div>
  </template>
  
  <script>
  import profileIcon from '@/assets/userIcon.jpg'; // Импортируем изображение

  export default {
    data() {
      return {
        isMenuVisible: false, // Контролирует видимость меню
        profileIcon // Добавляем в data
      };
    },
    methods: {
      showMenu() {
        this.isMenuVisible = true;
      },
      hideMenu() {
        this.isMenuVisible = false;
      },
      logout() {
        this.$emit('logoutEvent');
        console.log('Выход');
      }
    }
  }
  </script>
  
  <style scoped>
  .profile-menu {
    position: relative;
    display: inline-block;
  }
  
  .profile-icon-wrapper {
    cursor: pointer;
    padding: 5px;
    background-color: #f0f0f0;
    border-radius: 50%;
  }
  
  .profile-icon {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: block;
  }
  
  .menu-dropdown {
    position: absolute;
    top: 60px; /* Позиционирование ниже иконки */
    right: 0;
    background-color: #fff;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 4px;
    list-style: none;
    padding: 10px;
    margin: 0;
    z-index: 100;
    width: 120px;
  }
  
  .menu-dropdown li {
    margin: 5px 0;
  }
  
  .menu-dropdown li a {
    text-decoration: none;
    color: #333;
    display: block;
    padding: 5px 10px;
  }
  
  .menu-dropdown li a:hover {
    background-color: #f0f0f0;
  }
  </style>
