<template>
  <h1>Sign in</h1>
  <p><input type="text" placeholder="Email" v-model="email" /></p>
  <p><input type="password" placeholder="Password" v-model="password" /></p>
  <p><button @click="signin">Sign in via Firebase</button></p>
  <p v-if="currentRole">
    Signed in as: <strong>{{ currentUserEmail }}</strong> (role: <strong>{{ currentRole }}</strong>)
  </p>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAuth, signInWithEmailAndPassword, onAuthStateChanged } from 'firebase/auth'
import { getFirestore, doc, getDoc } from 'firebase/firestore'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const currentRole = ref('')
const currentUserEmail = ref('')
const router = useRouter()
const auth = getAuth()
const db = getFirestore()

onMounted(() => {
  onAuthStateChanged(auth, async (user) => {
    if (user) {
      currentUserEmail.value = user.email
      const snap = await getDoc(doc(db, 'users', user.uid))
      currentRole.value = snap.exists() ? snap.data().role : 'unknown'
    }
  })
})

const signin = () => {
  signInWithEmailAndPassword(getAuth(), email.value, password.value)
    .then(async (data) => {
      console.log('Firebase Sign in Successful!')
      router.push('/')
      console.log(auth.currentUser) // To check the current User signed in

      // Look up this user's role so we can show role-based sign in (Task 7.2)
      const snap = await getDoc(doc(db, 'users', data.user.uid))
      const role = snap.exists() ? snap.data().role : 'unknown'
      currentRole.value = role
      currentUserEmail.value = data.user.email
      console.log('Current user role:', role)
    })
    .catch((error) => {
      console.log(error.code)
    })
}
</script>
