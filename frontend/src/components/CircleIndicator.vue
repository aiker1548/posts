<template>
    <div class="tag-container">
        <div :style="{ maxHeight: showAllTags ? `${tags.length * 40}px` : '100px' }" class="tags">
            <div
                v-for="tag in (showAllTags ? tags : visibleTags)" 
                :key="tag.id" 
                class="tag"
                :class="{ active: selectedTags.includes(tag) }"
                @click="toggleTag(tag)"
            >
                {{ tag.name }}
            </div>
            <button @click="toggleShowAll">{{ showAllTags ? 'Скрыть' : 'Еще' }}</button>
        </div> <!-- Кнопка для переключения -->
    </div>
</template>

<script>
import { getTags } from '@/api/tags';

export default {
    name: 'TagSelector',
    data() {
        return {
            tags: [], // Список тегов
            showAllTags: false, // Переменная для управления отображением всех тегов
            visibleTags: [], // Массив для хранения видимых тегов
            modelValue: [] // Массив для хранения выбранных тегов
        };
    },
    props: {
        selectedTags: {
            type: Array,
            required: true
        }
    },
    created() {
        this.fetchTags();
    },
    mounted() {
        this.calculateVisibleTags();
        window.addEventListener('resize', this.calculateVisibleTags);
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.calculateVisibleTags);
    },
    methods: {
        toggleTag(tag) {
            const index = this.selectedTags.indexOf(tag);
            console.log(this.selectedTags)
            if (index === -1) {
                this.selectedTags.push(tag); // Добавление тега
            } else {
                this.selectedTags.splice(index, 1); // Удаление тега
            }
        },
        toggleShowAll() {
            this.showAllTags = !this.showAllTags;
        },
        fetchTags() {
            getTags().then(tags => {
                this.tags = tags;
                this.calculateVisibleTags(); // Обновляем видимые теги после загрузки
            });
        },
        calculateVisibleTags() {
            const containerWidth = this.$el.querySelector('.tags').clientWidth;
            const tagWidth = containerWidth*0.16; // Ширина одного тега (можно настроить)
            const tagsInRow = Math.floor(containerWidth / tagWidth);
            this.visibleTags = this.tags.slice(0, tagsInRow);
        },
    }
}
</script>

<style scoped>
.tag-container {
    display: flex; /* Блочное расположение элементов */
    flex-direction: column; /* Вертикальное расположение */
    gap: 10px; /* Отступ между элементами */
}

.tags {
    display: flex; /* Блочное расположение тегов */
    flex-wrap: wrap; /* Перенос на новую строку при необходимости */
    gap: 10px; /* Отступ между тегами */
}

button {
    align-self: flex-start; /* Кнопка выравнивается по левому краю */
    margin-top: 10px; /* Отступ сверху от тегов */
    background-color: transparent; /* Сделать кнопку прозрачной */
    border: none; /* Удалить границу кнопки */
}

.tags {
    overflow: hidden; /* Скрываем переполнение */
    transition: max-height 0.5s ease; /* Плавный переход для высоты */
    max-height: 100px; /* Максимальная высота для скрытых тегов */
}

.tag {
    padding: 10px 15px;
    border: 2px solid #bbb; /* Светлая граница, аналогичная .post-input */
    border-radius: 15px; /* Закругленные углы */
    cursor: pointer;
    transition: background-color 0.3s, border-color 0.3s;
}

.tag.active {
    background-color: #679ef1;
    border-color: #ffffff;
    color: #ffffff;
}
</style>