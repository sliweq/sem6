<template>
    <div class="layout">
        <div class="content-wrapper">
            <SidebarMain />
            <main class="content">
                <router-view />
            </main>
        </div>
        <FooterMain>
        </FooterMain>
    </div>
</template>

<script>
import FooterMain from '@/components/FooterMain.vue';
import SidebarMain from '@/components/SidebarMain.vue';

export default {
    components: {
        SidebarMain,
        FooterMain
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