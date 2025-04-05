<template>
  <div>
    <h1>Authors List</h1>
    <router-link to="/add-author">
      <button class="menu-button">Add new author</button>
    </router-link>

    <ul v-if="authors.length > 0">
      <li v-for="author in authors" :key="author.id">
        {{ author.id }} - {{ author.name }}
        <router-link :to="`/edit-author/${author.id}`">
          <button>Edit</button>
        </router-link>
        <button @click="deleteAuthor(author.id)">Delete</button>
      </li>
    </ul>

    <p v-else-if="error">Unable to load authors</p>
    <p v-else>Authors loading...</p>

    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
      <span> Page {{ currentPage }} </span>
      <button @click="nextPage" :disabled="isLastPage">Next</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      authors: [],
      error: null,
      currentPage: 1,
      pageSize: 5,
      isLastPage: false,
    };
  },
  mounted() {
    this.fetchAuthors();
  },
  methods: {
    async fetchAuthors() {
      try {
        const response = await fetch(`http://localhost:8080/authors?page=${this.currentPage}&size=${this.pageSize}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        this.authors = data;
        this.isLastPage = data.length < this.pageSize;
      } catch (e) {
        console.error('Error loading authors:', e);
        this.error = true;
      }
    },
    nextPage() {
      if (!this.isLastPage) {
        this.currentPage++;
        this.fetchAuthors();
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.fetchAuthors();
      }
    },
    async deleteAuthor(id) {
      try {
        const response = await fetch(`http://localhost:8080/authors/${id}`, {
          method: 'DELETE',
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        this.authors = this.authors.filter(author => author.id !== id);
      } catch (e) {
        console.error('Error during delete author:', e);
      }
      this.fetchAuthors();
    },
  },
};
</script>

<style scoped>
.pagination {
  margin: 10px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

button {
  margin-right: 5px;
  padding: 8px 12px;
  margin: 5px 5px 5px 5px;
  font-size: 14px;
  border: none;
  border-radius: 5px;
  background-color: #41B883;
  color: white;
  cursor: pointer;
  transition: 0.3s;
}

button:hover {
  background-color: #3aa575;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
