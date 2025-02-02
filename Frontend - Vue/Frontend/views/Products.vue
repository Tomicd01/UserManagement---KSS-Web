<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Layout from './Layout.vue';

const router = useRouter();
const products = ref([]);
const productToDelete = ref(null);

const fetchProducts = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/products', { withCredentials: true });
    products.value = response.data;
  } catch (error) {
    console.error('Error fetching products:', error);
  }
};

const deleteProduct = async () => {
  if (!productToDelete.value) return;

  try {
    await axios.delete(`http://127.0.0.1:5000/deleteproduct/${productToDelete.value}`, { withCredentials: true });

    products.value = products.value.filter(product => product.id !== productToDelete.value);
    productToDelete.value = null;

    // Zatvori modal
    const modalElement = document.getElementById("confirmDeleteModal");
    const modalInstance = bootstrap.Modal.getInstance(modalElement);
    if (modalInstance) {
      modalInstance.hide();
    }

    alert("Product deleted successfully!");
  } catch (error) {
    console.error("Error deleting product:", error);
    alert(error.response?.data?.message || "Error deleting product");
  }
};


const confirmDelete = (id) => {
  productToDelete.value = id;
  const modal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
  modal.show();
};

onMounted(fetchProducts);
</script>

<template>
  <Layout>
    <div class="my-5 text-center d-flex align-items-center justify-content-center flex-column">
    <h2>Product List</h2>
    <button @click="router.push('/add-product')" class="btn btn-primary mb-1">Add Product</button>
    <div class="container-md mt-5 w-75">
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Description</th>
            <th>Price</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td>{{ product.id }}</td>
            <td>{{ product.name }}</td>
            <td>{{ product.description }}</td>
            <td>RSD {{ product.price }}</td>
            <td>
              <button @click="router.push(`/editproduct/${product.id}`)" class="btn btn-success">Edit</button> |
              <button @click="confirmDelete(product.id)" class="btn btn-danger">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- MODAL -->
  <div class="modal fade" id="confirmDeleteModal" tabindex="-1" aria-labelledby="deleteModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="deleteModalLabel">Confirm Deletion</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          Are you sure you want to delete this product?
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button @click="deleteProduct" class="btn btn-danger">Delete</button>
        </div>
      </div>
    </div>
  </div>
  </Layout>
</template>

<style scoped>

</style>
