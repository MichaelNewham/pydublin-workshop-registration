/* =============================================================================
   event_registration/static/js/app.js
   =============================================================================
   The mandatory "at least one simple JavaScript interaction" for Option A.

   Two interactions, both pure vanilla JS (no libraries):
     1. Copy-to-clipboard: any element with class .js-copy-ref, when clicked,
        copies its data-ref attribute to the system clipboard and shows a
        confirmation tooltip.
     2. Live character counter: any textarea next to a .js-notes-counter
        updates the "NNN characters left" hint as the user types.

   The counter also dynamically turns red when over the limit.
   ========================================================================== */

(function () {
  'use strict';

  // ---- 1. Clipboard copy (any element with class .js-copy-ref) ----------
  function handleCopyClick(event) {
    var btn = event.currentTarget;
    var ref = btn.getAttribute('data-ref');
    if (!ref) { return; }

    var notify = function () {
      var original = btn.textContent;
      btn.textContent = 'Copied: ' + ref;
      btn.disabled = true;
      setTimeout(function () {
        btn.textContent = original;
        btn.disabled = false;
      }, 1500);
    };

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(ref).then(notify).catch(notify);
    } else {
      // Fallback for older browsers (incl. non-HTTPS contexts)
      var tmp = document.createElement('textarea');
      tmp.value = ref;
      document.body.appendChild(tmp);
      tmp.select();
      try { document.execCommand('copy'); } catch (e) {}
      document.body.removeChild(tmp);
      notify();
    }
  }

  // ---- 2. Live character counter ---------------------------------------
  // Walks every .js-notes-counter and binds it to the nearest preceding textarea.
  function bindCounters() {
    var counters = document.querySelectorAll('.js-notes-counter');
    Array.prototype.forEach.call(counters, function (counter) {
      var textarea = counter.previousElementSibling;
      if (!textarea || textarea.tagName !== 'TEXTAREA') { return; }
      var max = parseInt(textarea.getAttribute('maxlength'), 10) || 280;

      function update() {
        var remaining = max - (textarea.value || '').length;
        counter.textContent = remaining + ' characters left';
        counter.style.color = remaining < 0 ? '#b3261e' : '';
      }
      textarea.addEventListener('input', update);
      update(); // initial state
    });
  }

  // ---- Boot -------------------------------------------------------------
  function init() {
    var copyButtons = document.querySelectorAll('.js-copy-ref');
    Array.prototype.forEach.call(copyButtons, function (btn) {
      btn.addEventListener('click', handleCopyClick);
    });
    bindCounters();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
