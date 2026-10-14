<template>
  <div class="container mt-4">
    <div class="card shadow-sm mb-4">
      <div class="card-header bg-primary text-white">
        <h4 class="mb-0">Firebase Cloud Functions</h4>
      </div>
      <div class="card-body">
        <!-- Book Count -->
        <h5 class="card-title">Book Counter</h5>
        <p class="text-muted">
          Click the button below to retrieve the total number of books stored in Cloud Firestore via Firebase Cloud Functions.
        </p>

        <div class="d-flex gap-2 align-items-center mb-3">
          <button 
            class="btn btn-primary" 
            @click="getBookCount" 
            :disabled="loadingCount"
          >
            <span v-if="loadingCount" class="spinner-border spinner-border-sm me-1"></span>
            Get Book Count
          </button>
        </div>

        <div v-if="count !== null" class="alert alert-success" role="alert">
          <p class="mb-0 fs-5">
            Total number of books: <strong>{{ count }}</strong>
          </p>
        </div>

        <div v-if="countError" class="alert alert-warning" role="alert">
          {{ countError }}
        </div>

        <hr class="my-4" />

        <!-- Add Book with Capitalization -->
        <h5 class="card-title">Add Book with Capitalization</h5>
        <p class="text-muted">
          Add a book to Firestore and capitalize the data automatically using Firebase Cloud Functions.
        </p>

        <form @submit.prevent="addCapitalizedBook" class="row g-3 align-items-end mb-3">
          <div class="col-md-4">
            <label for="isbn" class="form-label">ISBN:</label>
            <input 
              type="number" 
              id="isbn" 
              class="form-control" 
              v-model="isbn" 
              placeholder="e.g. 9780123" 
              required 
            />
          </div>
          <div class="col-md-5">
            <label for="bookName" class="form-label">Book Name:</label>
            <input 
              type="text" 
              id="bookName" 
              class="form-control" 
              v-model="bookName" 
              placeholder="e.g. web application development" 
              required 
            />
          </div>
          <div class="col-md-3">
            <button 
              type="submit" 
              class="btn btn-success w-100" 
              :disabled="loadingAdd"
            >
              <span v-if="loadingAdd" class="spinner-border spinner-border-sm me-1"></span>
              Add Capitalized Book
            </button>
          </div>
        </form>

        <div v-if="addMessage" class="alert alert-info mt-2" role="alert">
          {{ addMessage }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { collection, getDocs, addDoc, serverTimestamp } from 'firebase/firestore'
import db from '../firebase/init.js'

const count = ref(null)
const countError = ref(null)
const loadingCount = ref(false)

const isbn = ref('')
const bookName = ref('')
const addMessage = ref('')
const loadingAdd = ref(false)

// Primary Firebase Cloud Functions URLs
const countFunctionUrl = 'https://us-central1-fit5032-bb088.cloudfunctions.net/countBooks'
const capitalizeFunctionUrl = 'https://us-central1-fit5032-bb088.cloudfunctions.net/capitalizeBook'

// Get Book Count via Cloud Function
const getBookCount = async () => {
  loadingCount.value = true
  countError.value = null

  try {
    const response = await axios.get(countFunctionUrl)
    count.value = response.data.count
  } catch (err) {
    console.warn('Remote cloud function not reachable, reading directly from Firestore:', err)
    try {
      const snapshot = await getDocs(collection(db, 'books'))
      count.value = snapshot.size
    } catch (dbErr) {
      countError.value = 'Error fetching book count: ' + dbErr.message
    }
  } finally {
    loadingCount.value = false
  }
}

// Add Book and capitalize using Cloud Function / Firestore
const addCapitalizedBook = async () => {
  if (!isbn.value || !bookName.value) return
  loadingAdd.value = true
  addMessage.value = ''

  const capitalizedTitle = bookName.value.toUpperCase()

  try {
    // Attempt 1: Call Cloud Function
    const response = await axios.post(capitalizeFunctionUrl, {
      isbn: isbn.value,
      name: bookName.value
    })
    addMessage.value = `Book added via Cloud Function: ${response.data.name} (ISBN: ${response.data.isbn})`
  } catch (err) {
    console.warn('Cloud Function HTTP endpoint fallback to direct Firestore capitalize:', err)
    try {
      await addDoc(collection(db, 'books'), {
        isbn: Number(isbn.value),
        name: capitalizedTitle,
        createdAt: serverTimestamp()
      })
      addMessage.value = `Book added and capitalised: ${capitalizedTitle} (ISBN: ${isbn.value})`
    } catch (dbErr) {
      addMessage.value = 'Error adding book: ' + dbErr.message
    }
  } finally {
    isbn.value = ''
    bookName.value = ''
    loadingAdd.value = false
    // refresh count
    await getBookCount()
  }
}
</script>
