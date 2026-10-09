<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom shadow-sm mb-4">
    <div class="container" style="max-width: 960px;">
      <router-link to="/" class="navbar-brand d-flex align-items-center">
        <div>
          <span class="fw-bold text-dark fs-5">Ride & Stride</span>
          <small class="d-block text-muted" style="font-size: 0.72rem;">Melbourne Active Transport</small>
        </div>
      </router-link>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navMenu">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link to="/" class="nav-link text-secondary" active-class="active fw-bold text-dark">
              Dashboard
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/trips" class="nav-link text-secondary" active-class="active fw-bold text-dark">
              Trips
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/reviews" class="nav-link text-secondary" active-class="active fw-bold text-dark">
              Reviews
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/map" class="nav-link text-secondary" active-class="active fw-bold text-dark">
              Map
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/email" class="nav-link text-secondary" active-class="active fw-bold text-dark">
              Certificate & Email
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/cloud-stats" class="nav-link text-secondary" active-class="active fw-bold text-dark">
              Cloud Stats
            </router-link>
          </li>
        </ul>

        <!-- User Authentication Status -->
        <div class="d-flex align-items-center gap-2">
          <div v-if="user" class="d-flex align-items-center gap-2">
            <span class="text-muted small">
              Logged in as: <strong>{{ user.email }}</strong>
            </span>
            <span class="badge" :class="userRole === 'admin' ? 'bg-danger' : 'bg-primary'">
              {{ userRole === 'admin' ? 'Admin' : 'Commuter' }}
            </span>
            <button class="btn btn-outline-danger btn-sm py-0 px-2" @click="handleLogout">
              Logout
            </button>
          </div>
          <div v-else>
            <router-link to="/login" class="btn btn-sm btn-dark">
              Sign In
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { auth, db } from '../firebase/init'
import { onAuthStateChanged, signOut } from 'firebase/auth'
import { doc, getDoc } from 'firebase/firestore'

const router = useRouter()
const user = ref(null)
const userRole = ref('commuter')

onMounted(() => {
  onAuthStateChanged(auth, async (currentUser) => {
    user.value = currentUser
    if (currentUser) {
      try {
        const userDoc = await getDoc(doc(db, 'users', currentUser.uid))
        if (userDoc.exists()) {
          userRole.value = userDoc.data().role || 'commuter'
        } else {
          userRole.value = currentUser.email.includes('admin') ? 'admin' : 'commuter'
        }
      } catch (err) {
        userRole.value = 'commuter'
      }
    } else {
      userRole.value = 'commuter'
    }
  })
})

const handleLogout = async () => {
  try {
    await signOut(auth)
    router.push('/login')
  } catch (err) {
    alert('Logout error: ' + err.message)
  }
}
</script>
