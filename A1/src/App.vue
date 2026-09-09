<template>
  <div class="container my-5" style="max-width: 720px;">
    <!-- Simple Title -->
    <div class="p-3 mb-4 bg-light border text-center">
      <h3 class="text-dark mb-1">Ride & Stride Melbourne</h3>
      <p class="text-muted mb-0 small">Active Transport & Carbon Tracking</p>
    </div>

    <!-- User Authentication (BR C.1 & C.2) -->
    <div class="card p-3 mb-4 border bg-white">
      <div v-if="currentUser">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <span>Logged in as: <strong>{{ currentUser }}</strong></span>
            <span class="badge ms-2" :class="currentRole === 'admin' ? 'bg-danger' : 'bg-primary'">
              {{ currentRole === 'admin' ? 'Admin' : 'Commuter' }}
            </span>
          </div>
          <button class="btn btn-sm btn-outline-danger" @click="logout">Logout</button>
        </div>

        <!-- Role-based Authorization Banner (BR C.2) -->
        <div v-if="currentRole === 'admin'" class="alert alert-danger py-2 px-3 mt-3 mb-0 d-flex justify-content-between align-items-center">
          <div>
            <strong>Admin Privileges:</strong>
            <span class="small ms-1">Full administrator access unlocked.</span>
          </div>
          <button class="btn btn-sm btn-danger py-0 px-2" @click="clearAllTrips">
            Clear All Records
          </button>
        </div>
        <div v-else class="alert alert-light border py-1 px-3 mt-3 mb-0 text-muted small">
          Standard Commuter Access: Regular trip recording permissions.
        </div>
      </div>
      <div v-else>
        <div class="d-flex gap-2">
          <input v-model="usernameInput" type="text" class="form-control form-control-sm" placeholder="Username" />
          <input v-model="passwordInput" type="password" class="form-control form-control-sm" placeholder="Password" />
          <select v-model="roleInput" class="form-select form-select-sm" style="width: 125px;">
            <option value="commuter">Commuter</option>
            <option value="admin">Admin</option>
          </select>
          <button class="btn btn-sm btn-dark" @click="login">Login</button>
          <button class="btn btn-sm btn-outline-secondary" @click="register">Register</button>
        </div>
        <div v-if="authError" class="text-danger small mt-1">{{ authError }}</div>
      </div>
    </div>

    <!-- Summary Metrics -->
    <div class="row g-2 mb-3 text-center">
      <div class="col-4">
        <div class="p-2 border bg-white">
          <small class="text-muted d-block">Total Trips</small>
          <strong class="fs-5">{{ totalTrips }}</strong>
        </div>
      </div>
      <div class="col-4">
        <div class="p-2 border bg-white">
          <small class="text-muted d-block">Total Distance</small>
          <strong class="fs-5">{{ totalDistance }} km</strong>
        </div>
      </div>
      <div class="col-4">
        <div class="p-2 border bg-white">
          <small class="text-muted d-block">CO₂ Saved</small>
          <strong class="fs-5 text-success">{{ co2Saved }} kg</strong>
        </div>
      </div>
    </div>

    <!-- Weekly Target Progress Bar -->
    <div class="card p-3 mb-4 border bg-white">
      <div class="d-flex justify-content-between align-items-center mb-1">
        <small class="fw-bold text-secondary">Weekly Community Target (50 km)</small>
        <small class="text-muted">{{ goalProgress }}% Completed</small>
      </div>
      <div class="progress" style="height: 12px;">
        <div
          class="progress-bar bg-success"
          role="progressbar"
          :style="{ width: goalProgress + '%' }"
        ></div>
      </div>
    </div>

    <!-- Part 1: Input Form -->
    <div class="card p-3 mb-4 border bg-white">
      <h5 class="mb-3">1. Add Commuter Trip</h5>

      <form @submit.prevent="addTrip">
        <div class="row mb-3">
          <!-- Commuter Name -->
          <div class="col-md-6 mb-2 mb-md-0">
            <label class="form-label small">Commuter Name:</label>
            <input
              v-model="formData.name"
              type="text"
              class="form-control"
              placeholder="Enter commuter name"
            />
            <div v-if="errors.name" class="text-danger small mt-1">
              {{ errors.name }}
            </div>
          </div>

          <!-- Trip Date -->
          <div class="col-md-6">
            <label class="form-label small">Trip Date:</label>
            <input
              v-model="formData.date"
              type="date"
              class="form-control"
            />
            <div v-if="errors.date" class="text-danger small mt-1">
              {{ errors.date }}
            </div>
          </div>
        </div>

        <div class="row mb-3">
          <!-- Distance -->
          <div class="col-md-6 mb-2 mb-md-0">
            <label class="form-label small">Distance (km):</label>
            <input
              v-model="formData.distance"
              type="number"
              step="any"
              class="form-control"
              placeholder="Enter distance"
            />
            <div v-if="errors.distance" class="text-danger small mt-1">
              {{ errors.distance }}
            </div>
          </div>

          <!-- Transport Mode -->
          <div class="col-md-6">
            <label class="form-label small">Transport Mode:</label>
            <select v-model="formData.mode" class="form-select">
              <option value="">Select mode</option>
              <option value="Walking">Walking</option>
              <option value="Cycling">Cycling</option>
              <option value="Public Transport">Public Transport</option>
            </select>
            <div v-if="errors.mode" class="text-danger small mt-1">
              {{ errors.mode }}
            </div>
          </div>
        </div>

        <!-- Buttons: Submit and Clear -->
        <div class="d-flex gap-2">
          <button type="submit" class="btn btn-dark flex-grow-1">
            Submit Trip
          </button>
          <button type="button" class="btn btn-secondary px-4" @click="clearForm">
            Clear
          </button>
        </div>
      </form>
    </div>

    <!-- Part 2: Data Table with Filter -->
    <div class="card p-3 border bg-white">
      <div class="d-flex justify-content-between align-items-center mb-3 gap-2">
        <h5 class="mb-0">2. Trip Records List</h5>
        
        <!-- Simple Filter by Mode -->
        <div class="d-flex align-items-center gap-2">
          <label class="small text-muted mb-0">Filter:</label>
          <select v-model="selectedFilter" class="form-select form-select-sm" style="width: 150px;">
            <option value="All">All Modes</option>
            <option value="Walking">Walking</option>
            <option value="Cycling">Cycling</option>
            <option value="Public Transport">Public Transport</option>
          </select>
        </div>
      </div>

      <div v-if="filteredTrips.length === 0" class="text-center text-muted py-3 border bg-light">
        No trips found for the selected filter.
      </div>

      <table v-else class="table table-bordered mb-0">
        <thead class="table-light">
          <tr>
            <th style="width: 8%;">No.</th>
            <th>Date</th>
            <th>Name</th>
            <th>Mode</th>
            <th>Distance</th>
            <th style="width: 14%;" class="text-center">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in filteredTrips" :key="item.id || index">
            <td>{{ index + 1 }}</td>
            <td>{{ item.date }}</td>
            <td>{{ item.name }}</td>
            <td>
              <span class="badge bg-light text-dark border">{{ item.mode }}</span>
            </td>
            <td>{{ item.distance }} km</td>
            <td class="text-center">
              <button
                type="button"
                class="btn btn-sm btn-outline-danger py-0 px-2"
                @click="deleteTrip(item.id)"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Part 3: Community Route Reviews & Ratings (BR C.3) -->
    <div class="card p-3 mb-4 border bg-white">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h5 class="mb-0">3. Route Reviews & Rating Aggregation</h5>
        <div>
          <span class="text-muted small me-1">Average Rating:</span>
          <span class="badge bg-success fs-6">{{ averageRating }} / 5.0</span>
          <small class="text-muted ms-1">({{ reviewList.length }} reviews)</small>
        </div>
      </div>

      <!-- Add Review Form -->
      <form @submit.prevent="addReview" class="p-3 bg-light border mb-3">
        <div class="row g-2">
          <div class="col-md-5">
            <label class="form-label small mb-1">Route Name:</label>
            <input
              v-model="reviewForm.route"
              type="text"
              class="form-control form-control-sm"
              placeholder="e.g. Swanston St Bike Lane"
            />
            <div v-if="reviewErrors.route" class="text-danger small mt-1">{{ reviewErrors.route }}</div>
          </div>
          <div class="col-md-3">
            <label class="form-label small mb-1">Rating (1 to 5):</label>
            <select v-model.number="reviewForm.rating" class="form-select form-select-sm">
              <option :value="5">5 - Excellent</option>
              <option :value="4">4 - Good</option>
              <option :value="3">3 - Average</option>
              <option :value="2">2 - Fair</option>
              <option :value="1">1 - Poor</option>
            </select>
          </div>
          <div class="col-md-4">
            <label class="form-label small mb-1">Reviewer Name:</label>
            <input
              v-model="reviewForm.author"
              type="text"
              class="form-control form-control-sm"
              placeholder="Your name"
            />
            <div v-if="reviewErrors.author" class="text-danger small mt-1">{{ reviewErrors.author }}</div>
          </div>
          <div class="col-12 mt-2">
            <label class="form-label small mb-1">Comment / Feedback:</label>
            <input
              v-model="reviewForm.comment"
              type="text"
              class="form-control form-control-sm"
              placeholder="Share your active travel experience on this route"
            />
            <div v-if="reviewErrors.comment" class="text-danger small mt-1">{{ reviewErrors.comment }}</div>
          </div>
          <div class="col-12 text-end mt-2">
            <button type="submit" class="btn btn-sm btn-dark">Submit Review</button>
          </div>
        </div>
      </form>

      <!-- Review List -->
      <div v-if="reviewList.length === 0" class="text-center text-muted py-3 border bg-light">
        No community reviews yet.
      </div>
      <div v-else class="list-group list-group-flush">
        <div
          v-for="(item, index) in reviewList"
          :key="item.id || index"
          class="list-group-item px-0 py-2 d-flex justify-content-between align-items-start"
        >
          <div>
            <div class="fw-bold small">
              {{ item.route }}
              <span class="badge bg-secondary ms-2">Rating: {{ item.rating }}/5</span>
            </div>
            <div class="text-muted small">{{ item.comment }}</div>
            <small class="text-secondary">By: {{ item.author }} ({{ item.date }})</small>
          </div>
          <button
            v-if="currentRole === 'admin'"
            type="button"
            class="btn btn-sm btn-outline-danger py-0 px-2"
            @click="deleteReview(item.id)"
          >
            Delete
          </button>
        </div>
      </div>

      <!-- Security Notice (BR C.4) -->
      <div class="mt-3 p-2 bg-light border text-muted small text-center">
        Security Notice: Client-side data validation and XSS escaping active.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// ================= BR C.1 & C.2: Auth & Role-based Access =================
