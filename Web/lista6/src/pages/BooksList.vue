<template>
    <div>
        <h1>Books List</h1>

        <router-link to="/add-book">
            <button class="menu-button">Add new book</button>
        </router-link>


        <ul v-if="books.length > 0">
            <li v-for="book in books" :key="book.id">
                {{ book.title }} -
                <span v-if="authors.length > 0">
                    {{authors.find(author => author.id === book.authorId)?.name}}
                </span>
                <router-link :to="`/edit-book/${book.id}`">
                    <button>Edit</button>
                </router-link>
                <button @click="deleteBook(book.id)">Delete</button>
            </li>
        </ul>

        <p v-else-if="error">Unable to load books</p>
        <p v-else>Books loading...</p>
    </div>
    <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
        <span> Page {{ currentPage }} </span>
        <button @click="nextPage" :disabled="isLastPage">Next</button>
    </div>
</template>

<script>
export default {
    data() {
        return {
            books: [],
            authors: [],
            error: null,
            currentPage: 1,
            pageSize: 5,
            isLastPage: false,
        };
    },
    mounted() {
        this.fetchBooks();
        this.fetchAuthors();
    },
    methods: {
        async fetchBooks() {
            try {
                const response = await fetch(`http://localhost:8080/books/${this.pageSize}/${this.currentPage}`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();

                this.books = data;
                this.isLastPage = data.length < this.pageSize;
            } catch (e) {
                console.error('Error fetching books:', e);
                this.error = true;
            }
        },
        async fetchAuthors() {
            try {
                const response = await fetch('http://localhost:8080/authors');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                this.authors = await response.json();
            } catch (e) {
                console.error('Error fetching authors:', e);
            }
        },
        nextPage() {
            if (!this.isLastPage) {
                this.currentPage++;
                this.fetchBooks();
            }
        },
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
                this.fetchBooks();
            }
        },
        async deleteBook(id) {
            try {
                const response = await fetch(`http://localhost:8080/books/${id}`, {
                    method: 'DELETE',
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                this.books = this.books.filter(book => book.id !== id);

                if (this.books.length === 0 && this.currentPage > 1) {
                    this.currentPage--;
                }
                this.fetchBooks();
            } catch (e) {
                console.error('Error deleting book:', e);
            }
        }
    },
};
</script>

<style scoped>
.pagination {
    margin: 20px 0;
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
