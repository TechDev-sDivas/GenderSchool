<template>
  <div class="max-w-md mx-auto bg-white p-8 rounded-lg shadow-md mt-10">
    <h2 class="text-2xl font-bold mb-6 text-center">{{ $t('register.title') }}</h2>
    <form @submit.prevent="handleRegister">
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="username">{{ $t('register.username') }}</label>
        <input v-model="form.username" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" required>
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="email">{{ $t('register.email') }}</label>
        <input v-model="form.email" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="email" type="email">
      </div>
      <div class="mb-6">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="password">{{ $t('register.password') }}</label>
        <input v-model="form.password" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" id="password" type="password" required>
      </div>
      <div class="flex items-center justify-between">
        <button class="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full transform hover:scale-105 transition-all duration-200" type="submit">
          {{ $t('register.submit') }}
        </button>
      </div>
      <p v-if="error" class="text-red-500 text-xs italic mt-4">{{ error }}</p>
      <p v-if="success" class="text-green-500 text-xs italic mt-4">{{ success }}</p>
      
      <div class="mt-4 text-center">
        <span class="text-gray-600 text-sm">{{ $t('register.have_account') }} </span>
        <router-link to="/login" class="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-800 hover:to-pink-800 text-sm font-bold">{{ $t('register.login_link') }}</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';

const form = ref({ username: '', email: '', password: '' });
const error = ref('');
const success = ref('');
const router = useRouter();
const { t } = useI18n();

const handleRegister = async () => {
  error.value = '';
  success.value = '';
  try {
    await axios.post('http://localhost:8000/api/register/', form.value);
    success.value = t('register.success');
    setTimeout(() => {
        router.push('/login');
    }, 2000);
  } catch (err) {
    error.value = t('register.error');
    console.error(err);
  }
};
</script>
