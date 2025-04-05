<template>
    <div>
        <h1>Rental List</h1>

        <router-link to="/add-rental">
            <button class="menu-button">Add new rental</button>
        </router-link>

        <ul v-if="rentals.length > 0">
            <li v-for="rental in rentals" :key="rental.id">
                {{ rental.userId }} -
                <span v-if="getAuthorName(rental.bookId)">{{ getAuthorName(rental.bookId) }}</span> -
                <span v-if="getBookTitle(rental.bookId)">{{ getBookTitle(rental.bookId) }}</span> -
                {{ rental.startDate }} - {{ rental.endDate }}

                <button @click="returnBook(rental.userId)">Return book</button>
            </li>
        </ul>

        <div v-else-if="error">Unable to load rentals</div>
        <p v-else>No rentals</p>

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
            books: [],
            authors: [],
            rentals: [],
            error: null,
            currentPage: 1,
            pageSize: 5,
            isLastPage: false,
        };
    },
    mounted() {
        this.fetchData();
    },
    methods: {
        async fetchData() {
            try {
                console.log('Fetching data...');
                const booksRes = await fetch('http://localhost:8080/books');
                if (!booksRes.ok) {
                    throw new Error(`HTTP error! status: ${booksRes.status}`);
                }
                const authorsRes = await fetch('http://localhost:8080/authors');
                if (!authorsRes.ok) {
                    throw new Error(`HTTP error! status: ${authorsRes.status}`);
                }
                const rentalsRes = await fetch(`http://localhost:8080/rentals/${this.pageSize}/${this.currentPage}`);
                if (!rentalsRes.ok) {
                    throw new Error(`HTTP error! status: ${rentalsRes.status}`);
                }

                this.books = await booksRes.json();
                this.authors = await authorsRes.json();
                const rentalData = await rentalsRes.json();

                this.rentals = rentalData;
                this.isLastPage = rentalData.length < this.pageSize;

            } catch (e) {
                console.error('Unable to load:', e);
                this.error = true;
            }
        },
        nextPage() {
            if (!this.isLastPage) {
                this.currentPage++;
                this.fetchData();
            }
        },
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
                this.fetchData();
            }
        },
        async returnBook(id) {
            try {
                const response = await fetch(`http://localhost:8080/rentals/${id}`, {
                    method: 'DELETE',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ endDate: new Date().toISOString() }),
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                this.fetchData();
            } catch (e) {
                console.error('Error during returning:', e);
            }
        },
        getBookTitle(bookId) {
            const book = this.books.find(b => b.id === bookId);
            return book ? book.title : 'Unknown Book';
        },
        getAuthorName(bookId) {
            const book = this.books.find(b => b.id === bookId);
            if (!book) return 'Unknown Author';
            const author = this.authors.find(a => a.id === book.authorId);
            return author ? author.name : 'Unknown Author';
        }
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
