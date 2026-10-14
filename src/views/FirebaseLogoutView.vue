<template>
  <h1>Log out</h1>
  <p v-if="userEmail">Current user: <strong>{{ userEmail }}</strong></p>
  <p v-else>No user is currently signed in.</p>
  <p><button @click="logout">Log out</button></p>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAuth, signOut, onAuthStateChanged } from 'firebase/auth'

const auth = getAuth()
const userEmail = ref('')

onMounted(() => {
  onAuthStateChanged(auth, (user) => {
    userEmail.value = user ? user.email : ''
    console.log('Current user:', auth.currentUser) // shows the signed-in user in the console
  })
})

const logout = () => {
  signOut(auth)
    .then(() => {
      console.log('Sign out successful!')
      console.log('Current user after logout:', auth.currentUser) // should print null
    })
    .catch((error) => {
      console.log(error.code)
    })
}
</script>
