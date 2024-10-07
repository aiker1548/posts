<template>
    <div class="post-index">
        <h3>{{ post.title }}</h3>
        <p>{{ post.content }}</p>
        <p><small>Автор: {{ post.author_id }}</small></p>
        <p><small>Создано: {{ formatDate(post.created_at) }}</small></p>
        <button @click="deletePost(post.id)">Удалить</button>
    </div>
</template>

<script>
export default {
    name: 'PostIndex',
    props: {
        post: {
            type: Object,
            required: true
        }
    },
    methods: {
        deletePost(id) {
            this.$emit('delete-post', id)
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
