<template>
    <div class="post-index">
        <h3>{{ post.title }}</h3>
        <img v-if="post.image_url" :src="post.image_url" alt="Post Image" class="post-image" />
        <p v-else class="no-image">Нет изображения</p>

        <p>{{ post.content }}</p>
        <p><small>Автор: {{ post.author_id }}</small></p>
        <p><small>Создано: {{ formatDate(post.created_at) }}</small></p>

        <!-- Кнопка скачивания фото -->
        <a 
            v-if="post.image_url" 
            :href="post.image_url" 
            download 
            class="download-button"
        >
            Скачать фото
        </a>

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
.post-index {
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 16px;
    margin: 16px 0;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
}

.post-index:hover {
    transform: scale(1.02);
}

.post-index h3 {
    font-size: 1.5em;
    color: #333;
    margin: 0 0 8px;
    text-transform: capitalize;
}

.post-index p {
    color: #555;
    line-height: 1.6;
    margin: 8px 0;
}

.post-index small {
    font-size: 0.85em;
    color: #888;
}

.post-index button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9em;
    transition: background-color 0.3s;
}

.post-index button:hover {
    background-color: #00Abff;
}

.post-index button:active {
    background-color: #ff1f1f;
}

.post-index img {
    display: block;
    width: 300px; /* Фиксированная ширина */
    height: 200px; /* Фиксированная высота */
    object-fit: cover; /* Устанавливает обрезку для заполнения рамки */
    margin: 16px 0;
    border-radius: 8px;
}

.post-index .no-image {
    color: #aaa;
    font-style: italic;
}
/* Стили кнопки скачивания */
.download-button {
    display: inline-block;
    background-color: #28a745;
    color: white;
    padding: 8px 12px;
    margin-top: 8px;
    border-radius: 4px;
    text-decoration: none;
    font-size: 0.9em;
    transition: background-color 0.3s ease;
}

.download-button:hover {
    background-color: #218838;
}

.download-button:active {
    background-color: #1e7e34;
}
</style>