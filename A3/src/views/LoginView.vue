<template>
  <div class="container my-5" style="max-width: 480px;">
    <!-- Title Banner -->
    <div class="p-3 mb-4 bg-light border text-center rounded">
      <h3 class="text-dark mb-1 fw-bold">Ride & Stride Melbourne</h3>
      <p class="text-muted mb-0 small">Authentication & Account Access</p>
    </div>

    <div class="card p-4 border bg-white shadow-sm">
      <h5 class="fw-bold mb-3 text-center">{{ isRegister ? 'Create Account' : 'Account Login' }}</h5>

      <!-- Quick Demo Fill Buttons -->
      <div class="d-flex gap-2 mb-3">
        <button type="button" class="btn btn-sm btn-outline-danger flex-fill" @click="fillAdmin">
          Demo Admin
        </button>
        <button type="button" class="btn btn-sm btn-outline-primary flex-fill" @click="fillCommuter">
          Demo Commuter
        </button>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="mb-3">
          <label class="form-label small fw-bold">Email Address:</label>
          <input 
            v-model="email" 
            type="email" 
            class="form-control" 
            placeholder="name@example.com" 
            required 
          />
        </div>

        <div class="mb-3">
          <label class="form-label small fw-bold">Password:</label>
          <input 
            v-model="password" 
            type="password" 
            class="form-control" 
            placeholder="At least 6 characters" 
            required 
          />
        </div>

        <div v-if="isRegister" class="mb-3">
          <label class="form-label small fw-bold">Account Role:</label>
          <select v-model="role" class="form-select">
            <option value="commuter">Commuter (Standard User)</option>
            <option value="admin">Admin (Administrator)</option>
          </select>
        </div>

        <div v-if="error" class="alert alert-danger py-2 small mb-3">
          {{ error }}
        </div>
        <div v-if="successMsg" class="alert alert-success py-2 small mb-3">
          {{ successMsg }}
        </div>

        <button type="submit" class="btn btn-dark w-100 py-2" :disabled="loading">
          <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
          {{ isRegister ? 'Register Account' : 'Sign In' }}
        </button>
      </form>

      <hr class="my-3" />

      <div class="text-center">
        <button 
          type="button" 
          class="btn btn-link text-decoration-none small text-muted"
          @click="isRegister = !isRegister; error = ''; successMsg = ''"
        >
          {{ isRegister ? 'Already have an account? Sign in here' : "Don't have an account? Register here" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { auth, db } from '../firebase/init'
import { 
  signInWithEmailAndPassword, 
  createUserWithEmailAndPassword 
} from 'firebase/auth'
import { doc, setDoc } from 'firebase/firestore'

const router = useRouter()
const isRegister = ref(false)
const email = ref('')
const password = ref('')
const role = ref('commuter')
const error = ref('')
const successMsg = ref('')
const loading = ref(false)

const fillAdmin = () => {
  email.value = 'admin@fit5032.com'
  password.value = 'admin123'
  role.value = 'admin'
}

const fillCommuter = () => {
  email.value = 'commuter@fit5032.com'
  password.value = '123456'
  role.value = 'commuter'
}

const handleSubmit = async () => {
  error.value = ''
  successMsg.value = ''
  loading.value = true

  try {
    if (isRegister.value) {
      if (password.value.length < 6) {
        error.value = 'Password must be at least 6 characters long'
        loading.value = false
        return
      }
      const cred = await createUserWithEmailAndPassword(auth, email.value, password.value)
      await setDoc(doc(db, 'users', cred.user.uid), {
        email: email.value,
        role: role.value
      })
      successMsg.value = 'Account registered successfully!'
      setTimeout(() => router.push('/'), 1000)
    } else {
      await signInWithEmailAndPassword(auth, email.value, password.value)
      router.push('/')
    }
  } catch (err) {
    if (err.code === 'auth/invalid-credential' || err.code === 'auth/user-not-found' || err.code === 'auth/wrong-password') {
      error.value = 'Invalid email or password.'
    } else if (err.code === 'auth/email-already-in-use') {
      error.value = 'This email is already in use.'
    } else {
      error.value = err.message
    }
  } finally {
    loading.value = false
  }
}
</script>
