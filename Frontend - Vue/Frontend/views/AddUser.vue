<script setup>
import { ref } from 'vue';
import axios from 'axios';
import Layout from './Layout.vue';
import { useRouter } from 'vue-router';

const username = ref('');
const email = ref('');
const password = ref('');
const role = ref('');

const router = useRouter();

const addUser = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/adduser', {
      username: username.value,
      email: email.value,
      password: password.value,
      role: role.value
    }, { withCredentials: true });

    alert(response.data.message);
    
    router.push('/users');
  } catch (error) {
    alert(error.response?.data?.message || 'Error adding user');
  }
};
</script>

<template>
  <Layout>
    <div class="container py-5 h-100">
    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col-lg-8 col-xl-6">
        <div class="card rounded-3">
          <div class="card-body p-4 p-md-5">
            <h2 class="mb-4 pb-2 text-center">Add User</h2>
            <form @submit.prevent="addUser">
              <div class="form-group">
                <input type="text" v-model="username" class="form-control mb-3" placeholder="Username" required />
              </div>
              <div class="form-group">
                <input type="email" v-model="email" class="form-control mb-3" placeholder="Email" required />
              </div>
              <div class="form-group">
                <input type="password" v-model="password" class="form-control mb-3" placeholder="Password" required />
              </div>
              <div class="form-group">
                <input type="text" v-model="role" class="form-control mb-3" placeholder="Role (user, admin)" required />
              </div>
              <br />
              <button type="submit" class="btn btn-success text-center">Add User</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
  </Layout>
</template>

<style scoped>

</style>
