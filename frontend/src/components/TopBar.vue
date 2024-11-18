<template>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@400;500&display=swap" rel="stylesheet">

    <div class="top-bar">
        <div class="top-bar-left">
            <router-link to="/home" class="blog-title" >blog</router-link>
            <router-link to="/myposts">Мои посты</router-link>
            <router-link to="/createpost">Создать пост</router-link>
        </div>
        <div class="top-bar-right">
            <ProfileMenu @logoutEvent="logout"/>
        </div>
    </div>
</template>

<script>
import ProfileMenu from './ProfileMenu.vue'

export default {
    name: 'TopBar',
    components: {
        ProfileMenu
    },
    methods: {
        logout() {
            this.$emit('logoutEvent')
        }
    }
}
</script>

<style scoped>
.top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: #f8f8f8;
}

.top-bar-left h1 {
    margin: 0;
}

.top-bar-right {
    display: flex;
    align-items: center;
    flex-grow: 1; /* Добавлено: позволяет правой части расширяться */
    justify-content: flex-end; /* Добавлено: выравнивает содержимое по правому краю */
}

.blog-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    font-weight: 700;
    color: #333;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    letter-spacing: 1px;
    margin: 0;
    padding: 10px 0;
}

.top-bar-left a {
    display: inline-block; 
    align-items: center;
    justify-content: center;
    margin-left: 20px;
    text-decoration: none;
    color: #333;
    font-weight: 500;
}

</style>
