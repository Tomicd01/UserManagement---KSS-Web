<script setup>
  import { ref, onMounted } from "vue";
  import axios from "axios";
  import { useRouter } from "vue-router";
  import Layout from "./Layout.vue";
  
  const orders = ref([]);
  const selectedOrderId = ref(null);
  const router = useRouter();
  
  const fetchOrders = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/orders");
      orders.value = response.data;
    } catch (error) {
      console.error("Error fetching orders:", error);
    }
  };
  
  const confirmDelete = (orderId) => {
    selectedOrderId.value = orderId;
    let modal = new bootstrap.Modal(document.getElementById("confirmDeleteModal"));
    modal.show();
  };
  
  const deleteOrder = async () => {
  if (!selectedOrderId.value) return;

  try {
    await axios.delete(`http://127.0.0.1:5000/deleteorder/${selectedOrderId.value}`, { withCredentials: true });

    orders.value = orders.value.filter(order => order.id !== selectedOrderId.value);
    selectedOrderId.value = null;

    // zatvori modal
    const modalElement = document.getElementById("confirmDeleteModal");
    const modalInstance = bootstrap.Modal.getInstance(modalElement);
    if (modalInstance) {
      modalInstance.hide();
    }

    alert("Order deleted successfully!");
  } catch (error) {
    console.error("Error deleting order:", error);
    alert(error.response?.data?.message || "Error deleting order");
  }
  };

  
  onMounted(fetchOrders);
  </script>


<template>
<Layout>
    <div class="my-5 text-center d-flex align-items-center justify-content-center flex-column">
      <h2 class="text-center">Orders</h2>
      <router-link to="/add-order" class="btn btn-primary mb-3">Add Order</router-link>
      
      <div class="container-md mt-5 w-75">
        <table class="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer</th>
              <th>Total Price</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in orders" :key="order.id">
              <td>{{ order.id }}</td>
              <td>{{ order.customer }}</td>
              <td>{{ order.total_price }}</td>
              <td>
                <router-link :to="`/editorder/${order.id}`" class="btn btn-success">Edit</router-link>
                <button class="btn btn-danger ms-2" @click="confirmDelete(order.id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- MODAL -->
      <div class="modal fade" id="confirmDeleteModal" tabindex="-1" aria-labelledby="deleteModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Confirm Deletion</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              Are you sure you want to delete this order?
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
              <button class="btn btn-danger" @click="deleteOrder">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>
</Layout> 
</template>

  
<style scoped>
    
 </style>
  