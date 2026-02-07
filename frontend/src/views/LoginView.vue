<template>
  <div class="max-w-md mx-auto bg-white p-8 rounded-lg shadow-md mt-10">
    <h2 class="text-2xl font-bold mb-6 text-center">{{ $t('login.title') }}</h2>
    <form @submit.prevent="handleLogin">
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="username">{{ $t('login.username') }}</label>
        <input v-model="username" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" :placeholder="$t('login.username')" required>
      </div>
      <div class="mb-6">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="password">{{ $t('login.password') }}</label>
        <input v-model="password" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" id="password" type="password" placeholder="******************" required>
      </div>
      <div class="flex items-center justify-between">
        <button class="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full transform hover:scale-105 transition-all duration-200" type="submit">
          {{ $t('login.signin') }}
        </button>
      </div>
      <div class="mt-4 text-center">
        <span class="text-gray-600 text-sm">{{ $t('login.no_account') }} </span>
        <router-link to="/register" class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-800 hover:to-purple-800 text-sm font-bold">{{ $t('login.register_link') }}</router-link>
      </div>
      <p v-if="error" class="text-red-500 text-xs italic mt-4">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';

const username = ref('');
const password = ref('');
const error = ref('');
const router = useRouter();
const { t } = useI18n();

const handleLogin = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/login/', {
      username: username.value,
      password: password.value
    });
    
    const token = response.data.token;
    const isStaff = response.data.is_staff;
    
    localStorage.setItem('token', token);
    localStorage.setItem('is_staff', isStaff);
    
    // Simple reload to update auth state in App.vue
    window.location.href = '/courses'; 
  } catch (err) {
    error.value = t('login.error_invalid');
    console.error(err);
  }
};
</script>
