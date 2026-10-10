<template>
  <div class="container my-4" style="max-width: 800px;">
    <!-- Title Banner -->
    <div class="p-3 mb-4 bg-light border text-center rounded">
      <h3 class="text-dark mb-1 fw-bold">Community Route Reviews</h3>
      <p class="text-muted mb-0 small">Active Transport Route Feedback, Ratings & Safety Observations</p>
    </div>

    <!-- Add Review Form Card -->
    <div class="card p-3 mb-4 border bg-white shadow-sm">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <h5 class="mb-0 fw-bold">Submit Route Review</h5>
        <button class="btn btn-sm btn-outline-secondary" @click="showForm = !showForm">
          {{ showForm ? 'Hide Form' : 'Show Form' }}
        </button>
      </div>

      <form v-if="showForm" @submit.prevent="addReview" class="mt-3">
        <div class="row g-2 mb-2">
          <div class="col-md-5">
            <label class="form-label small">Route Name:</label>
            <input v-model="formData.route" type="text" class="form-control form-control-sm" placeholder="e.g. Swanston St Bikeway" />
            <div v-if="errors.route" class="text-danger small mt-1">{{ errors.route }}</div>
          </div>
          <div class="col-md-3">
            <label class="form-label small">Rating:</label>
            <select v-model.number="formData.rating" class="form-select form-select-sm">
              <option :value="5">5 - Excellent</option>
              <option :value="4">4 - Good</option>
              <option :value="3">3 - Average</option>
              <option :value="2">2 - Fair</option>
              <option :value="1">1 - Poor</option>
            </select>
          </div>
          <div class="col-md-4">
            <label class="form-label small">Reviewer Name:</label>
            <input v-model="formData.author" type="text" class="form-control form-control-sm" placeholder="Your name" />
            <div v-if="errors.author" class="text-danger small mt-1">{{ errors.author }}</div>
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label small">Comment / Feedback:</label>
          <input v-model="formData.comment" type="text" class="form-control form-control-sm" placeholder="Describe safety and cycling conditions" />
          <div v-if="errors.comment" class="text-danger small mt-1">{{ errors.comment }}</div>
        </div>

        <div class="d-flex gap-2">
          <button type="submit" class="btn btn-sm btn-dark flex-grow-1">Submit Review</button>
          <button type="button" class="btn btn-sm btn-secondary px-3" @click="clearForm">Clear</button>
        </div>
      </form>
    </div>

    <!-- Reviews Table Card -->
    <div class="card p-3 mb-4 border bg-white shadow-sm">
      <div class="d-flex flex-wrap justify-content-between align-items-center mb-3 gap-2">
        <div>
          <h5 class="mb-0 fw-bold">Route Reviews List</h5>
          <span class="text-muted small">Average Rating: </span>
          <span class="badge bg-success">{{ averageRating }} / 5.0</span>
        </div>
        <div class="d-flex gap-2">
          <input 
            v-model="searchKeyword" 
            type="text" 
            class="form-control form-control-sm" 
            style="width: 170px;" 
            placeholder="Search route or author..." 
          />
          <select v-model="selectedRating" class="form-select form-select-sm" style="width: 130px;">
            <option value="">All Ratings</option>
            <option value="5">5 Stars</option>
            <option value="4">4+ Stars</option>
            <option value="3">3+ Stars</option>
          </select>
        </div>
      </div>

      <div v-if="paginatedReviews.length === 0" class="text-center text-muted py-3 border bg-light rounded">
        No reviews match the current filter.
      </div>

      <div v-else class="table-responsive">
        <table class="table table-bordered mb-2">
        <thead class="table-light">
          <tr>
            <th style="width: 8%;">No.</th>
            <th @click="sortBy('route')" style="cursor: pointer;">
              Route <span class="small text-muted">&#x21C5;</span>
            </th>
            <th @click="sortBy('rating')" style="cursor: pointer; width: 15%;">
              Rating <span class="small text-muted">&#x21C5;</span>
            </th>
            <th>Comment</th>
            <th style="width: 25%;">Author</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, idx) in paginatedReviews" :key="item.id || idx">
            <td>{{ (currentPage - 1) * pageSize + idx + 1 }}</td>
            <td class="fw-bold small">{{ item.route }}</td>
            <td>
              <span class="badge bg-secondary">{{ item.rating }} / 5</span>
            </td>
            <td class="small text-muted">{{ item.comment }}</td>
            <td class="small">{{ item.author || item.reviewer || 'Anonymous' }} ({{ item.date }})</td>
          </tr>
        </tbody>
        </table>
      </div>

      <!-- 10 Rows Limit Pagination Bar -->
      <div class="d-flex justify-content-between align-items-center mt-2 pt-2 border-top">
        <small class="text-muted">
          Page {{ currentPage }} of {{ totalPages }} (10 rows per page)
        </small>
        <div class="btn-group btn-group-sm">
          <button class="btn btn-outline-secondary" :disabled="currentPage === 1" @click="currentPage--">Previous</button>
          <button 
            v-for="p in totalPages" 
            :key="p" 
            class="btn" 
            :class="currentPage === p ? 'btn-dark' : 'btn-outline-secondary'"
            @click="currentPage = p"
          >
            {{ p }}
          </button>
          <button class="btn btn-outline-secondary" :disabled="currentPage === totalPages || totalPages === 0" @click="currentPage++">Next</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { db } from '../firebase/init'
