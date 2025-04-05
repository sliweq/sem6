<template>
  <nav class="navbar">
    <div class="logo">Login Library</div>
    <ul class="nav-links">
      <li><router-link to="/">Home</router-link></li>
    </ul>
  </nav>
</template>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background: #222;
  color: white;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 15px;
}

.nav-links a {
  color: white;
  text-decoration: none;
  display: block;
  padding: 12px;
  border-radius: 8px;
  transition: background 0.3s ease-in-out, transform 0.2s;
}

.nav-links a:hover {
  background: #41B883;
  transform: scale(1.05);
}
</style>