const currentUser = ref(localStorage.getItem('currentUser') || '')
const currentRole = ref(localStorage.getItem('currentRole') || '')
const usernameInput = ref('')
const passwordInput = ref('')
const roleInput = ref('commuter')
const authError = ref('')

function register() {
  if (!usernameInput.value.trim() || !passwordInput.value) {
    authError.value = 'Please enter both username and password.'
    return
  }
  if (/[<>]/.test(usernameInput.value)) {
    authError.value = 'Security notice: Special characters (< >) are not allowed.'
    return
  }
  const uname = usernameInput.value.trim()
  localStorage.setItem('user_' + uname, passwordInput.value)
  localStorage.setItem('role_' + uname, roleInput.value)
  currentUser.value = uname
  currentRole.value = roleInput.value
  localStorage.setItem('currentUser', uname)
  localStorage.setItem('currentRole', currentRole.value)
  if (!formData.value.name) {
    formData.value.name = uname
  }
  reviewForm.value.author = uname
  usernameInput.value = ''
  passwordInput.value = ''
  authError.value = ''
}

function login() {
  const uname = usernameInput.value.trim()
  const saved = localStorage.getItem('user_' + uname)
  if (saved && saved === passwordInput.value) {
    currentUser.value = uname
    currentRole.value = localStorage.getItem('role_' + uname) || roleInput.value
    localStorage.setItem('currentUser', uname)
    localStorage.setItem('currentRole', currentRole.value)
    if (!formData.value.name) {
      formData.value.name = uname
    }
    reviewForm.value.author = uname
    usernameInput.value = ''
    passwordInput.value = ''
    authError.value = ''
  } else {
    authError.value = 'Invalid username or password.'
  }
}

