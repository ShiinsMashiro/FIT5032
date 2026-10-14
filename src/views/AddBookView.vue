<template>
  <h1>Add Book</h1>
  <form @submit.prevent="addBook">
    <div>
      <label for="isbn">ISBN:</label>
      <input type="text" v-model="isbn" id="isbn" required />
    </div>
    <div>
      <label for="name">Name:</label>
      <input type="text" v-model="name" id="name" required />
    </div>
    <button type="submit">Add Book</button>
  </form>

  <h2>Manage Books</h2>
  <ul>
    <li v-for="book in allBooks" :key="book.id">
      <input type="text" v-model="book.name" />
      (ISBN: {{ book.isbn }})
      <button @click="updateBook(book.id, book.name)">Update</button>
      <button @click="deleteBook(book.id)">Delete</button>
    </li>
  </ul>

  <BookList :key="listKey" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { collection, addDoc, getDocs, updateDoc, deleteDoc, doc } from 'firebase/firestore'
import db from '../firebase/init.js'
import BookList from '../components/BookList.vue'

const isbn = ref('')
const name = ref('')
const allBooks = ref([])
const listKey = ref(0)

const addBook = async () => {
  try {
    const isbnNumber = Number(isbn.value)
    if (isNaN(isbnNumber)) {
      alert('ISBN must be a valid number')
      return
    }
    await addDoc(collection(db, 'books'), {
      isbn: isbnNumber,
      name: name.value
    })
    isbn.value = ''
    name.value = ''
    alert('Book added successfully!')
    await loadBooks()
  } catch (error) {
    console.error('Error adding book:', error)
  }
}

const loadBooks = async () => {
  const snapshot = await getDocs(collection(db, 'books'))
  allBooks.value = snapshot.docs.map((d) => ({ id: d.id, ...d.data() }))
  listKey.value++
}

const updateBook = async (id, newName) => {
  try {
    await updateDoc(doc(db, 'books', id), { name: newName })
    console.log('Book updated:', id, '->', newName)
    await loadBooks()
  } catch (error) {
    console.error('Error updating book:', error)
  }
}

const deleteBook = async (id) => {
  try {
    await deleteDoc(doc(db, 'books', id))
    console.log('Book deleted:', id)
    await loadBooks()
  } catch (error) {
    console.error('Error deleting book:', error)
  }
}

onMounted(loadBooks)
</script>
