<template>
  <aside class="sidebar">
    <div class="logo-container">
      <img alt="Vue logo" src="../assets/logo.png" class="logo">
      <h1 class="title">Library</h1>
    </div>
    <ul>
      <li><router-link to="/">Home</router-link></li>
      <li><router-link to="/books">Books</router-link></li>
      <li><router-link to="/authors">Authors</router-link></li>
      <li><router-link to="/rentals">Rentals</router-link></li>
      <li><router-link to="/login">Login</router-link></li>
    </ul>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 250px;
  height: 100vh;
  background: #222;
  color: white;
  padding: 20px;
  margin: 20px 0;
  box-shadow: 3px 0 10px rgba(0, 0, 0, 0.3);
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
}

.logo-container {
  text-align: center;
  margin-bottom: 20px;
}

.logo {
  width: 60px;
  height: 60px;
  margin-bottom: 10px;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin-bottom: 15px;
}

.sidebar a {
  color: white;
  text-decoration: none;
  display: block;
  padding: 12px;
  border-radius: 8px;
  transition: background 0.3s ease-in-out, transform 0.2s;
}

.sidebar a:hover {
  background: #41B883;
  transform: scale(1.05);
}
</style>
