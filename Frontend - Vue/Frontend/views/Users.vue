<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import Layout from "./Layout.vue";
import { RouterView } from "vue-router";

const users = ref([]);
const userIdToDelete = ref(null);


const fetchUsers = async () => {
  try {
      const response = await axios.get("http://127.0.0.1:5000/users", {
      withCredentials: true, 
    });

    console.log("Response from server:", response.data);
    users.value = response.data;  // Postavi korisnike u tabelu
  } catch (error) {
    console.error("Fetch users error:", error.response?.data || error);
  }
};

const confirmDelete = (id) => {
  userIdToDelete.value = id;
  new bootstrap.Modal(document.getElementById("deleteModal")).show();
};

const deleteUser = async () => {
  if (!userIdToDelete.value) return;

  try {
    await axios.delete(`http://127.0.0.1:5000/deleteuser/${userIdToDelete.value}`, { withCredentials: true });

    alert("User deleted successfully!");

    const modalElement = document.getElementById("deleteModal");
    const modalInstance = bootstrap.Modal.getInstance(modalElement);
    if (modalInstance) {
      modalInstance.hide();
    }

    // Resetujemo selektovani ID
    userIdToDelete.value = null;

    // Osvezi listu korisnika
    fetchUsers();
  } catch (error) {
    alert(error.response?.data?.message || 'Error deleting user');
  }
};


onMounted(fetchUsers);
</script>
<template>
<Layout>
    <div class="my-5 text-center d-flex align-items-center justify-content-center flex-column">
      <h2 class="text-center">Users</h2>
      <RouterLink to="/add-user" class="btn btn-primary mb-3">Add User</RouterLink>
  
      <div class="container-md mt-5 w-75">
        <table class="table">
          <thead>
            <tr>
              <th scope="col">Id</th>
              <th scope="col">Username</th>
              <th scope="col">Email</th>
              <th scope="col">Role</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.role }}</td>
              <td>
                <RouterLink :to="'/edituser/' + user.id" class="btn btn-success">Edit</RouterLink>
                <button class="btn btn-danger ms-2" @click="confirmDelete(user.id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Delete Modal -->
      <div class="modal fade" id="deleteModal" tabindex="-1" @hidden="userIdToDelete = null">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Confirm Deletion</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              Are you sure you want to delete this user? This action cannot be undone.
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
              <button type="button" class="btn btn-danger" @click="deleteUser(userIdToDelete)">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <RouterView/>
</Layout>
</template>
  
<style>
 
</style>
  