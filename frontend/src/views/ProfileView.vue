<template>
  <div class="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow-md mt-10">
    <h2 class="text-3xl font-bold mb-6 text-center text-gray-800">{{ $t('profile.title') || 'Edit Profile' }}</h2>
    
    <div v-if="loading" class="text-center text-gray-600">Loading...</div>
    
    <form v-else @submit.prevent="updateProfile" class="space-y-6">
      <!-- Photo Upload -->
      <div class="flex flex-col items-center mb-6">
        <div class="w-32 h-32 rounded-full overflow-hidden bg-gray-200 mb-4 border-4 border-purple-100 shadow-sm relative">
          <img v-if="previewImage || user.profile?.photo" 
               :src="previewImage || user.profile?.photo" 
               class="w-full h-full object-cover" 
               alt="Profile Photo">
          <img v-else src="/default-profile.svg" class="w-full h-full object-cover" alt="Default Profile">
        </div>
        
        <div class="flex space-x-2">
          <label class="cursor-pointer bg-purple-50 text-purple-700 px-4 py-2 rounded-full hover:bg-purple-100 transition-colors font-medium text-sm">
            {{ $t('profile.change_photo') || 'Change Photo' }}
            <input type="file" @change="handleFileUpload" class="hidden" accept="image/*">
          </label>
          <button v-if="user.profile?.photo && !previewImage" @click.prevent="removePhoto" class="bg-red-50 text-red-700 px-4 py-2 rounded-full hover:bg-red-100 transition-colors font-medium text-sm">
            {{ $t('profile.remove_photo') || 'Remove' }}
          </button>
          <button v-if="previewImage" @click.prevent="cancelUpload" class="bg-gray-50 text-gray-700 px-4 py-2 rounded-full hover:bg-gray-100 transition-colors font-medium text-sm">
            {{ $t('common.cancel') || 'Cancel' }}
          </button>
        </div>
      </div>

      <!-- Basic Info -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('profile.username') || 'Username' }}</label>
          <input v-model="user.username" type="text" disabled class="w-full px-4 py-2 bg-gray-50 border border-gray-300 rounded-md text-gray-500 cursor-not-allowed">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('profile.email') || 'Email' }}</label>
          <input v-model="user.email" type="email" class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none transition-all">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('profile.first_name') || 'First Name' }}</label>
          <input v-model="user.first_name" type="text" class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none transition-all">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('profile.last_name') || 'Last Name' }}</label>
          <input v-model="user.last_name" type="text" class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none transition-all">
        </div>
      </div>

      <!-- Bio -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('profile.bio') || 'Bio' }}</label>
        <textarea v-model="user.profile.bio" rows="4" class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none transition-all" placeholder="Tell us a little about yourself..."></textarea>
      </div>

      <!-- Actions -->
      <div class="flex justify-end pt-4">
        <button type="submit" :disabled="saving" class="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-2 px-6 rounded-md shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
          {{ saving ? ($t('common.saving') || 'Saving...') : ($t('common.save') || 'Save Changes') }}
        </button>
      </div>

      <p v-if="message" :class="{'text-green-500': success, 'text-red-500': !success}" class="text-center text-sm font-medium mt-4">{{ message }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
const user = ref({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  profile: {
    bio: '',
    photo: null
  }
});
const previewImage = ref(null);
const selectedFile = ref(null);
const loading = ref(true);
const saving = ref(false);
const message = ref('');
const success = ref(false);

const fetchProfile = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get('/api/profile/', {
      headers: { Authorization: `Token ${token}` }
    });
    user.value = response.data;
    // Ensure profile object exists
    if (!user.value.profile) {
      user.value.profile = { bio: '', photo: null };
    }
  } catch (err) {
    console.error('Error fetching profile:', err);
    message.value = 'Failed to load profile.';
  } finally {
    loading.value = false;
  }
};

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    console.log('📂 File selected:', file.name, file.size, file.type);
    selectedFile.value = file;
    // Create preview URL
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const cancelUpload = () => {
  selectedFile.value = null;
  previewImage.value = null;
};

const removePhoto = async () => {
  if (!confirm(t('profile.confirm_remove_photo') || 'Are you sure you want to remove your photo?')) return;
  
  saving.value = true;
  message.value = '';
  
  try {
    const token = localStorage.getItem('token');
    const formData = new FormData();
    formData.append('remove_photo', 'true');
    // Also send other required fields if necessary, but PATCH should handle partial updates
    
    const response = await axios.patch('/api/profile/', formData, {
      headers: { 
        Authorization: `Token ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    });
    
    user.value = response.data;
    if (!user.value.profile) user.value.profile = { bio: '', photo: null };
    success.value = true;
    message.value = t('profile.photo_removed') || 'Photo removed successfully!';
  } catch (err) {
    console.error('Error removing photo:', err);
    message.value = 'Failed to remove photo.';
  } finally {
    saving.value = false;
  }
};

const updateProfile = async () => {
  saving.value = true;
  message.value = '';
  success.value = false;

  try {
    const token = localStorage.getItem('token');
    const formData = new FormData();
    
    formData.append('email', user.value.email);
    formData.append('first_name', user.value.first_name);
    formData.append('last_name', user.value.last_name);
    formData.append('profile.bio', user.value.profile.bio); // Note: Nested serializer handling depends on backend implementation. 
    // DRF Nested Serializers usually require specific format or flattening. 
    // Since we used `profile_data = validated_data.pop('profile')` in backend, 
    // we need to send data structure that DRF parser handles. 
    // Multipart/form-data with nested keys can be tricky.
    // Let's manually structure it as flattened keys if needed, but standard DRF ModelSerializer 
    // with nested serializer expects JSON usually. 
    // BUT we are uploading a file, so we MUST use multipart/form-data.
    // DRF default parser handles 'profile.bio' as {'profile': {'bio': ...}} only if using JSON parser, NOT multipart.
    // For multipart, we typically flatten it or use a library.
    // However, our backend update() method expects 'profile' key in validated_data.
    
    // We will send flat structure matching UserProfileUpdateSerializer
    // bio, photo (as file), first_name, last_name, email
    
    formData.append('bio', user.value.profile.bio);
    if (selectedFile.value) {
      formData.append('photo', selectedFile.value);
    }

    const response = await axios.patch('/api/profile/', formData, {
      headers: { 
        Authorization: `Token ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    });
    
    user.value = response.data;
    if (!user.value.profile) user.value.profile = { bio: '', photo: null };
    success.value = true;
    message.value = t('common.saved') || 'Profile updated successfully!';
  } catch (err) {
    console.error('Error updating profile:', err);
    message.value = 'Failed to update profile. ' + (err.response?.data?.detail || '');
  } finally {
    saving.value = false;
  }
};

onMounted(fetchProfile);
</script>
