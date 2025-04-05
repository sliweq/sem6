<template>
    <div>
        <h1>Add new author</h1>
        <div v-if="error">
            Error: {{ error }}
        </div>
        <div v-else>
            <form @submit.prevent="submitAuthor">
                <p>Name</p>
                <input v-model="name" placeholder="Magnus" maxlength="100" required />
                <p v-if="nameError" class="error">{{ nameError }}</p>

                <p>Surname</p>
                <input v-model="surname" placeholder="Carlsen" maxlength="100" required />
                <p v-if="surnameError" class="error">{{ surnameError }}</p>

                <input type="submit" value="Submit">
            </form>
        </div>
        <router-link to="/authors">
            <button class="menu-button">Cancel</button>
        </router-link>
    </div>
</template>

<script>
export default {
    data() {
        return {
            name: "",
            surname: "",
            error: null,
            nameError: "",
            surnameError: ""
        };
    },
    methods: {
        validateForm() {
            this.nameError = "";
            this.surnameError = "";
            let isValid = true;

            if (!this.name || this.name.length > 100) {
                this.nameError = "Name cannot be empty or longer than 100 characters.";
                isValid = false;
            }

            if (!this.surname || this.surname.length > 100) {
                this.surnameError = "Surname cannot be empty or longer than 100 characters.";
                isValid = false;
            }

            return isValid;
        },

        async submitAuthor() {
            if (!this.validateForm()) return;

            const newAuthor = {
                name: this.name.trim() + " " + this.surname.trim(),
            };

            try {
                const response = await fetch("http://localhost:8080/authors", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(newAuthor),
                });

                if (!response.ok) {
                    throw new Error(`Failed to add author: ${response.status}`);
                }

                alert("Author added successfully!");
                this.$router.push("/authors");
            } catch (e) {
                console.error("Error adding author:", e);
                this.error = e.message;
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