function logout() {
  currentUser.value = ''
  currentRole.value = ''
  localStorage.removeItem('currentUser')
  localStorage.removeItem('currentRole')
  reviewForm.value.author = ''
  authError.value = ''
}

function clearAllTrips() {
  if (confirm('Admin confirmation: Are you sure you want to clear all community records?')) {
    tripList.value = []
  }
}
// =========================================================================

// Form state object
const formData = ref({
  name: '',
  date: '2026-08-27',
  distance: '',
  mode: ''
})

// Error messages object
const errors = ref({
  name: '',
  date: '',
  distance: '',
  mode: ''
})

// Filter state
const selectedFilter = ref('All')

// Initial sample data (3 simple records)
const tripList = ref([
  { id: 1, date: '2026-08-25', name: 'Liam Cooper', distance: 5.8, mode: 'Cycling' },
  { id: 2, date: '2026-08-26', name: 'Maya Patel', distance: 8.2, mode: 'Public Transport' },
  { id: 3, date: '2026-08-27', name: 'Sarah Jenkins', distance: 3.5, mode: 'Walking' }
])

// Computed statistics
const totalTrips = computed(() => tripList.value.length)

const totalDistance = computed(() => {
  const sum = tripList.value.reduce((acc, curr) => acc + Number(curr.distance || 0), 0)
  return sum.toFixed(1)
})

