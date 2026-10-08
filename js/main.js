// Spirits menu. The drinks live in js/menu-data.js, made from the menu PDF.
// Start view lists the types. Clicking one opens its drinks in a fresh view, with a way back.
(function () {
  if (typeof MENU === 'undefined') {
    document.getElementById('menu-fallback').hidden = false;
    return;
  }

  var homeEl = document.getElementById('menu-home');
  var detailEl = document.getElementById('menu-detail');
  var typesEl = document.getElementById('menu-types');
  var titleEl = document.getElementById('menu-detail-title');
  var countEl = document.getElementById('menu-count');
  var listEl = document.getElementById('menu-list');
  var backEl = document.getElementById('menu-back');
  var cats = MENU.categories;

  // Whiskey has a mash bill. The rest list what they're made with.
  var MASH_BILL = { 'bourbon': 1, 'rye': 1, 'other-american-whiskey': 1 };

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text) e.textContent = text;
    return e;
  }

  // "Confirm on bottle" is a note to self in the menu file, so don't show it as a fact.
  function clean(v) {
    return !v || /^confirm on bottle$/i.test(v) ? '' : v;
  }

  function drinkRow(d, cat) {
    var row = el('details', 'drink');
    var sum = el('summary');
    var main = el('span', 'drink-main');
    main.appendChild(el('span', 'drink-name', d.name));
    main.appendChild(el('span', 'drink-maker', d.maker));
    sum.appendChild(main);
    var proof = clean(d.proof);
    if (proof) sum.appendChild(el('span', 'drink-proof', proof));
    row.appendChild(sum);

    var body = el('div', 'drink-body');
    if (d.notes) body.appendChild(el('p', '', d.notes));
    var facts = el('p', 'drink-facts');
    var age = clean(d.age), details = clean(d.details);
    if (age) {
      facts.appendChild(el('b', '', 'Age '));
      facts.appendChild(document.createTextNode(age + (details ? '  ·  ' : '')));
    }
    if (details) {
      facts.appendChild(el('b', '', MASH_BILL[cat.id] ? 'Mash bill ' : 'Made with '));
      facts.appendChild(document.createTextNode(details));
    }
    if (facts.firstChild) body.appendChild(facts);
    row.appendChild(body);
    return row;
  }

  function scrollToMenu() {
    document.getElementById('menu').scrollIntoView();
  }

  function openType(cat) {
    titleEl.textContent = cat.name;
    countEl.textContent = cat.drinks.length + (cat.drinks.length === 1 ? ' pour' : ' pours') + ' · tap one for the details';
    listEl.textContent = '';
    // House Drinks carry a base spirit, so show a small heading each time it changes.
    var lastBase = '';
    cat.drinks.forEach(function (d) {
      if (d.base && d.base !== lastBase) {
        listEl.appendChild(el('h4', 'drink-group', d.base));
        lastBase = d.base;
      }
      listEl.appendChild(drinkRow(d, cat));
    });
    homeEl.hidden = true;
    detailEl.hidden = false;
    scrollToMenu();
  }

  function closeType() {
    detailEl.hidden = true;
    homeEl.hidden = false;
    scrollToMenu();
  }

  cats.forEach(function (cat) {
    var li = el('li');
    var b = el('button', 'menu-type');
    b.type = 'button';
    b.appendChild(el('span', 'menu-type-name', cat.name));
    b.appendChild(el('span', 'menu-type-n', String(cat.drinks.length)));
    b.addEventListener('click', function () { openType(cat); });
    li.appendChild(b);
    typesEl.appendChild(li);
  });

  backEl.addEventListener('click', closeType);
})();

