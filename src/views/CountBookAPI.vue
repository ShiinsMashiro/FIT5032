<template>
  <pre>{{ jsondata }}</pre>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { collection, getDocs } from 'firebase/firestore'
import db from '../firebase/init.js'

const jsondata = ref(null)

const getBookCountAPI = async () => {
  try {
    const response = await axios.get('https://us-central1-fit5032-bb088.cloudfunctions.net/countBooks')
    jsondata.value = response.data
  } catch (error) {
    console.warn('Cloud function fetch failed, fallback to direct Firestore count:', error)
    try {
      const snapshot = await getDocs(collection(db, 'books'))
      jsondata.value = { count: snapshot.size }
    } catch (err) {
      jsondata.value = { error: err.message }
    }
  }
}

onMounted(() => {
  getBookCountAPI()
})
</script>

<style scoped>
pre {
  font-family: monospace;
  font-size: 1.1rem;
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-radius: 4px;
}
</style>
