<template>
    <header>
        <div class="menu-container left-aligned">
            <img alt="Vue logo" src="../assets/logo.png" class="logo">
            <h1 class="title">Library</h1>
            <nav class="nav-buttons">
                <router-link to="/">
                    <button class="menu-button">Menu</button>
                </router-link>
                <router-link to="/books">
                    <button class="menu-button">Books</button>
                </router-link>
                <router-link to="/authors">
                    <button class="menu-button">Authors</button>
                </router-link>
                <router-link to="/rentals">
                    <button class="menu-button">Rentals</button>
                </router-link>
            </nav>
        </div>
    </header>
</template>

<script>
export default {
    name: 'MenuBar',
};
</script>

<style scoped>
header {
    background-color: #e2e2e2;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.menu-container {
    display: flex;
    align-items: center;
    margin: 0 auto;
}

.left-aligned {
    justify-content: flex-start;
}

.logo {
    width: 30px;
    height: 30px;

}

.title {
    margin: 0 5px 0 0;
    font-size: 24px;
    font-weight: bold;
    color: #333;
}

.nav-buttons {
    display: flex;
}

.menu-button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 15px;
    margin-left: 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
}

.menu-button:hover {
    background-color: #45a049;
}

.router-link-active .menu-button {
    background-color: #007bff;
}
</style>