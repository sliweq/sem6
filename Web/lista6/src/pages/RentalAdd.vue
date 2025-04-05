<template>
    <div>
        <h1>Add new rental</h1>
        <div v-if="error">
            Error: {{ error }}
        </div>
        <div v-else>
            <form @submit.prevent="submitRental">
                <p>User Id</p>
                <input v-model="user_id" type="number" min="1" placeholder="1" required />
                <p v-if="userError" class="error">{{ userError }}</p>

                <p>Book</p>
                <select v-model="book_id" required>
                    <option v-for="book in books" :key="book.id" :value="book.id">
                        {{ book.title }}
                    </option>
                </select>

                <p>Rental Date</p>
                <input type="date" v-model="rental_date" required />

                <p>Return Date</p>
                <input type="date" v-model="return_date" required />

                <input type="submit" value="Submit">
            </form>
        </div>
        <router-link to="/rentals">
            <button class="menu-button">Cancel</button>
        </router-link>
    </div>
</template>

<script>
export default {
    data() {
        return {
            books: [],
            user_id: null,
            book_id: null,
            rental_date: "",
            return_date: "",
            error: null,
            userError: ""
        };
    },
    mounted() {
        this.fetchBooks();
    },
    methods: {
        async fetchBooks() {
            try {
                const response_books = await fetch('http://localhost:8080/books');
                if (!response_books.ok) {
                    throw new Error(`HTTP error! status: ${response_books.status}`);
                }
                this.books = await response_books.json();
            } catch (e) {
                console.error('Unable to load books:', e);
                this.error = "Failed to load books.";
            }
        },
        validateForm() {
            this.userError = "";
            let isValid = true;

            if (!this.user_id || this.user_id <= 0) {
                this.userError = "User ID must be a valid number greater than 0.";
                isValid = false;
            }

            if (!this.book_id) {
                this.userError = "You must select a book.";
                isValid = false;
            }

            if (!this.rental_date || !this.return_date || this.rental_date > this.return_date) {
                this.userError = "Please provide valid rental and return dates.";
                isValid = false;
            }

            return isValid;
        },

        async submitRental() {
            if (!this.validateForm()) return;

            const newRental = {
                userId: this.user_id,
                bookId: this.book_id,
                startDate: this.rental_date,
                endDate: this.return_date
            };

            try {
                const response = await fetch("http://localhost:8080/rentals", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(newRental),
                });

                if (!response.ok) {
                    throw new Error(`Failed to add rental: ${response.status}`);
                }

                alert("Rental added successfully!");
                this.$router.push("/rentals");
            } catch (e) {
                console.error("Error adding rental:", e);
                this.error = "Error adding rental: " + e.message;
            }
        }
    }
};
</script>

<style scoped>
.error {
    color: red;
    margin-top: 5px;
    font-size: 14px;
}

button {
    margin-right: 5px;
    padding: 8px 12px;
    margin: 5px 5px 5px 5px;
    font-size: 14px;
    border: none;
    border-radius: 5px;
    background-color: #b84141;
    color: white;
    cursor: pointer;
    transition: 0.3s;
}

button:hover {
    background-color: #a03939;
}

button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

input {
    width: 10%;
    padding: 8px;
    margin: 5px 0;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f9f9f9;
    color: #333;
}

input:focus {
    border-color: #41B883;
    outline: none;
}

input[type="submit"] {
    width: 10%;
    padding: 10px;
    margin: 10px;
    font-size: 16px;
    border: none;
    border-radius: 5px;
    background-color: #41B883;
    color: white;
    cursor: pointer;
    transition: 0.3s;
}

input[type="submit"]:hover {
    background-color: #3aa575;
}

input[type="submit"]:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}
</style>
