<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import Layout from "./Layout.vue";

const route = useRoute();
const router = useRouter();
const productId = route.params.id;

const name = ref("");
const description = ref("");
const price = ref("");


const fetchProduct = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/getproduct/${productId}`);
    const product = response.data;
    name.value = product.name;
    description.value = product.description;
    price.value = product.price;
  } catch (error) {
    console.error("Error fetching product data:", error.response);
    alert(error.response?.data?.message || "Error fetching product data");
  }
};


const updateProduct = async () => {
  try {
    await axios.put(
      `http://127.0.0.1:5000/editproduct/${productId}`,
      {
        name: name.value,
        description: description.value,
        price: parseFloat(price.value),
      },
      { withCredentials: true }
    );

    alert("Product updated successfully!");
    router.push("/products"); 
  } catch (error) {
    console.error("Error updating product:", error.response);
    alert(error.response?.data?.message || "Error updating product");
  }
};

onMounted(fetchProduct);
</script>

<template>
  <Layout>
    <div class="container py-5 h-100">
      <div class="row d-flex justify-content-center align-items-center h-100">
        <div class="col-lg-8 col-xl-6">
          <div class="card rounded-3">
            <div class="card-body p-4 p-md-5">
              <h2 class="mb-4 pb-2 text-center">Edit Product</h2>
              <form @submit.prevent="updateProduct">
                <div class="form-group">
                  <label>Name:</label>
                  <input type="text" v-model="name" class="form-control" required />
                </div>
                <div class="form-group">
                  <label>Description:</label>
                  <input type="text" v-model="description" class="form-control" />
                </div>
                <div class="form-group">
                  <label>Price:</label>
                  <input type="number" v-model="price" step="0.01" class="form-control" required />
                </div>
                <button type="submit" class="btn btn-primary mt-3">Save Changes</button>
                <button type="button" class="btn btn-secondary mt-3" @click="router.push('/products')">Cancel</button>
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