import { 
  collection, 
  onSnapshot, 
  addDoc, 
  serverTimestamp 
} from 'firebase/firestore'

const showForm = ref(true)
const formData = ref({
  route: '',
  rating: 5,
  author: '',
  comment: ''
})
const errors = ref({})

// Reviews come only from the Firestore 'reviews' collection, so the table,
// the average rating and the cloud data all use the same records.
const reviews = ref([])
const pageSize = 10
const currentPage = ref(1)
const sortKey = ref('rating')
const sortAsc = ref(false)
const searchKeyword = ref('')
const selectedRating = ref('')

onMounted(() => {
  onSnapshot(collection(db, 'reviews'), (snapshot) => {
    reviews.value = snapshot.docs.map(d => ({ id: d.id, ...d.data() }))
  }, (err) => console.error('Reviews sync failed:', err))
})

// Angle brackets are rejected so that markup cannot be stored in the shared records.
const hasMarkup = (text) => /[<>]/.test(text)

const addReview = async () => {
  errors.value = {}
  const route = formData.value.route.trim()
  const author = formData.value.author.trim()
  const comment = formData.value.comment.trim()

  if (!route) errors.value.route = 'Please enter route'
  else if (hasMarkup(route)) errors.value.route = 'Route cannot contain < or > characters'
  if (!author) errors.value.author = 'Please enter author'
  else if (hasMarkup(author)) errors.value.author = 'Name cannot contain < or > characters'
  if (!comment) errors.value.comment = 'Please enter comment'
  else if (hasMarkup(comment)) errors.value.comment = 'Comment cannot contain < or > characters'

  if (Object.keys(errors.value).length > 0) return

  const item = {
    route,
    rating: Number(formData.value.rating),
    author,
    comment,
    date: new Date().toISOString().split('T')[0]
  }

  // The onSnapshot listener adds the new record to the table, so no local insert is needed.
  try {
    await addDoc(collection(db, 'reviews'), { ...item, createdAt: serverTimestamp() })
  } catch (e) {
    alert('Could not save the review. Please try again.')
    return
  }

  clearForm()
}

const clearForm = () => {
  formData.value = {
    route: '',
    rating: 5,
    author: '',
    comment: ''
  }
  errors.value = {}
}

const sortBy = (key) => {
  if (sortKey.value === key) {
    sortAsc.value = !sortAsc.value
  } else {
    sortKey.value = key
    sortAsc.value = true
  }
}

const filteredReviews = computed(() => {
  let list = [...reviews.value]
  if (searchKeyword.value) {
    const kw = searchKeyword.value.toLowerCase()
    list = list.filter(r => 
      (r.route || '').toLowerCase().includes(kw) ||
      (r.author || r.reviewer || '').toLowerCase().includes(kw)
    )
  }
  if (selectedRating.value) {
    const mr = parseInt(selectedRating.value)
    if (!isNaN(mr)) list = list.filter(r => r.rating >= mr)
  }

  list.sort((a, b) => {
    let va = a[sortKey.value]
    let vb = b[sortKey.value]
    if (sortKey.value === 'rating') {
      va = Number(va) || 0
      vb = Number(vb) || 0
    }
    if (va < vb) return sortAsc.value ? -1 : 1
    if (va > vb) return sortAsc.value ? 1 : -1
    return 0
  })

  return list
})

const totalPages = computed(() => Math.ceil(filteredReviews.value.length / pageSize) || 1)
const paginatedReviews = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredReviews.value.slice(start, start + pageSize)
})

const averageRating = computed(() => {
  if (reviews.value.length === 0) return '0.0'
  const sum = reviews.value.reduce((acc, r) => acc + (Number(r.rating) || 0), 0)
  return (sum / reviews.value.length).toFixed(1)
})
</script>
