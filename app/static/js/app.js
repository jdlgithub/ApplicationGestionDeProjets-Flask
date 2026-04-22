/**
 * Interface locale : menu responsive, fermeture des messages flash.
 */
(function () {
  "use strict";

  function initNavToggle() {
    document.querySelectorAll("[data-nav-toggle]").forEach(function (btn) {
      var id = btn.getAttribute("aria-controls");
      if (!id) return;
      var panel = document.getElementById(id);
      if (!panel) return;

      btn.addEventListener("click", function () {
        var open = panel.classList.toggle("site-header__nav--open");
        btn.setAttribute("aria-expanded", open ? "true" : "false");
      });
    });
  }

  function initFlashDismiss() {
    document.querySelectorAll("[data-flash-dismiss]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var box = btn.closest(".flash");
        if (box) {
          box.remove();
        }
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      initNavToggle();
      initFlashDismiss();
    });
  } else {
    initNavToggle();
    initFlashDismiss();
  }
})();
