<template>
  <h1>Create an Account</h1>
  <p><input type="text" placeholder="Email" v-model="email" /></p>
  <p><input type="password" placeholder="Password" v-model="password" /></p>
  <p>
    <select v-model="role">
      <option value="commuter">Commuter</option>
      <option value="admin">Admin</option>
    </select>
  </p>
  <p><button @click="register">Save to Firebase</button></p>
</template>

<script setup>
import { ref } from 'vue'
import { getAuth, createUserWithEmailAndPassword } from 'firebase/auth'
import { getFirestore, doc, setDoc } from 'firebase/firestore'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const role = ref('commuter')
const router = useRouter()
const auth = getAuth()
const db = getFirestore()

const register = () => {
  createUserWithEmailAndPassword(auth, email.value, password.value)
    .then((data) => {
      console.log('Firebase Register Successful!')
      // Save the selected role against the new user so we can
      // demonstrate role-based sign in (eFolio Task 7.2)
      return setDoc(doc(db, 'users', data.user.uid), {
        email: email.value,
        role: role.value
      }).then(() => {
        router.push('/FireLogin')
      })
    })
    .catch((error) => {
      console.log(error.code)
    })
}
</script>
