<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const email = ref('');
const password = ref('');
const router = useRouter();
const isReady = ref(false);

const handleLogin = async () => {
    try {
        const response = await axios.post('http://127.0.0.1:5000/', 
            { email: email.value, password: password.value }, 
            { withCredentials: true, headers: { "Content-Type": "application/json" } }
        );

        alert(response.data.message);

        
        localStorage.setItem("access_token", response.data.access_token);
        localStorage.setItem("isAuthenticated", "true"); 
        
        router.push('/users');  
    } catch (error) {
        alert(error.response?.data?.message || "Login failed");
    }
};


onMounted(() => {
  document.cookie = "access_token_cookie=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";

  localStorage.removeItem("access_token");
  localStorage.removeItem("isAuthenticated");

  isReady.value = true;
});
</script>

<template>
  <div v-if="isReady">
    <div class="container-md mt-5 w-50">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input v-model="email" type="email" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control" required />
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
      </form>
    </div>
  </div>
</template>

<style scoped>

</style>
