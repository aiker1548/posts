<template>
    <div class="post-index">
        <h3>{{ post.title }}</h3>
        <img 
            v-if="post.image_url" 
            :src="post.image_url" 
            alt="Post Image" 
            class="post-image" 
            @click="openImageModal(post.image_url)" 
        />
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

        <!-- Модальное окно для изображения
        <div 
            v-if="isModalOpen" 
            class="image-modal" 
            @click="closeImageModal"
        >
            <img :src="modalImageUrl" alt="Full Image" class="modal-image" />
        </div> -->
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
    data() {
        return {
            isModalOpen: false, // Состояние модального окна
            modalImageUrl: null // URL изображения для показа
        };
    },
    methods: {
        deletePost(id) {
            this.$emit('delete-post', id);
        },
        formatDate(dateString) {
            const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
            return new Date(dateString).toLocaleDateString('ru-RU', options);
        },
        openImageModal(imageUrl) {
            this.modalImageUrl = imageUrl;
            this.isModalOpen = true;
        },
        closeImageModal() {
            this.isModalOpen = false;
            this.modalImageUrl = null;
        }
    }
};
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

.post-index img {
    display: block;
    width: 300px; /* Фиксированная ширина */
    height: 200px; /* Фиксированная высота */
    object-fit: cover;
    margin: 16px 0;
    border-radius: 8px;
    cursor: pointer;
}

.no-image {
    color: #aaa;
    font-style: italic;
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

/* Модальное окно */
/* .image-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.image-modal img {
    max-width: 90%;
    max-height: 90%;
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
    animation: fadeIn 0.3s ease-in-out;
} */

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
</style>
