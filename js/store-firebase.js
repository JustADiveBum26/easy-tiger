// REAL STORE. Guest book and photo notes live in Firebase (Firestore), photo files live in
// Cloudinary. It replaces the demo store in js/store.js only when js/firebase-config.js is
// filled in and the Firebase scripts loaded. Same functions as the demo store, so main.js
// and admin.js don't know the difference.
//
// How the approval works:
//   Guests write to a "Pending" collection. Only Bradley can read that, so the house
//   password they typed (stored with the entry so the rules can check it) is never public.
//   Approving copies the entry, without the password, into the public collection.
(function () {
  var cfg = window.EASY_TIGER_CONFIG;
  if (!cfg || !cfg.firebase || !cfg.firebase.projectId || typeof firebase === 'undefined') return;

  firebase.initializeApp(cfg.firebase);
  var db = firebase.firestore();
  var auth = firebase.auth();
  var stamp = firebase.firestore.FieldValue.serverTimestamp;

  var WRONG_PASSWORD = 'That is not the house password.';

  function ms(t) { return t && t.toMillis ? t.toMillis() : Date.now(); }
  function fail(msg) { return Promise.reject(new Error(msg)); }

  // Firestore says "permission-denied" when the rules say no. The only thing a guest can
  // get wrong that the page doesn't already check is the password.
  function friendly(err) {
    if (err && err.code === 'permission-denied') return new Error(WRONG_PASSWORD);
    return new Error('Something went wrong. Try again in a minute.');
  }

  // Cloudinary shrinks and converts on the fly when we ask in the web address.
  function wallSrc(url) {
    return url.replace('/upload/', '/upload/c_limit,w_1200,q_auto,f_auto/');
  }

  function guestbookDoc(d) {
    var x = d.data();
    return { id: d.id, name: x.name, note: x.note, ts: ms(x.ts) };
  }
  function photoDoc(d) {
    var x = d.data();
    return { id: d.id, caption: x.caption || '', src: wallSrc(x.src), ts: ms(x.ts) };
  }

  // Move one waiting document into the public collection, without the password.
  function approve(pendingName, publicName, fields) {
    return function (id) {
      var from = db.collection(pendingName).doc(id);
      return from.get().then(function (snap) {
        if (!snap.exists) return;
        var data = {};
        fields.forEach(function (f) { data[f] = snap.data()[f]; });
        var batch = db.batch();
        batch.set(db.collection(publicName).doc(id), data);
        batch.delete(from);
        return batch.commit();
      });
    };
  }

  // Delete from wherever it is (waiting or public). Deleting a missing document does nothing.
  function remove(pendingName, publicName) {
    return function (id) {
      var batch = db.batch();
      batch.delete(db.collection(pendingName).doc(id));
      batch.delete(db.collection(publicName).doc(id));
      return batch.commit();
    };
  }

  function list(name, map) {
    return db.collection(name).orderBy('ts', 'desc').get().then(function (snap) {
      return snap.docs.map(map);
    });
  }

  function uploadToCloudinary(dataUrl) {
    var c = cfg.cloudinary || {};
    if (!c.cloudName || !c.uploadPreset) return fail('Photo uploads are not set up yet.');
    return fetch(dataUrl).then(function (r) { return r.blob(); }).then(function (blob) {
      var form = new FormData();
      form.append('file', blob, 'photo.jpg');
      form.append('upload_preset', c.uploadPreset);
      return fetch('https://api.cloudinary.com/v1_1/' + c.cloudName + '/image/upload', { method: 'POST', body: form });
    }).then(function (r) {
      if (!r.ok) throw new Error('upload failed');
      return r.json();
    });
  }

  window.EasyStore = {
    isDemo: false,

    // ----- guest book -----
    listGuestbook: function (opts) {
      var waiting = opts && opts.approved === false;
      return list(waiting ? 'guestbookPending' : 'guestbook', guestbookDoc);
    },
    addGuestbook: function (entry) {
      var name = (entry.name || '').trim();
      var note = (entry.note || '').trim();
      if (!name || name.length > 60) return fail('Add a name (60 letters or fewer).');
      if (!note || note.length > 400) return fail('Add a note (400 letters or fewer).');
      if (!entry.password) return fail(WRONG_PASSWORD);
      return db.collection('guestbookPending')
        .add({ name: name, note: note, key: entry.password, ts: stamp() })
        .then(function () {}, function (err) { throw friendly(err); });
    },
    approveGuestbook: approve('guestbookPending', 'guestbook', ['name', 'note', 'ts']),
    deleteGuestbook: remove('guestbookPending', 'guestbook'),

    // ----- photos -----
    listPhotos: function (opts) {
      var waiting = opts && opts.approved === false;
      return list(waiting ? 'photosPending' : 'photos', photoDoc);
    },
    addPhoto: function (photo) {
      var caption = (photo.caption || '').trim();
      if (!/^data:image\//.test(photo.dataUrl || '')) return fail('That does not look like a photo.');
      if (caption.length > 80) return fail('Keep the caption to 80 letters.');
      if (!photo.password) return fail(WRONG_PASSWORD);
      return uploadToCloudinary(photo.dataUrl).then(function (up) {
        return db.collection('photosPending')
          .add({ src: up.secure_url, caption: caption, key: photo.password, ts: stamp() })
          .then(function () {}, function (err) { throw friendly(err); });
      }, function (err) {
        throw err && err.message === 'Photo uploads are not set up yet.' ? err : new Error('The photo would not upload. Try again.');
      });
    },
    approvePhoto: approve('photosPending', 'photos', ['src', 'caption', 'ts']),
    deletePhoto: remove('photosPending', 'photos'),

    // ----- admin: Google sign-in, and the rules decide if it is really Bradley -----
    isAdmin: function () {
      return new Promise(function (resolve) {
        var off = auth.onAuthStateChanged(function (user) {
          off();
          if (!user) return resolve(false);
          // Only the admin is allowed to read the waiting list, so a successful read means yes.
          db.collection('photosPending').limit(1).get().then(function () { resolve(true); }, function () { resolve(false); });
        });
      });
    },
    adminSignIn: function () {
      return auth.signInWithPopup(new firebase.auth.GoogleAuthProvider()).then(function () {
        return window.EasyStore.isAdmin().then(function (ok) {
          if (!ok) return auth.signOut().then(function () { throw new Error('That Google account is not the admin.'); });
        });
      }, function (err) {
        if (err && err.code === 'auth/popup-closed-by-user') throw new Error('Sign-in was closed.');
        throw new Error('Could not sign in.');
      });
    },
    adminSignOut: function () { return auth.signOut(); }
  };
})();
