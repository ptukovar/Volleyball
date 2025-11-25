<template>
  <div class="form-container">
    <h2 class="form-title">New Player</h2>
    <form @submit.prevent="submitForm" class="form">
      <div class="form-group">
        <label for="first_name" class="form-label">First Name</label>
        <input type="text" id="first_name" v-model="form.first_name" required class="form-input" />
      </div>
      <div class="form-group">
        <label for="last_name" class="form-label">Last Name</label>
        <input type="text" id="last_name" v-model="form.last_name" required class="form-input" />
      </div>
      <div class="form-group">
        <label for="nickname" class="form-label">Nickname</label>
        <input type="text" id="nickname" v-model="form.nickname" class="form-input" />
      </div>
      <div class="form-group">
        <label for="role" class="form-label">Role</label>
        <select id="role" v-model="form.role" class="form-select">
          <option value="0">Player</option>
          <option value="1">Admin</option>
        </select>
      </div>
      <div class="form-group">
        <label for="password" class="form-label">Password</label>
        <input type="password" id="password" v-model="form.password" required class="form-input" />
      </div>
      <div class="form-group file-group">
        <label for="image" class="form-label">Image</label>
        <input type="file" id="image" @change="handleFileUpload" class="form-file" />
      </div>
      <button type="submit" class="form-button">Create Player</button>
    </form>
  </div>
</template>


<script setup>

import { ref } from 'vue'
import { useRouter } from 'vue-router'

const form = ref({
    first_name: '',
    last_name: '',
    nickname: '', 
    role: 0,
    password: '',   
    image: ''
})
const router = useRouter()

async function submitForm() {
    await fetch('http://localhost:8000/players/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(form.value)
    })
    console.log('Player created:', form.value)
    router.push('/players')
}

function handleFileUpload(event) {
    const file = event.target.files[0]
    if (file) {
        const reader = new FileReader()
        reader.onloadend = () => {
            form.value.image = reader.result
        }
        reader.readAsDataURL(file)
    }
}

</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.form-container {
  max-width: 500px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: 0.5rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.form-title {
  margin-bottom: 1.5rem;
  font-size: 1.75rem;
  color: #111827;
  text-align: center;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.form-input,
.form-select {
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59,130,246,0.2);
}

.file-group .form-file {
  padding: 0.5rem;
}

.form-button {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #3b82f6;
  color: #fff;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.1s;
}

.form-button:hover {
  background-color: #2563eb;
}

.form-button:active {
  transform: scale(0.98);
}

@media (max-width: 480px) {
  .form-container {
    margin: 1rem;
    padding: 1.5rem;
  }
  .form-title {
    font-size: 1.5rem;
  }
}
</style>
