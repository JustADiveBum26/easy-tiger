// Hidden admin page: approve or delete photos, and clear out guest book entries.
// Talks to EasyStore only (js/store.js), same as the main page.
(function () {
  var store = window.EasyStore;
  var signinEl = document.getElementById('signin');
  var panelEl = document.getElementById('panel');

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text) e.textContent = text;
    return e;
  }

  function button(label, solid, onClick) {
    var b = el('button', solid ? 'btn btn-solid' : 'btn', label);
    b.type = 'button';
    b.addEventListener('click', onClick);
    return b;
  }

  function niceDate(ts) {
    return new Date(ts).toLocaleString(undefined, { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
  }

  function photoCard(p, waiting) {
    var card = el('figure', 'photo admin-photo');
    var mat = el('div', 'photo-mat');
    var img = el('img');
    img.src = p.src;
    img.alt = p.caption || 'Uploaded photo';
    mat.appendChild(img);
    card.appendChild(mat);
    card.appendChild(el('figcaption', '', (p.caption ? p.caption + ' · ' : '') + niceDate(p.ts)));
    var row = el('div', 'admin-actions');
    if (waiting) {
      row.appendChild(button('Approve', true, function () { store.approvePhoto(p.id).then(render); }));
    }
    row.appendChild(button('Delete', false, function () {
      if (confirm('Delete this photo for good?')) store.deletePhoto(p.id).then(render);
    }));
    card.appendChild(row);
    return card;
  }

  function fill(box, list, makeCard, emptyText) {
    box.textContent = '';
    if (!list.length) box.appendChild(el('p', 'placeholder', emptyText));
    list.forEach(function (item) { box.appendChild(makeCard(item)); });
  }

  function guestbookRow(e, waiting) {
    var row = el('div', 'admin-gb-row');
    var text = el('div', 'admin-gb-text');
    text.appendChild(el('p', 'gb-note', e.note));
    var by = el('p', 'gb-by');
    by.appendChild(el('b', '', e.name));
    by.appendChild(document.createTextNode(' · ' + niceDate(e.ts)));
    text.appendChild(by);
    row.appendChild(text);
    var actions = el('div', 'admin-actions');
    if (waiting) {
      actions.appendChild(button('Approve', true, function () { store.approveGuestbook(e.id).then(render); }));
    }
    actions.appendChild(button('Delete', false, function () {
      if (confirm('Delete this entry?')) store.deleteGuestbook(e.id).then(render);
    }));
    row.appendChild(actions);
    return row;
  }

  var BASE_TITLE = 'Easy Tiger \u00b7 Admin';

  // Shows how many things are waiting, on the page and in the browser tab's title,
  // so a pinned tab tells you at a glance.
  function setWaiting(photos, notes) {
    var total = photos + notes;
    document.title = (total ? '(' + total + ') ' : '') + BASE_TITLE;
    var parts = [];
    if (photos) parts.push(photos + (photos === 1 ? ' photo' : ' photos'));
    if (notes) parts.push(notes + (notes === 1 ? ' guest book note' : ' guest book notes'));
    var line = document.getElementById('admin-summary');
    line.textContent = total ? parts.join(' and ') + ' waiting for you.' : 'Nothing waiting. You are all caught up.';
    line.className = 'admin-summary' + (total ? ' has-waiting' : '');
  }

  function showSignedOut(message) {
    signinEl.hidden = false;
    panelEl.hidden = true;
    document.title = BASE_TITLE;
    document.getElementById('signin-msg').textContent = message || '';
  }

  function render() {
    store.isAdmin().then(function (ok) {
      if (!ok) { showSignedOut(); return; }
      signinEl.hidden = true;
      panelEl.hidden = false;

      return Promise.all([
        store.listPhotos({ approved: false }),
        store.listPhotos({ approved: true }),
        store.listGuestbook({ approved: false }),
        store.listGuestbook({ approved: true })
      ]).then(function (r) {
        setWaiting(r[0].length, r[2].length);
        document.getElementById('pending-count').textContent = '(' + r[0].length + ')';
        document.getElementById('approved-count').textContent = '(' + r[1].length + ')';
        document.getElementById('gb-pending-count').textContent = '(' + r[2].length + ')';
        document.getElementById('gb-count').textContent = '(' + r[3].length + ')';

        fill(document.getElementById('pending'), r[0], function (p) { return photoCard(p, true); }, 'Nothing waiting.');
        fill(document.getElementById('approved'), r[1], function (p) { return photoCard(p, false); }, 'No photos on the wall yet.');
        fill(document.getElementById('gb-pending'), r[2], function (e) { return guestbookRow(e, true); }, 'Nothing waiting.');
        fill(document.getElementById('gb'), r[3], function (e) { return guestbookRow(e, false); }, 'No entries yet.');
      });
    }).catch(function (err) {
      showSignedOut('Something went wrong: ' + err.message);
    });
  }

  if (store.isDemo) document.getElementById('demo-note').hidden = false;

  document.getElementById('signin-btn').addEventListener('click', function () {
    store.adminSignIn().then(render).catch(function (err) { showSignedOut(err.message); });
  });
  document.getElementById('signout-btn').addEventListener('click', function () { store.adminSignOut().then(render); });

  render();

  // Quiet refresh so an open (or pinned) tab keeps its count current.
  setInterval(function () { if (!panelEl.hidden) render(); }, 120000);
})();
