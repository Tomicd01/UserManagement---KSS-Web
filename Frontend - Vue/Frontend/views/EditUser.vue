<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import Layout from './Layout.vue';

const route = useRoute();
const router = useRouter();
const userId = route.params.id;

const username = ref('');
const email = ref('');
const password = ref('');
const role = ref('');


const fetchUser = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/getuser/${userId}`);
    console.log("User fetched:", response.data);
    const user = response.data;
    username.value = user.username;
    email.value = user.email;
    role.value = user.role;
  } catch (error) {
    alert(error.response?.data?.message || 'Error fetching user data');
  }
};


const updateUser = async () => {
  try {
    await axios.put(`http://127.0.0.1:5000/edituser/${userId}`, {
      username: username.value,
      email: email.value,
      password: password.value, 
      role: role.value
    }, { withCredentials: true });

    alert('User updated successfully!');
    router.push('/users'); 
  } catch (error) {
    alert(error.response?.data?.message || 'Error updating user');
  }
};

onMounted(fetchUser);
</script>

<template>
  <Layout>
    <div class="container py-5 h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-lg-8 col-xl-6">
          <div class="card rounded-3">
            <div class="card-body p-4 p-md-5">
              <h2 class="mb-4 pb-2 text-center">Edit User</h2>
              <form @submit.prevent="updateUser">
                <div class="form-group">
                  <input type="text" v-model="username" class="form-control mb-3" placeholder="Username" required />
                </div>
                <div class="form-group">
                  <input type="email" v-model="email" class="form-control mb-3" placeholder="Email" required />
                </div>
                <div class="form-group">
                  <input type="password" v-model="password" class="form-control mb-3" placeholder="New Password (optional)" />
                </div>
                <div class="form-group">
                  <input type="text" v-model="role" class="form-control mb-3" placeholder="Role (user, admin)" required />
                </div>
                <button type="submit" class="btn btn-success text-center">Update User</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>
