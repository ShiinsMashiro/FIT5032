<template>
  <div class="container my-4" style="max-width: 800px;">
    <!-- Title Banner -->
    <div class="p-3 mb-4 bg-light border text-center rounded">
      <h3 class="text-dark mb-1 fw-bold">Commuter Trip Records</h3>
      <p class="text-muted mb-0 small">Interactive Data Table with Pagination, Sorting & Filtering</p>
    </div>

    <!-- Add Trip Form Card -->
    <div class="card p-3 mb-4 border bg-white shadow-sm">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <h5 class="mb-0 fw-bold">Add Commuter Trip</h5>
        <button class="btn btn-sm btn-outline-secondary" @click="showForm = !showForm">
          {{ showForm ? 'Hide Form' : 'Show Form' }}
        </button>
      </div>

      <form v-if="showForm" @submit.prevent="addTrip" class="mt-3">
        <div class="row g-2 mb-2">
          <div class="col-md-6">
            <label class="form-label small">Commuter Name:</label>
            <input v-model="formData.name" type="text" class="form-control form-control-sm" placeholder="Enter commuter name" />
            <div v-if="errors.name" class="text-danger small mt-1">{{ errors.name }}</div>
          </div>
          <div class="col-md-6">
            <label class="form-label small">Trip Date:</label>
            <input v-model="formData.date" type="date" class="form-control form-control-sm" />
            <div v-if="errors.date" class="text-danger small mt-1">{{ errors.date }}</div>
          </div>
        </div>

        <div class="row g-2 mb-3">
          <div class="col-md-6">
            <label class="form-label small">Distance (km):</label>
            <input v-model="formData.distance" type="number" step="any" min="0.1" class="form-control form-control-sm" placeholder="Enter distance (> 0)" />
            <div v-if="errors.distance" class="text-danger small mt-1">{{ errors.distance }}</div>
          </div>
          <div class="col-md-6">
            <label class="form-label small">Transport Mode:</label>
            <select v-model="formData.mode" class="form-select form-select-sm">
              <option value="">Select mode</option>
              <option value="Walking">Walking</option>
              <option value="Cycling">Cycling</option>
              <option value="Public Transport">Public Transport</option>
              <option value="E-Scooter">E-Scooter</option>
            </select>
            <div v-if="errors.mode" class="text-danger small mt-1">{{ errors.mode }}</div>
          </div>
        </div>

        <div class="d-flex gap-2">
          <button type="submit" class="btn btn-sm btn-dark flex-grow-1">Save Trip</button>
          <button type="button" class="btn btn-sm btn-secondary px-3" @click="clearForm">Clear</button>
        </div>
      </form>
    </div>

    <!-- Trip Records Table Card -->
    <div class="card p-3 mb-4 border bg-white shadow-sm">
      <div class="d-flex flex-wrap justify-content-between align-items-center mb-3 gap-2">
        <div>
          <h5 class="mb-0 fw-bold">Trip Records List</h5>
          <small class="text-muted">Total {{ filteredTrips.length }} records found</small>
        </div>
        <div class="d-flex gap-2">
          <input 
            v-model="searchKeyword" 
            type="text" 
            class="form-control form-control-sm" 
            style="width: 160px;" 
            placeholder="Search keyword..." 
          />
          <select v-model="selectedMode" class="form-select form-select-sm" style="width: 140px;">
            <option value="">All Modes</option>
            <option value="Walking">Walking</option>
            <option value="Cycling">Cycling</option>
            <option value="Public Transport">Public Transport</option>
            <option value="E-Scooter">E-Scooter</option>
          </select>
        </div>
      </div>

      <div v-if="paginatedTrips.length === 0" class="text-center text-muted py-3 border bg-light rounded">
        No trip records match the current filters.
      </div>

      <div v-else class="table-responsive">
        <table class="table table-bordered mb-2">
        <thead class="table-light">
          <tr>
            <th style="width: 8%;">No.</th>
            <th @click="sortBy('date')" style="cursor: pointer;">
              Date <span class="small text-muted">&#x21C5;</span>
            </th>
            <th @click="sortBy('name')" style="cursor: pointer;">
              Commuter <span class="small text-muted">&#x21C5;</span>
            </th>
            <th @click="sortBy('mode')" style="cursor: pointer;">
              Mode <span class="small text-muted">&#x21C5;</span>
            </th>
            <th @click="sortBy('distance')" style="cursor: pointer;">
              Distance <span class="small text-muted">&#x21C5;</span>
            </th>
            <th style="width: 14%;" class="text-center">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in paginatedTrips" :key="item.id || index">
            <td>{{ (currentPage - 1) * pageSize + index + 1 }}</td>
            <td>{{ item.date }}</td>
            <td>{{ item.name }}</td>
            <td>
              <span class="badge bg-light text-dark border">{{ item.mode }}</span>
            </td>
            <td>{{ Number(item.distance).toFixed(1) }} km</td>
            <td class="text-center">
              <button 
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
  deleteDoc, 
  doc, 
  serverTimestamp 
} from 'firebase/firestore'

