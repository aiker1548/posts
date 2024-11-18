<template>
    <div class="post-create">
        <div class="post-header">

        </div>
        <input v-model="post.title" class="post-title" placeholder="Введите заголовок..." /> <!-- Добавлено поле для заголовка -->
        <textarea v-model="post.content" class="post-input" placeholder="Напишите что-то..."></textarea>
        <circle-indicator :selectedTags="post.post_tags"></circle-indicator>
        <div class="post-footer">
            <div class="post-options">
                <button class="option-button">Фото/Видео</button>
                <button class="option-button">Музыка</button>
            </div>
            <button class="publish-button" @click="createPost">Опубликовать</button>
        </div>
    </div>
</template>

<script>
import CircleIndicator from '@/components/CircleIndicator.vue';
import { createPost } from '@/api/posts';
export default {
    name: 'PostCreate',
    components: {
        CircleIndicator
    },
    data() {
        return {
            post: {
                title: '',
                content: '',
                post_tags: [],
                author_id: this.userId
            },
        }
    },
    created() {
        this.post.author_id = this.userId
    },
    props: {
        userId: {
            type: Number,
            required: true
        }
    },
    methods: {
        createPost() {
            console.log('Создание поста', this.post); // Вывод информации о посте, включая теги
            this.post.post_tags = this.post.post_tags.map(tag => tag.id)
            createPost(this.post).then(response => {
                console.log('Пост успешно создан', response);
            }).catch(error => {
                console.error('Ошибка при создании поста', error);
            });
            this.post.post_tags = []
            this.$router.push('/myposts')
        }
    }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap');

body {
    font-family: 'Roboto', sans-serif; /* Используем мягкий шрифт Roboto */
}

.post-create {
    background-color: #f8f8f8; /* Темный фон для формы */
    border-radius: 12px; /* Более закругленные углы */
    padding: 20px;
    width: 55%;
    margin: 20px auto;
    box-shadow: 0 4px 20px  #f8f8f8; /* Мягкая тень */
    border: 1px solid #bbb; /* Светлая граница */
}

.post-header {
    font-size: 20px; /* Увеличенный размер шрифта */
    font-weight: 500; /* Полужирный шрифт */
    color: #333; /* Темно-серый цвет для мягкости */
    margin-bottom: 10px;
}

.post-title {
    width: 100%;
    height: 40px; /* Высота поля заголовка */
    border: 1px solid #f8f8f8; /* Светлая граница */
    border-radius: 8px; /* Более закругленные углы */
    padding: 8px; /* Внутренний отступ */
    box-sizing: border-box;
    font-size: 16px; /* Увеличенный размер шрифта */
    color: #555; /* Мягкий цвет текста */
    background-color: #f8f8f8; /* Белый фон для текстового поля */
}

/* Убираем границу при наведении */
.post-title:hover {
    border: none; /* Убираем границу при наведении */
}

/* Убираем границу и обводку при фокусе */
.post-title:focus {
    border: none; /* Убираем границу при нажатии */
    outline: none; /* Убираем обводку при фокусе */
}

.post-input {
    width: 100%;
    height: 100px;
    border: 1px solid #f8f8f8; /* Светлая граница */
    border-radius: 8px; /* Более закругленные углы */
    padding: 12px; /* Увеличенный внутренний отступ */
    box-sizing: border-box;
    resize: none;
    font-size: 16px; /* Увеличенный размер шрифта */
    color: #555; /* Мягкий цвет текста */
    background-color: #f8f8f8; /* Белый фон для текстового поля */
}

/* Убираем границу при наведении */
.post-input:hover {
    border: none; /* Убираем границу при наведении */
}

/* Убираем границу и обводку при фокусе */
.post-input:focus {
    border: none; /* Убираем границу при нажатии */
    outline: none; /* Убираем обводку при фокусе */
}

.post-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;
}

.post-options {
    display: flex;
    gap: 10px;
}

.option-button {
    background-color: #cfe2ff; /* Светлый фон */
    border: none;
    border-radius: 8px; /* Более закругленные углы */
    padding: 10px 15px; /* Увеличенный внутренний отступ */
    cursor: pointer;
    transition: background-color 0.3s;
    font-size: 14px; /* Увеличенный размер шрифта */
    color: #007bff; /* Цвет текста */
}

.option-button:hover {
    background-color: #b6d4fe; /* Более светлый фон при наведении */
}

.publish-button {
    background-color: #0056b3; /* Темный цвет для кнопки публикации */
    color: white;
    border: none;
    border-radius: 8px; /* Более закругленные углы */
    padding: 10px 20px;
    cursor: pointer;
    transition: background-color 0.3s;
    font-size: 16px; /* Увеличенный размер шрифта */
}

.publish-button:hover {
    background-color: #004085; /* Темный цвет при наведении */
}
</style>
