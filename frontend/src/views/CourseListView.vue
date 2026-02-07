<template>
  <div>
    <h2 class="text-3xl font-bold mb-6">{{ $t('courses.available_title') }}</h2>

    <!-- Create Course Form (Only if authenticated AND Admin) -->
    <div v-if="isAuthenticated && isAdmin" class="bg-white p-6 rounded-lg shadow-md mb-8 border-l-4 border-purple-500">
      <h3 class="text-xl font-semibold mb-4">{{ $t('courses.create_title') }}</h3>
      <form @submit.prevent="createCourse" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">{{ $t('courses.form_title') }}</label>
          <input v-model="newCourse.title" type="text" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" required>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">{{ $t('courses.form_desc') }}</label>
          <textarea v-model="newCourse.description" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" required></textarea>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">{{ $t('courses.form_price') }}</label>
          <input v-model="newCourse.price" type="number" step="0.01" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" required>
        </div>
        <button type="submit" class="bg-gradient-to-r from-green-500 to-teal-500 text-white px-4 py-2 rounded-md hover:from-green-600 hover:to-teal-600 transform hover:scale-105 transition-all duration-200">{{ $t('courses.create_button') }}</button>
      </form>
    </div>

    <!-- Course List -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="course in courses" :key="course.id" class="bg-white rounded-lg shadow-md overflow-hidden flex flex-col hover:shadow-xl transition-shadow duration-300">
        <div class="p-6 flex-grow">
          <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ course.title }}</h3>
          <p class="text-gray-600 mb-4 line-clamp-3">{{ course.description }}</p>
          <div class="flex justify-between items-center mt-auto">
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-green-600 to-blue-600 font-bold text-lg">${{ course.price }}</span>
            <span class="text-sm text-gray-500">{{ $t('courses.by') }} {{ course.instructor?.username || $t('courses.unknown') }}</span>
          </div>
        </div>
        
        <!-- Action Footer -->
        <div class="bg-gray-50 px-6 py-4 border-t border-gray-100">
          <template v-if="isAuthenticated">
             <div v-if="course.is_enrolled">
               <div class="mb-2">
                 <div class="flex justify-between text-sm mb-1">
                   <span class="font-medium text-gray-700">{{ $t('courses.progress') }}</span>
                   <span class="text-indigo-600 font-bold">{{ course.progress }}%</span>
                 </div>
                 <div class="w-full bg-gray-200 rounded-full h-2.5">
                   <div class="bg-gradient-to-r from-green-400 to-blue-500 h-2.5 rounded-full" :style="{ width: course.progress + '%' }"></div>
                 </div>
               </div>
               <button class="w-full bg-gradient-to-r from-indigo-100 to-purple-100 text-indigo-700 font-semibold py-2 px-4 rounded hover:from-indigo-200 hover:to-purple-200 transition-colors">
                 {{ $t('courses.continue') }}
               </button>
             </div>
             <div v-else>
               <button @click="enroll(course.id)" class="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold py-2 px-4 rounded hover:from-indigo-700 hover:to-purple-700 transition-colors shadow-md hover:shadow-lg transform hover:-translate-y-0.5 duration-200">
                 {{ $t('courses.enroll') }}
               </button>
             </div>
          </template>
          <template v-else>
             <router-link to="/login" class="block text-center w-full bg-gray-200 text-gray-700 font-semibold py-2 px-4 rounded hover:bg-gray-300 transition-colors">
               {{ $t('home.login_button') }}
             </router-link>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useI18n } from 'vue-i18n';

const courses = ref([]);
const newCourse = ref({ title: '', description: '', price: 0 });
const isAuthenticated = computed(() => !!localStorage.getItem('token'));
// Check if user is staff (admin)
const isAdmin = computed(() => localStorage.getItem('is_staff') === 'true');
const { t } = useI18n();

const fetchCourses = async () => {
  try {
    const headers = {};
    const token = localStorage.getItem('token');
    if (token) {
        headers['Authorization'] = `Token ${token}`;
    }
    const response = await axios.get('http://localhost:8000/api/courses/', { headers });
    courses.value = response.data;
  } catch (err) {
    console.error('Error fetching courses:', err);
  }
};

const createCourse = async () => {
  try {
    const token = localStorage.getItem('token');
    await axios.post('http://localhost:8000/api/courses/', newCourse.value, {
      headers: {
        'Authorization': `Token ${token}`
      }
    });
    // Reset form and refresh list
    newCourse.value = { title: '', description: '', price: 0 };
    fetchCourses();
  } catch (err) {
    console.error('Error creating course:', err);
    alert(t('courses.error_create'));
  }
};

const enroll = async (courseId) => {
    try {
        const token = localStorage.getItem('token');
        await axios.post(`http://localhost:8000/api/courses/${courseId}/enroll/`, {}, {
            headers: { 'Authorization': `Token ${token}` }
        });
        // Refresh list to show updated status
        fetchCourses();
    } catch (err) {
        console.error('Error enrolling:', err);
        alert('Error enrolling in course.');
    }
};

onMounted(fetchCourses);
</script>
