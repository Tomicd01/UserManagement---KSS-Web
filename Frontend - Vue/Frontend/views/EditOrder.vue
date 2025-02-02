<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import Layout from "./Layout.vue";

const route = useRoute();
const router = useRouter();
const orderId = route.params.id;

const userId = ref("");
const productId = ref("");
const quantity = ref(1);
const products = ref([]);

// narudžbina i lista proizvoda
const fetchOrder = async () => {
  try {
    const orderResponse = await axios.get(`http://127.0.0.1:5000/getorder/${orderId}`);
    const order = orderResponse.data;
    userId.value = order.user_id;
    productId.value = order.product_id;
    quantity.value = order.quantity;

    // proizviodi za dropdown
    const productsResponse = await axios.get("http://127.0.0.1:5000/products");
    products.value = productsResponse.data;
  } catch (error) {
    console.error("Error fetching order data:", error.response);
    alert(error.response?.data?.message || "Error fetching order data");
  }
};

// ažuriranje narudžbine
const updateOrder = async () => {
  try {
    await axios.put(
      `http://127.0.0.1:5000/editorder/${orderId}`,
      {
        user_id: userId.value,
        product_id: productId.value,
        quantity: quantity.value,
      },
      { withCredentials: true }
    );

    alert("Order updated successfully!");
    router.push("/orders"); // Nakon ažuriranja preusmeri korisnika
  } catch (error) {
    console.error("Error updating order:", error.response);
    alert(error.response?.data?.message || "Error updating order");
  }
};

onMounted(fetchOrder);
</script>

<template>
  <Layout>
    <div class="container py-5">
      <div class="row d-flex justify-content-center">
        <div class="col-lg-6">
          <div class="card">
            <div class="card-body">
              <h2 class="text-center">Edit Order</h2>
              <form @submit.prevent="updateOrder">
                <div class="form-group">
                  <label for="user_id">User ID</label>
                  <input type="text" v-model="userId" class="form-control mb-3" required />
                </div>

                <div class="form-group">
                  <label for="product_id">Product</label>
                  <select v-model="productId" class="form-control mb-3" required>
                    <option v-for="product in products" :key="product.id" :value="product.id">
                      {{ product.name }}
                    </option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="quantity">Quantity</label>
                  <input type="number" v-model="quantity" class="form-control mb-3" min="1" required />
                </div>

                <button type="submit" class="btn btn-success">Update</button>
                <button type="button" class="btn btn-secondary" @click="router.push('/orders')">Cancel</button>
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
