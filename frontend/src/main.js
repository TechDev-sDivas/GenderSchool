import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createPinia } from 'pinia'
import router from './router'
import { createI18n } from 'vue-i18n'
import en from './locales/en.js'
import pt from './locales/pt.js'

const i18n = createI18n({
  legacy: false, // Use Composition API
  locale: 'pt-BR', // Default locale
  fallbackLocale: 'en',
  messages: {
    en,
    'pt-BR': pt
  }
})

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(i18n)
app.mount('#app')
