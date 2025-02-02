<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { RouterLink, useRouter } from "vue-router";
import axios from "axios";

const isAuthenticated = ref(false);
const router = useRouter();
let authCheckInterval = null; 

const checkAuth = () => {
  const token = localStorage.getItem("access_token");
  isAuthenticated.value = !!token;
};

onMounted(() => {
  checkAuth();

  
  if (!isAuthenticated.value) {
    router.push("/");
  }

});

onUnmounted(() => {
  clearInterval(authCheckInterval);
});

const logout = async () => {
  try {
    await axios.post("http://127.0.0.1:5000/logout", {}, {
      withCredentials: true,  
      headers: { "Content-Type": "application/json" }
    });

    localStorage.removeItem("access_token");
    localStorage.removeItem("isAuthenticated");
    
    router.push("/");
  } catch (error) {
    console.error("Logout failed", error);
  }
};

</script>

<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <RouterLink class="navbar-brand" to="/users">User Management</RouterLink>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse d-flex justify-content-between" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item"><RouterLink class="nav-link" to="/users">Users</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link" to="/products">Products</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link" to="/orders">Orders</RouterLink></li>
          </ul>
          <ul class="navbar-nav">
            
            <li class="nav-item" v-if="isAuthenticated">
              <button @click="logout" class="btn btn-danger">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container mt-3">
      <slot></slot>
    </div>
  </div>
</template>
