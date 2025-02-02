import { createApp } from 'vue'
import App from './App.vue'
import toast from 'vue3-toastify'
import router from '../router'

const app = createApp(App)

app.use(router)  // Omogućava rute
app.use(toast)   // Omogućava notifikacije

app.mount('#app') // Renderuje aplikaciju