/*
   event_registration/static/js/app.js
   ---------------------------------------------------------------------------

   The mandatory "at least one simple JavaScript interaction" for Option A.

   Live character counter: any textarea next to a .js-notes-counter
   updates the "NNN characters left" hint as the user types. Turns red
   when the limit is exceeded. Pure vanilla JS, no libraries.

   An earlier version of this file also implemented a clipboard copy
   button on the home page. The group removed that as over-extrapolated
   beyond the brief - one JS interaction is enough, and the counter is
   genuinely useful feedback to attendees filling in the notes field.
*/

(function () {
  'use strict';

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
      update();
    });
  }

  function init() {
    bindCounters();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
