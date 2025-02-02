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
    { path: '/users', component: Users, meta: { requiresAuth: true } },
    { path: '/add-user', component: AddUser, meta: { requiresAuth: true }},
    { path: '/products', component: Products, meta: { requiresAuth: true } },
    { path: '/orders', component: Orders, meta: { requiresAuth: true } },
    { path: '/add-product', component: AddProduct, meta: { requiresAuth: true } },
    { path: '/add-order', component: AddOrder, meta: { requiresAuth: true } },
    { path: '/edituser/:id', component: EditUser, meta: { requiresAuth: true } },
    { path: '/editproduct/:id', component: EditProduct, meta: { requiresAuth: true } },
    { path: '/editorder/:id', component: EditOrder, meta: { requiresAuth: true } },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach((to, from, next) => {
    const isAuthenticated = !!localStorage.getItem("access_token"); 
    const userRole = localStorage.getItem("user_role"); 

    if (to.meta.requiresAuth && !isAuthenticated) {
        if (to.path !== "/") {  // sprečava beskonačno preusmeravanje
            next('/'); 
        } else {
            next(); // Ako je već na login stranici, dozvoli prikaz
        }
    } else if (to.meta.requiresAdmin && userRole !== 'admin') {
        next('/'); 
    } else {
        next(); // Dozvoljavamo pristup
    }
});

export default router;
