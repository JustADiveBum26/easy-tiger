// DEMO STORE. Saves the guest book and photos in this one browser only, so nothing
// is shared between guests. It exists so we can see how everything looks and works.
//
// Later this file gets swapped for a Firebase version with the same functions, so
// main.js and admin.js don't have to change. Every function returns a Promise on purpose.
//
// The password here is only for the demo. The real house password never goes in this repo.
(function () {
  var GB = 'et_demo_guestbook';
  var PH = 'et_demo_photos';
  var DEMO_PASSWORD = 'tiger';

  function read(key) {
    try { return JSON.parse(localStorage.getItem(key) || '[]'); } catch (e) { return []; }
  }
  function write(key, list) {
    try { localStorage.setItem(key, JSON.stringify(list)); return true; } catch (e) { return false; }
  }
  function newId() { return Date.now().toString(36) + Math.random().toString(36).slice(2, 7); }
  function fail(msg) { return Promise.reject(new Error(msg)); }
  function newestFirst(a, b) { return b.ts - a.ts; }

  // Same limits the Firebase rules will enforce later.
  function checkPassword(pw) {
    return pw === DEMO_PASSWORD ? null : 'That is not the house password.';
  }

  window.EasyStore = {
    isDemo: true,
    demoPassword: DEMO_PASSWORD,

    // ----- guest book -----
    // Wall: only approved. Admin: pass { approved: false } for the ones waiting.
    listGuestbook: function (opts) {
      var list = read(GB).sort(newestFirst);
      var want = opts && opts.approved === false ? false : true;
      return Promise.resolve(list.filter(function (e) { return !!e.approved === want; }));
    },
    addGuestbook: function (entry) {
      var name = (entry.name || '').trim();
      var note = (entry.note || '').trim();
      var bad = checkPassword(entry.password);
      if (bad) return fail(bad);
      if (!name || name.length > 60) return fail('Add a name (60 letters or fewer).');
      if (!note || note.length > 400) return fail('Add a note (400 letters or fewer).');
      var list = read(GB);
      list.push({ id: newId(), name: name, note: note, approved: false, ts: Date.now() });
      return write(GB, list) ? Promise.resolve() : fail('This browser is out of room to save it.');
    },
    approveGuestbook: function (id) {
      var list = read(GB);
      list.forEach(function (e) { if (e.id === id) e.approved = true; });
      write(GB, list);
      return Promise.resolve();
    },
    deleteGuestbook: function (id) {
      write(GB, read(GB).filter(function (e) { return e.id !== id; }));
      return Promise.resolve();
    },

    // ----- photos -----
    // Wall: only approved. Admin: everything.
    listPhotos: function (opts) {
      var list = read(PH).sort(newestFirst);
      if (opts && opts.approved === true) list = list.filter(function (p) { return p.approved; });
      if (opts && opts.approved === false) list = list.filter(function (p) { return !p.approved; });
      return Promise.resolve(list);
    },
    addPhoto: function (photo) {
      var bad = checkPassword(photo.password);
      if (bad) return fail(bad);
      if (!/^data:image\//.test(photo.dataUrl || '')) return fail('That does not look like a photo.');
      var caption = (photo.caption || '').trim();
      if (caption.length > 80) return fail('Keep the caption to 80 letters.');
      var list = read(PH);
      list.push({ id: newId(), caption: caption, src: photo.dataUrl, approved: false, ts: Date.now() });
      return write(PH, list) ? Promise.resolve() : fail('This browser is out of room to save more photos.');
    },
    approvePhoto: function (id) {
      var list = read(PH);
      list.forEach(function (p) { if (p.id === id) p.approved = true; });
      write(PH, list);
      return Promise.resolve();
    },
    deletePhoto: function (id) {
      write(PH, read(PH).filter(function (p) { return p.id !== id; }));
      return Promise.resolve();
    },

    // ----- admin sign-in (demo: just a button) -----
    isAdmin: function () {
      try { return Promise.resolve(sessionStorage.getItem('et_demo_admin') === '1'); } catch (e) { return Promise.resolve(false); }
    },
    adminSignIn: function () {
      try { sessionStorage.setItem('et_demo_admin', '1'); } catch (e) { /* ignore */ }
      return Promise.resolve();
    },
    adminSignOut: function () {
      try { sessionStorage.removeItem('et_demo_admin'); } catch (e) { /* ignore */ }
      return Promise.resolve();
    }
  };
})();
