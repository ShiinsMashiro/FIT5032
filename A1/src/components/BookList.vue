<script setup>
import { ref, computed } from 'vue'

// Reactive State (Activity 1 & Activity 4)
const searchQuery = ref('')
const selectedCategory = ref('All')
const isHighlightEnabled = ref(true)

// New Book Form Input (Activity 1)
const newTitle = ref('')
const newAuthor = ref('')
const newYear = ref('')

// Book Catalog Dataset (Activity 4)
const books = ref([
  { id: 1, title: '1984', author: 'George Orwell', year: 1949, category: 'Dystopian' },
  { id: 2, title: 'Animal Farm', author: 'George Orwell', year: 1945, category: 'Political Satire' },
  { id: 3, title: 'To Kill a Mockingbird', author: 'Harper Lee', year: 1960, category: 'Classic' },
  { id: 4, title: 'The Great Gatsby', author: 'F. Scott Fitzgerald', year: 1925, category: 'Classic' },
  { id: 5, title: 'Brave New World', author: 'Aldous Huxley', year: 1932, category: 'Dystopian' },
  { id: 6, title: 'Homage to Catalonia', author: 'George Orwell', year: 1938, category: 'Autobiography' }
])

// Computed Property: Filtered Books (Activity 2)
const filteredBooks = computed(() => {
  return books.value.filter((book) => {
    const matchesSearch =
      book.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      book.author.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory =
      selectedCategory.value === 'All' || book.category === selectedCategory.value

    return matchesSearch && matchesCategory
  })
})

// Computed Property: Total Books Count (Activity 2)
const totalBooks = computed(() => books.value.length)

// Computed Property: George Orwell Books Count (Activity 2 & Task 2.2)
const orwellBooksCount = computed(() => {
  return books.value.filter((b) => b.author === 'George Orwell').length
})

// Event Handling Methods (Activity 3)
const addBook = () => {
  if (!newTitle.value.trim() || !newAuthor.value.trim()) return

  books.value.push({
    id: Date.now(),
    title: newTitle.value.trim(),
    author: newAuthor.value.trim(),
    year: Number(newYear.value) || 2026,
    category: 'General'
  })

  newTitle.value = ''
  newAuthor.value = ''
  newYear.value = ''
}

const removeBook = (id) => {
  books.value = books.value.filter((book) => book.id !== id)
}
</script>

