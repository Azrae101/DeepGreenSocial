# Firestore Security Rules

**Problem:** Users cannot see posts without being logged in. The Firestore rules are blocking read access for unauthenticated users.

**Solution:** Update your Firestore rules to allow unauthenticated users to read approved posts.

## Rules to Apply

Copy and paste these rules into your Firebase Firestore console:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow anyone (authenticated or not) to read approved posts
    match /posts/{postId} {
      allow read: if resource.data.approved == true;
      allow create: if request.auth != null;
      allow update, delete: if request.auth != null && (resource.data.userId == request.auth.token.email || request.auth.token.email in ['clara.holst@outlook.com', 'clar.holst@gmail.com', 'admin@socialgreen.com', 'socialandgreen@gmail.com']);
    }
    
    // Allow users to read and write their own user documents
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }
  }
}
```

## How to Apply

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project: **social-green-4d772**
3. Navigate to **Firestore Database** → **Rules** tab
4. Delete any existing rules
5. Paste the rules above
6. Click **Publish**

## What These Rules Do

- ✅ Unauthenticated users can **read approved posts** (`approved == true`)
- ✅ Unauthenticated users can **view admin posts** (admins auto-approve their posts)
- ✅ Logged-in users can **create new posts** (will be pending approval)
- ✅ Only admins and post authors can **delete posts**
- ✅ Users can only access their own user documents

## Testing

After applying the rules:
1. Reload `community.html` without logging in
2. You should see approved posts and admin posts
3. Login to create new posts (posts will need admin approval)
