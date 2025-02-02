import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Users from '../views/Users.vue';
import AddUser from '../views/AddUser.vue';
import Products from '../views/Products.vue';
import Orders from '../views/Orders.vue';
import AddProduct from '../views/AddProduct.vue';
import AddOrder from '../views/AddOrder.vue';
import EditUser from '../views/EditUser.vue';
import EditProduct from '../views/EditProduct.vue';
import EditOrder from '../views/EditOrder.vue';

const routes = [
    { path: '/', component: Home },
    { path: '/users', component: Users },
    { path: '/add-user', component: AddUser},
    { path: '/products', component: Products },
    { path: '/orders', component: Orders },
    { path: '/add-product', component: AddProduct },
    { path: '/add-order', component: AddOrder },
    { path: '/edituser/:id', component: EditUser },
    { path: '/editproduct/:id', component: EditProduct },
    { path: '/editorder/:id', component: EditOrder },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;