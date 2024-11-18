<template>
    <div>
        <PostList :posts="posts" />
    </div>
</template>

<script>
import PostList from '@/components/PostList.vue'
import { getPostsByUser } from '@/api/posts'

export default {
    components: {
        PostList
    },
    name: 'MyPosts',
    data() {
        return {
            posts: []
        }
    },
    props: {
        userId: {
            type: Number,
            required: true
        }
    },
    async created() {
        try {
            this.posts = await getPostsByUser(this.userId)
            console.log(this.posts[0]) // Теперь posts будет заполнен после загрузки данных
        } catch (error) {
            console.error("Ошибка при получении постов:", error)
        }
    }

}

</script>

<style scoped>

</style>