<template>
  <div class="task2-container">
    <!-- Header Section -->
    <header class="header">
      <h1>FIT5032 — Task 2: Book Library App</h1>
      <p class="subtitle">Computed Properties, Directives & Attribute Binding</p>
    </header>

    <!-- Activity 1: Directives & Form Input Binding (v-model & v-on) -->
    <section class="card form-section">
      <h2>Activity 1 & 3: Add New Book</h2>
      <form @submit.prevent="addBook" class="add-form">
        <input v-model="newTitle" placeholder="Book Title" required class="input" />
        <input v-model="newAuthor" placeholder="Author Name" required class="input" />
        <input v-model="newYear" type="number" placeholder="Year" class="input input-small" />
        <button type="submit" class="btn btn-primary">Add Book</button>
      </form>
    </section>

    <!-- Activity 2: Search & Filter (v-model, Computed Properties) -->
    <section class="card filter-section">
      <h2>Activity 2: Filter & Search Catalog</h2>
      <div class="filter-controls">
        <input
          v-model="searchQuery"
          placeholder="Search by title or author..."
          class="input search-input"
        />
        <select v-model="selectedCategory" class="select">
          <option value="All">All Categories</option>
          <option value="Dystopian">Dystopian</option>
          <option value="Classic">Classic</option>
          <option value="Political Satire">Political Satire</option>
          <option value="Autobiography">Autobiography</option>
          <option value="General">General</option>
        </select>
        <button
          @click="isHighlightEnabled = !isHighlightEnabled"
          class="btn btn-toggle"
          :class="{ active: isHighlightEnabled }"
        >
          {{ isHighlightEnabled ? 'Highlight: ON' : 'Highlight: OFF' }}
        </button>
      </div>

      <!-- Stats Bar using Computed Properties -->
      <div class="stats-bar">
        <span>Total Books: <strong>{{ totalBooks }}</strong></span>
        <span>Filtered Items: <strong>{{ filteredBooks.length }}</strong></span>
        <span class="orwell-stat">
          George Orwell Books: <strong>{{ orwellBooksCount }}</strong>
        </span>
      </div>
    </section>

    <!-- Activity 2 & Task 2.2: List Rendering (v-for) & Class/Style Binding for George Orwell -->
    <section class="card catalog-section">
      <h2>Activity 4 & Task 2.2: Book List (George Orwell Highlighted)</h2>

      <!-- Conditional Rendering (v-if / v-else) -->
      <div v-if="filteredBooks.length === 0" class="empty-state">
        <p>No books match your criteria.</p>
      </div>

      <ul v-else class="book-list">
        <!-- v-for rendering with Task 2.2 class and style binding for George Orwell -->
        <li
          v-for="book in filteredBooks"
          :key="book.id"
          class="book-item"
          :class="{
            'highlight-orwell': isHighlightEnabled && book.author === 'George Orwell'
          }"
          :style="
            isHighlightEnabled && book.author === 'George Orwell'
              ? { borderLeft: '6px solid #ff5500' }
              : {}
          "
        >
          <div class="book-info">
            <span class="book-title">{{ book.title }}</span>
            <span class="book-author">by {{ book.author }}</span>
            <span class="book-meta">({{ book.year }}) • {{ book.category }}</span>
          </div>

          <!-- Task 2.2 Badge for George Orwell -->
          <div class="actions">
            <span
              v-if="book.author === 'George Orwell'"
              class="orwell-badge"
            >
              Featured Author
            </span>
            <button @click="removeBook(book.id)" class="btn-delete" title="Remove Book">
              ✕
            </button>
          </div>
        </li>
      </ul>
    </section>
  </div>
</template>

<style scoped>
.task2-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: #111111;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.header h1 {
  font-size: 2.2rem;
  font-weight: 800;
  margin: 0;
  color: #111111;
}

.subtitle {
  color: #ff5500;
  font-weight: 600;
  margin-top: 0.4rem;
}

.card {
  background: #ffffff;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
}

.card h2 {
  font-size: 1.2rem;
  font-weight: 700;
  margin-top: 0;
  margin-bottom: 1rem;
  color: #111111;
}

.add-form {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.input,
.select {
  padding: 8px 14px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
}

.input:focus,
.select:focus {
  border-color: #ff5500;
}

.search-input {
  flex: 1;
  min-width: 200px;
}

.input-small {
  width: 90px;
}

.filter-controls {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.stats-bar {
  display: flex;
  gap: 20px;
  font-size: 0.9rem;
  background: #f8fafc;
  padding: 10px 14px;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

.orwell-stat {
  color: #ff5500;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #ff5500;
  color: #ffffff;
}

.btn-primary:hover {
  background: #e04b00;
}

.btn-toggle {
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #cbd5e1;
}

.btn-toggle.active {
  background: #fff7ed;
  color: #ea580c;
  border-color: #ff5500;
}

.book-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.book-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  margin-bottom: 10px;
  background: #ffffff;
  transition: all 0.2s ease;
}

/* Task 2.2: Class Binding for George Orwell Highlight */
.highlight-orwell {
  background-color: #fff7ed !important;
  border-color: #ffedd5 !important;
  box-shadow: 0 2px 8px rgba(255, 85, 0, 0.1);
}

.book-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.book-title {
  font-weight: 700;
  font-size: 1.05rem;
}

.book-author {
  font-weight: 600;
  color: #334155;
  font-size: 0.95rem;
}

.book-meta {
  font-size: 0.85rem;
  color: #64748b;
}

.actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.orwell-badge {
  background: #ff5500;
  color: #ffffff;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-delete {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 1.1rem;
  cursor: pointer;
  padding: 4px;
}

.btn-delete:hover {
  color: #ef4444;
}

.empty-state {
  text-align: center;
  color: #64748b;
  padding: 2rem;
}
</style>
