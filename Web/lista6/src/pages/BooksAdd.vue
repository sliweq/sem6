<template>
    <div>
        <h1>Add new book</h1>
        <div v-if="error">
            Error fetching authors:
        </div>
        <div v-else>
            <form @submit.prevent="submitBook">
                <p>Title</p>
                <input v-model="title" placeholder="very interesting title" maxlength="200" required />
                <p v-if="titleError" class="error">{{ titleError }}</p>

                <p>Pages</p>
                <input v-model="pages" type="number" placeholder="number of page" required min="1" max="2000" />
                <p v-if="pagesError" class="error">{{ pagesError }}</p>

                <p>Author</p>
                <select v-model="selected">
                    <option v-for="author in authors" :key="author.id" :value="author.id">
                        {{ author.name }}
                    </option>
                </select>
                <p v-if="authorError" class="error">{{ authorError }}</p>

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
            pages: null,
            selected: null,
            authors: [],
            error: null,
            titleError: "",
            pagesError: "",
            authorError: ""
        };
    },
    mounted() {
        this.fetchAuthors();
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

        async submitBook() {
            if (!this.validateForm()) return;


            const newBook = {
                title: this.title,
                pages: this.pages,
                authorId: this.selected,
            };
            console.log("New book data:", newBook);

            try {
                const response = await fetch("http://localhost:8080/books", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(newBook),
                });

                if (!response.ok) {
                    throw new Error(`Failed to add book: ${response.status}`);
                }

                alert("Book added successfully!");

                this.$router.push("/books");
            } catch (e) {
                console.error("Error adding book:", e);
                alert("Error adding book: " + e.message);
            }

        }, validateForm() {
            this.titleError = "";
            this.pagesError = "";
            this.authorError = "";

            let isValid = true;

            if (!this.title || this.title.length > 200) {
                this.titleError = "Title cannot be empty or longer than 200 characters.";
                isValid = false;
            }

            if (!this.pages || this.pages < 1 || this.pages > 2000) {
                this.pagesError = "Pages must be between 1 and 2000.";
                isValid = false;
            }

            if (!this.selected) {
                this.authorError = "You must select an author.";
                isValid = false;
            }

            return isValid;
        },
    },
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