// ---------- Guest book and photo wall ----------
// All saving and loading goes through EasyStore (js/store.js), so this code stays the same
// when the demo store is swapped for the real one.
(function () {
  var store = window.EasyStore;
  if (!store) return;

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text) e.textContent = text;
    return e;
  }

  function niceDate(ts) {
    return new Date(ts).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
  }

  if (store.isDemo) {
    document.getElementById('demo-pw').textContent = store.demoPassword;
    document.getElementById('demo-note').hidden = false;
  }

  // ----- guest book -----
  var gbForm = document.getElementById('gb-form');
  var gbStatus = document.getElementById('gb-status');
  var gbEntries = document.getElementById('gb-entries');

  function showGuestbook() {
    store.listGuestbook({ approved: true }).then(function (list) {
      gbEntries.textContent = '';
      if (!list.length) {
        gbEntries.appendChild(el('p', 'placeholder', 'No one has signed yet. Be the first.'));
        return;
      }
      list.forEach(function (e) {
        var card = el('article', 'gb-entry');
        card.appendChild(el('p', 'gb-note', e.note));
        var by = el('p', 'gb-by');
        by.appendChild(el('b', '', e.name));
        by.appendChild(document.createTextNode(' \u00b7 ' + niceDate(e.ts)));
        card.appendChild(by);
        gbEntries.appendChild(card);
      });
    }).catch(function () {
      gbEntries.textContent = '';
      gbEntries.appendChild(el('p', 'placeholder', 'The guest book will not load right now.'));
    });
  }

  gbForm.addEventListener('submit', function (e) {
    e.preventDefault();
    gbStatus.textContent = '';
    store.addGuestbook({
      name: document.getElementById('gb-name').value,
      note: document.getElementById('gb-note').value,
      password: document.getElementById('gb-pass').value
    }).then(function () {
      gbForm.reset();
      gbStatus.textContent = 'Thanks for coming by. Your note will show up once Bradley approves it.';
      showGuestbook();
    }).catch(function (err) {
      gbStatus.textContent = err.message;
    });
  });

  // ----- photo wall -----
  var MAX_UPLOAD = 8 * 1024 * 1024;   // 8 MB, same cap the real rules will use
  var MAX_SIDE = 1400;                // shrink big phone photos before saving

  var addBtn = document.getElementById('add-photo');
  var fileEl = document.getElementById('photo-file');
  var photoForm = document.getElementById('photo-form');
  var previewEl = document.getElementById('photo-preview');
  var photoStatus = document.getElementById('photo-status');
  var wallEl = document.getElementById('wall');
  var pendingDataUrl = '';

  function emptyFrame() {
    var f = el('div', 'photo');
    var mat = el('div', 'photo-mat');
    mat.appendChild(el('div', 'photo-ph', 'Empty frame'));
    f.appendChild(mat);
    return f;
  }

  function showWall() {
    store.listPhotos({ approved: true }).then(function (list) {
      wallEl.textContent = '';
      if (!list.length) {
        for (var i = 0; i < 3; i++) wallEl.appendChild(emptyFrame());
        return;
      }
      list.forEach(function (p) {
        var fig = el('figure', 'photo');
        var mat = el('div', 'photo-mat');
        var img = el('img');
        img.src = p.src;
        img.alt = p.caption || 'A photo from a night at Easy Tiger';
        img.loading = 'lazy';
        mat.appendChild(img);
        fig.appendChild(mat);
        if (p.caption) fig.appendChild(el('figcaption', '', p.caption));
        wallEl.appendChild(fig);
      });
    });
  }

  function closePhotoForm() {
    photoForm.hidden = true;
    photoForm.reset();
    fileEl.value = '';
    previewEl.removeAttribute('src');
    pendingDataUrl = '';
  }

  // Shrinking in the browser also drops the camera data (location, etc.) from the photo.
  function shrink(file) {
    return new Promise(function (resolve, reject) {
      var url = URL.createObjectURL(file);
      var img = new Image();
      img.onload = function () {
        var scale = Math.min(1, MAX_SIDE / Math.max(img.naturalWidth, img.naturalHeight));
        var w = Math.round(img.naturalWidth * scale);
        var h = Math.round(img.naturalHeight * scale);
        var canvas = document.createElement('canvas');
        canvas.width = w; canvas.height = h;
        canvas.getContext('2d').drawImage(img, 0, 0, w, h);
        URL.revokeObjectURL(url);
        resolve(canvas.toDataURL('image/jpeg', 0.78));
      };
      img.onerror = function () { URL.revokeObjectURL(url); reject(new Error('That file would not open as a photo.')); };
      img.src = url;
    });
  }

  addBtn.addEventListener('click', function () { photoStatus.textContent = ''; fileEl.click(); });

  fileEl.addEventListener('change', function () {
    var file = fileEl.files && fileEl.files[0];
    if (!file) return;
    if (!/^image\//.test(file.type)) { photoStatus.textContent = 'Pick a photo, please.'; fileEl.value = ''; return; }
    if (file.size > MAX_UPLOAD) { photoStatus.textContent = 'That one is over 8 MB. Pick a smaller one.'; fileEl.value = ''; return; }
    photoStatus.textContent = 'Getting it ready...';
    shrink(file).then(function (dataUrl) {
      pendingDataUrl = dataUrl;
      previewEl.src = dataUrl;
      photoForm.hidden = false;
      photoStatus.textContent = '';
    }).catch(function (err) { photoStatus.textContent = err.message; });
  });

  document.getElementById('photo-cancel').addEventListener('click', function () {
    closePhotoForm();
    photoStatus.textContent = '';
  });

  photoForm.addEventListener('submit', function (e) {
    e.preventDefault();
    store.addPhoto({
      dataUrl: pendingDataUrl,
      caption: document.getElementById('photo-caption').value,
      password: document.getElementById('photo-pass').value
    }).then(function () {
      closePhotoForm();
      photoStatus.textContent = 'Got it. It will show up on the wall once Bradley approves it.';
    }).catch(function (err) {
      photoStatus.textContent = err.message;
    });
  });

  showGuestbook();
  showWall();
})();