const showForm = ref(true)
const formData = ref({
  name: '',
  date: new Date().toISOString().split('T')[0],
  distance: '',
  mode: ''
})
const errors = ref({})

// Trips come only from the Firestore 'trips' collection, so the table,
// the home page metrics and the cloud function all use the same records.
const trips = ref([])
const pageSize = 10
const currentPage = ref(1)
const sortKey = ref('date')
const sortAsc = ref(false)
const searchKeyword = ref('')
const selectedMode = ref('')

onMounted(() => {
  onSnapshot(collection(db, 'trips'), (snapshot) => {
    trips.value = snapshot.docs.map(d => ({ id: d.id, ...d.data() }))
  }, (err) => console.error('Trips sync failed:', err))
})

// Angle brackets are rejected so that markup cannot be stored in the shared records.
const hasMarkup = (text) => /[<>]/.test(text)

const addTrip = async () => {
  errors.value = {}
  const name = formData.value.name.trim()
  if (!name) errors.value.name = 'Please enter name'
  else if (hasMarkup(name)) errors.value.name = 'Name cannot contain < or > characters'
  if (!formData.value.date) errors.value.date = 'Please enter date'
  if (!formData.value.distance || Number(formData.value.distance) <= 0) {
    errors.value.distance = 'Distance must be a positive number greater than 0'
  }
  if (!formData.value.mode) errors.value.mode = 'Please select mode'

  if (Object.keys(errors.value).length > 0) return

  const item = {
    name,
    date: formData.value.date,
    mode: formData.value.mode,
    distance: Number(formData.value.distance)
  }

  // The onSnapshot listener adds the new record to the table, so no local insert is needed.
  try {
    await addDoc(collection(db, 'trips'), { ...item, createdAt: serverTimestamp() })
  } catch (e) {
    alert('Could not save the trip. Please try again.')
    return
  }

  clearForm()
}

const clearForm = () => {
  formData.value = {
    name: '',
    date: new Date().toISOString().split('T')[0],
    distance: '',
    mode: ''
  }
  errors.value = {}
}

const deleteTrip = async (id) => {
  trips.value = trips.value.filter(t => t.id !== id)
  try {
    await deleteDoc(doc(db, 'trips', id))
  } catch (e) {}
}

const sortBy = (key) => {
  if (sortKey.value === key) {
    sortAsc.value = !sortAsc.value
  } else {
    sortKey.value = key
    sortAsc.value = true
  }
}

const filteredTrips = computed(() => {
  let list = [...trips.value]
  if (searchKeyword.value) {
    const kw = searchKeyword.value.toLowerCase()
    list = list.filter(t => 
      (t.name || '').toLowerCase().includes(kw) ||
      (t.date || '').toLowerCase().includes(kw)
    )
  }
  if (selectedMode.value) {
    list = list.filter(t => t.mode === selectedMode.value)
  }

  list.sort((a, b) => {
    let va = a[sortKey.value]
    let vb = b[sortKey.value]
    if (sortKey.value === 'distance') {
      va = Number(va) || 0
      vb = Number(vb) || 0
    }
    if (va < vb) return sortAsc.value ? -1 : 1
    if (va > vb) return sortAsc.value ? 1 : -1
    return 0
  })

  return list
})

const totalPages = computed(() => Math.ceil(filteredTrips.value.length / pageSize) || 1)
const paginatedTrips = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredTrips.value.slice(start, start + pageSize)
})
</script>
