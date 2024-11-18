<template>
    <div class="post-list">
        <post-index v-for="post in posts" :key="post.id" :post="post" @delete-post="deletePost"/>
    </div>
</template>

<script>
import PostIndex from './PostIndex.vue'


export default {
    name: 'PostList',
    components: {
        PostIndex
    },
    data() {
        return {
         
        }
    },
    props: {
        posts: {
            type: Array,
            required: true
        }
    },
    methods: {
        deletePost(id) {
            this.$emit('delete-post', id)
            this.posts = this.posts.filter(post => post.id !== id)
        },
        
    }
}
</script>

<style scoped>



</style>