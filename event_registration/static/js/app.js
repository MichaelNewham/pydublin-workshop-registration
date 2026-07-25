/*
   event_registration/static/js/app.js
   ---------------------------------------------------------------------------

   The mandatory "at least one simple JavaScript interaction" for Option A.

   Live character counter: any textarea next to a .js-notes-counter
   updates the "NNN characters left" hint as the user types. Turns red
   when the user has 20 or fewer characters left, so the interaction
   is visible on screen (the maxlength attribute hard-blocks typing
   past 280, so the older "remaining < 0" check was unreachable).
   Pure vanilla JS, no libraries.

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
      counter.setAttribute('aria-live', 'polite');
      counter.setAttribute('aria-atomic', 'true');
      var max = parseInt(textarea.getAttribute('maxlength'), 10) || 280;

      function update() {
        var remaining = max - (textarea.value || '').length;
        counter.textContent = remaining + ' characters left';
        // Turn red when the user is close to the limit, so the
        // interaction is visible on screen (not just at <0, which
        // never happens because maxlength=280 hard-blocks typing).
        counter.style.color = remaining <= 20 ? '#b3261e' : '';
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
