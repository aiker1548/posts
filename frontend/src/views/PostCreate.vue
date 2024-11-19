<template>
    <div class="post-create">
      <div class="post-header">
      </div>
      <input v-model="post.title" class="post-title" placeholder="Введите заголовок..." />
      <textarea v-model="post.content" class="post-input" placeholder="Напишите что-то..."></textarea>
      <circle-indicator :selectedTags="post.post_tags"></circle-indicator>
      
      <div class="file-upload">
        <label for="image-upload" class="option-button">Выберите фото/видео</label>
        <input id="image-upload" type="file" @change="handleImageUpload" accept="image/*" hidden />
        <span v-if="selectedImage" class="file-name">Выбрано: {{ selectedImage.name }}</span>
      </div>
  
      <div class="post-footer">
        <button class="publish-button" @click="createPost">Опубликовать</button>
      </div>
    </div>
  </template>
  
  <script>
  import CircleIndicator from '@/components/CircleIndicator.vue';
  import { createPostWithImage } from '@/api/posts';
  
  export default {
    name: 'PostCreate',
    components: {
      CircleIndicator,
    },
    data() {
      return {
        post: {
          title: '',
          content: '',
          post_tags: [],
          author_id: this.userId,
        },
        selectedImage: null, // Выбранное изображение
      };
    },
    props: {
      userId: {
        type: Number,
        required: true,
      },
    },
    methods: {
      handleImageUpload(event) {
        const file = event.target.files[0];
        if (file) {
          this.selectedImage = file;
        }
      },
      async createPost() {
        if (!this.post.title || !this.post.content) {
          alert('Введите заголовок и содержание поста!');
          return;
        }
  
        const formData = new FormData();
        formData.append('title', this.post.title);
        formData.append('content', this.post.content);
        formData.append('author_id', this.post.author_id);
        if (this.selectedImage) {
          formData.append('image', this.selectedImage);
        }
  
        try {
          const response = await createPostWithImage(formData);
          console.log('Пост успешно создан', response);
          this.$router.push('/myposts'); // Перенаправление после создания поста
        } catch (error) {
          console.error('Ошибка при создании поста', error);
          alert('Ошибка при создании поста. Попробуйте снова.');
        }
      },
    },
  };
  </script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap');

body {
    font-family: 'Roboto', sans-serif; /* Используем мягкий шрифт Roboto */
}

/* Остальные стили остаются такими же */
.file-upload {
  margin: 10px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}
.file-name {
  font-size: 14px;
  color: #555;
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
