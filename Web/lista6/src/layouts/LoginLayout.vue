<template>
    <div class="layout">
        <NavbarLogin />
        <router-view />
    </div>
</template>

<script>
import NavbarLogin from '@/components/NavbarLogin.vue';

export default {
    components: {
        NavbarLogin
    }
};
</script>

<style scoped>
.layout {
    display: flex;
    flex-direction: column;
    height: 100vh;
}

.content-wrapper {
    display: flex;
    flex: 1;
}

.content {
    flex-grow: 1;
    padding: 20px;
}
</style>