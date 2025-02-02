<script setup>
import { ref } from "vue";
import axios from "axios";
import Layout from "./Layout.vue";
import { useRouter } from "vue-router";

const name = ref("");
const description = ref("");
const price = ref("");

const router = useRouter();

const addProduct = async () => {
  if (!name.value || !description.value || !price.value) {
    alert("Please fill all fields");
    return;
  }

  try {
    const response = await axios.post("http://127.0.0.1:5000/addproduct", {
      name: name.value,
      description: description.value,
      price: parseFloat(price.value),
    });

    console.log("Product added:", response.data);
    alert("Product added successfully!");
    name.value = "";
    description.value = "";
    price.value = "";

    router.push('/products');
  } catch (error) {
    console.error("Error adding product:", error);
    alert("Failed to add product.");
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
            <h2 class="text-center mt-4">Add Product</h2>
            <form @submit.prevent="addProduct">
              <div class="mb-3">
                <label class="form-label">Name</label>
                <input type="text" v-model="name" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <input type="text" v-model="description" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Price</label>
                <input type="number" v-model="price" class="form-control" required />
              </div>
              <button type="submit" class="btn btn-primary">Add Product</button>
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
