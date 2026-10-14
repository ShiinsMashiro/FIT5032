import { initializeApp } from 'firebase/app'
import { getFirestore } from 'firebase/firestore'

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: 'AIzaSyCDiEFwXO0ShatsplhF0eJAJ4DYj-d6lGA',
  authDomain: 'fit5032-bb088.firebaseapp.com',
  projectId: 'fit5032-bb088',
  storageBucket: 'fit5032-bb088.firebasestorage.app',
  messagingSenderId: '706395938606',
  appId: '1:706395938606:web:bae93d4b30e42c89f124bf'
}

// Initialize Firebase
initializeApp(firebaseConfig)
const db = getFirestore()
export default db
