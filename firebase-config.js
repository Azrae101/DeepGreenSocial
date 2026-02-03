// firebase-config.js
// Shared Firebase configuration for all pages

const firebaseConfig = {
    apiKey: "AIzaSyDAnzTtMgBJ57NjqsE7Te0htmMV9nf_gLg",
    authDomain: "social-green-4d772.firebaseapp.com",
    projectId: "social-green-4d772",
    storageBucket: "social-green-4d772.firebasestorage.app",
    messagingSenderId: "81847906637",
    appId: "1:81847906637:web:9eaf5e8cd1cd5d659d05bb"
    // Note: Using the SAME appId as login/register
};

// Initialize Firebase (compat version for simplicity)
firebase.initializeApp(firebaseConfig);

// Make Firebase services globally available
const auth = firebase.auth();
const db = firebase.firestore();
const storage = firebase.storage();

// Export for modular use if needed
window.firebaseApp = firebase.app();
window.firebaseAuth = auth;
window.firebaseDb = db;
window.firebaseStorage = storage;