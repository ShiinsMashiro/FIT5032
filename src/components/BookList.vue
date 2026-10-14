<template>
  <h2>Books with ISBN > 1000</h2>
  <ul>
    <li v-for="book in books" :key="book.id">
      {{ book.name }} (ISBN: {{ book.isbn }})
    </li>
  </ul>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { collection, query, where, orderBy, limit, getDocs } from 'firebase/firestore'
import db from '../firebase/init.js'

const books = ref([])

const fetchBooks = async () => {
  try {
    const q = query(
      collection(db, 'books'),
      where('isbn', '>', 1000),
      orderBy('isbn'),
      limit(10)
    )
    const querySnapshot = await getDocs(q)
    const booksArray = []
    querySnapshot.forEach((doc) => {
      booksArray.push({ id: doc.id, ...doc.data() })
    })
    books.value = booksArray
  } catch (error) {
    console.error('Error fetching books:', error)
  }
}

onMounted(() => {
  fetchBooks()
})
</script>
