<template>
    <div>
        <h1>Edit book</h1>
        <div v-if="error">
            Error fetching author:
        </div>
        <div v-else>
            <form @submit.prevent="submitBook">
                <p>Title</p>
                <input v-model="title" />

                <p>Pages</p>
                <input v-model="pages" type="number" />

                <p>Author</p>
                <select v-model="selected">
                    <option v-for="author in authors" :key="author.id" :value="author.id">
                        {{ author.name }}
                    </option>
                </select>

                <input type="submit" value="Submit">
            </form>
        </div>
        <router-link to="/books">
            <button class="menu-button">Cancel</button>
        </router-link>

    </div>
</template>

<script>
export default {
    data() {
        return {
            title: "",
            pages: 0,
            selected: null,
            authors: [],
            error: null,
            book: null,
        };
    },
    mounted() {
        const bookId = this.$route.params.id;
        this.fetchAuthors();
        this.fetchBook(bookId);
    },
    methods: {
        async fetchAuthors() {
            try {
                const response = await fetch("http://localhost:8080/authors");
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                this.authors = await response.json();
            } catch (e) {
                console.error("Error fetching authors:", e);
                this.error = e.message;
            }
        },
        async fetchBook(id) {
            try {
                const response = await fetch(`http://localhost:8080/books/${id}`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const book = await response.json();
                this.title = book.title;
                this.pages = book.pages;
                this.selected = book.authorId;
            } catch (e) {
                console.error("Error fetching book:", e);
                this.error = e.message;
            }
        },
        async submitBook() {
            const id = this.$route.params.id;
            if (!this.title || !this.selected || !this.pages) {
                alert("Please enter a title and select an author.");
                return;
            }

            const newBook = {
                title: this.title,
                pages: this.pages,
                authorId: this.selected,
            };

            try {
                const response = await fetch(`http://localhost:8080/books/${id}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(newBook),
                });

                if (!response.ok) {
                    throw new Error(`Failed to edit book: ${response.status}`);
                }

                alert("Book edited successfully!");

                this.$router.push("/books");
            } catch (e) {
                console.error("Error editing book:", e);
                alert("Error editing book: " + e.message);
            }

        },
    },
};
</script>

<style scoped>
.error {
    color: red;
    margin-top: 10px;
}

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
