// Settings for the real guest book and photo wall.
//
// None of these values are secret. They only say WHERE the data lives. What protects the
// data is the rules in firestore.rules. Leave a value empty and the site stays in demo mode.
//
// The house password and the admin email are NOT here. They live in two documents inside
// Firebase (config/house and config/admin) that only Bradley can edit, from the Firebase console.
window.EASY_TIGER_CONFIG = {
  firebase: {
    apiKey: 'AIzaSyBKSrju1ybKcL26tDMra5I3tmNvEXcqf2w',
    authDomain: 'easy-tiger-como.firebaseapp.com',
    projectId: 'easy-tiger-como',
    appId: '1:817764359074:web:1893e95689aa647d9830fb'
  },
  // Knock to Enter. Empty hash = no gate. To turn it on, run:
  //   python tools/make-knock-hash.py "the secret words"
  // and paste the long code it prints between the quotes. It is a fun gate, not real security.
  knock: {
    hash: '1111e6e907b39632ca3fa649d0c6ba41fc1d610c65204d8cd8a2a78a7c3980a9'
  },
  cloudinary: {
    cloudName: 'czj4oq2l',
    uploadPreset: 'easy-tiger-guests'   // an UNSIGNED preset, set up in the Cloudinary dashboard
  }
};