const co2Saved = computed(() => {
  return (Number(totalDistance.value) * 0.15).toFixed(2)
})

// Community weekly goal (50 km)
const weeklyGoalKm = 50
const goalProgress = computed(() => {
  const percent = (Number(totalDistance.value) / weeklyGoalKm) * 100
  return Math.min(Math.round(percent), 100)
})

// Filtered trips list based on selected transport mode
const filteredTrips = computed(() => {
  if (selectedFilter.value === 'All') {
    return tripList.value
  }
  return tripList.value.filter(item => item.mode === selectedFilter.value)
})

// Validation function
function validateForm() {
  let isValid = true

  if (!formData.value.name.trim()) {
    errors.value.name = 'Please enter a commuter name.'
    isValid = false
  } else if (/[<>]/.test(formData.value.name)) {
    errors.value.name = 'Security notice: HTML characters (< >) are not permitted.'
    isValid = false
  } else {
    errors.value.name = ''
  }

  if (!formData.value.date) {
    errors.value.date = 'Please select a date.'
    isValid = false
  } else {
    errors.value.date = ''
  }

  if (!formData.value.distance || Number(formData.value.distance) <= 0) {
    errors.value.distance = 'Distance must be greater than 0.'
    isValid = false
  } else {
    errors.value.distance = ''
  }

  if (!formData.value.mode) {
    errors.value.mode = 'Please select a transport mode.'
    isValid = false
  } else {
    errors.value.mode = ''
  }

  return isValid
}

