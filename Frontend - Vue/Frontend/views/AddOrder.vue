<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import Layout from "./Layout.vue";
import { useRouter } from "vue-router";

const users = ref([]);
const products = ref([]);
const selectedUser = ref("");
const selectedProduct = ref("");
const quantity = ref(1);

const router = useRouter();

const fetchData = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/addorder");
    users.value = response.data.users;
    products.value = response.data.products;
  } catch (error) {
    console.error("Error fetching users and products:", error);
  }
};

const addOrder = async () => {
  if (!selectedUser.value || !selectedProduct.value || quantity.value < 1) {
    alert("Please fill in all fields");
    return;
  }

  try {
    const response = await axios.post("http://127.0.0.1:5000/addorder", {
      user_id: selectedUser.value,
      product_id: selectedProduct.value,
      quantity: parseInt(quantity.value),
    });

    console.log("Order added:", response.data);
    alert("Order added successfully!");

    selectedUser.value = "";
    selectedProduct.value = "";
    quantity.value = 1;

    router.push('/orders');
  } catch (error) {
    console.error("Error adding order:", error);
    alert("Failed to add order.");
  }
};

onMounted(fetchData);
</script>

<template>
<Layout>
<div class="container py-5 h-100">
    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col-lg-8 col-xl-6">
        <div class="card rounded-3">
          <div class="card-body p-4 p-md-5">
            <div class="container">
            <h2 class="text-center mt-4">Add Order</h2>
            <form @submit.prevent="addOrder">
              <div class="mb-3">
                <label class="form-label">User</label>
                <select v-model="selectedUser" class="form-control" required>
                  <option value="" disabled>Select a user</option>
                  <option v-for="user in users" :key="user.id" :value="user.id">
                    {{ user.name }}
                  </option>
                </select>
              </div>
          
              <div class="mb-3">
                <label class="form-label">Product</label>
                <select v-model="selectedProduct" class="form-control" required>
                  <option value="" disabled>Select a product</option>
                  <option v-for="product in products" :key="product.id" :value="product.id">
                    {{ product.name }}
                  </option>
                </select>
              </div>
          
              <div class="mb-3">
                <label class="form-label">Quantity</label>
                <input type="number" v-model="quantity" class="form-control" min="1" required />
              </div>
          
              <button type="submit" class="btn btn-success">Submit</button>
            </form>
            </div>
        </div>
    </div>
</div>
</div>
</div>
</Layout>
</template>

<style scoped>

</style>
