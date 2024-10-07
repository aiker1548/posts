<template>
    <div class="post-list">
        <post-index v-for="post in posts" :key="post.id" :post="post" @delete-post="deletePost"/>
    </div>
</template>

<script>
import PostIndex from './PostIndex.vue'
import axios from 'axios'


export default {
    name: 'PostList',
    components: {
        PostIndex
    },
    data() {
        return {
            posts: []
        }
    },
    created() {
        this.fetchPosts()
    },
    methods: {
        deletePost(id) {
            this.$emit('delete-post', id)
            this.posts = this.posts.filter(post => post.id !== id)
        },
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
    }
}
</script>

<style scoped>



</style>