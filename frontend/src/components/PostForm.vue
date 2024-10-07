<template>
    <div class="post-form">
        <h2>Создать новый пост</h2>
        <form @submit.prevent="createPost">
            <input type="text"
             placeholder="Заголовок" 
             class="post-form__input" 
             v-model="post.title">
            
            <textarea
             placeholder="Содержание" 
             class="post-form__input" 
             v-model="post.content"></textarea>
            
             <button type="submit">Создать</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    props: {
        userId: {
            type: Number,
            required: true
        }
    },
    data() {
        return {
            post: {
                title: '',
                content: '',
                author_id: this.userId
            }
        }
    },
    methods: {
        async createPost() {
            try {
                const response = await axios.post('http://localhost:8000/posts', this.post)
                this.post.title = ''
                this.post.content = ''
                this.$emit('post-created', response.data)
            } catch (error) {
                console.error('Ошибка при создании поста:', error)
            }
        }
    }
}
</script>

<style scoped>

</style>