// Add a new trip
function addTrip() {
  if (!validateForm()) {
    return
  }

  tripList.value.push({
    id: Date.now(),
    date: formData.value.date,
    name: sanitizeInput(formData.value.name),
    distance: Number(formData.value.distance),
    mode: formData.value.mode
  })

  clearForm()
}

// Clear form inputs and error messages
function clearForm() {
  formData.value = {
    name: '',
    date: '2026-08-27',
    distance: '',
    mode: ''
  }
  errors.value = {
    name: '',
    date: '',
    distance: '',
    mode: ''
  }
}

// Delete a trip by id
function deleteTrip(id) {
  tripList.value = tripList.value.filter(item => item.id !== id)
}

// ================= BR C.3: Route Reviews & Rating Aggregation =================
const reviewForm = ref({
  route: '',
  rating: 5,
  author: currentUser.value || '',
  comment: ''
})

const reviewErrors = ref({
  route: '',
  author: '',
  comment: ''
})

// Initial sample reviews to demonstrate average calculation immediately
const reviewList = ref([
  { id: 1, route: 'Swanston St Bike Lane', rating: 5, author: 'Liam Cooper', comment: 'Smooth cycling lane with clear markings.', date: '2026-09-06' },
  { id: 2, route: 'Yarra River Trail', rating: 4, author: 'Maya Patel', comment: 'Scenic walking trail, slightly crowded near the bridge.', date: '2026-09-07' },
  { id: 3, route: 'Bourke St Mall', rating: 3, author: 'Sarah Jenkins', comment: 'Good pedestrian space, watch for trams.', date: '2026-09-08' }
])

// Aggregated average rating score (BR C.3 core requirement)
const averageRating = computed(() => {
  if (reviewList.value.length === 0) return '0.0'
  const total = reviewList.value.reduce((acc, curr) => acc + Number(curr.rating || 0), 0)
  return (total / reviewList.value.length).toFixed(1)
})

// ================= BR C.4: Basic Security & Input Sanitization =================
// Simple sanitization helper to strip angle brackets (< >) preventing script injection
function sanitizeInput(str) {
  if (!str) return ''
  return str.replace(/[<>]/g, '').trim()
}
// ===============================================================================

function addReview() {
  reviewErrors.value = { route: '', author: '', comment: '' }
  let isValid = true

  if (!reviewForm.value.route.trim()) {
    reviewErrors.value.route = 'Route name is required.'
    isValid = false
  } else if (/[<>]/.test(reviewForm.value.route)) {
    reviewErrors.value.route = 'Security notice: HTML characters (< >) are not permitted.'
    isValid = false
  }

  if (!reviewForm.value.author.trim()) {
    reviewErrors.value.author = 'Reviewer name is required.'
    isValid = false
  } else if (/[<>]/.test(reviewForm.value.author)) {
    reviewErrors.value.author = 'Security notice: HTML characters (< >) are not permitted.'
    isValid = false
  }

  if (!reviewForm.value.comment.trim()) {
    reviewErrors.value.comment = 'Comment is required.'
    isValid = false
  } else if (/[<>]/.test(reviewForm.value.comment)) {
    reviewErrors.value.comment = 'Security notice: HTML characters (< >) are not permitted.'
    isValid = false
  }

  if (!isValid) return

  reviewList.value.unshift({
    id: Date.now(),
    route: sanitizeInput(reviewForm.value.route),
    rating: Number(reviewForm.value.rating),
    author: sanitizeInput(reviewForm.value.author),
    comment: sanitizeInput(reviewForm.value.comment),
    date: '2026-09-09'
  })

  // Reset form inputs (keep author if still logged in)
  reviewForm.value.route = ''
  reviewForm.value.comment = ''
  reviewForm.value.rating = 5
  if (currentUser.value) {
    reviewForm.value.author = currentUser.value
  }
}

function deleteReview(id) {
  reviewList.value = reviewList.value.filter(item => item.id !== id)
}
// ==============================================================================
</script>

<style>
body {
  background-color: #f8fafc;
}
</style>
