(function () {
  var input = document.getElementById("productSearch");
  var grid = document.getElementById("productGrid");
  var noResults = document.getElementById("noResults");
  var resultCount = document.getElementById("resultCount");
  var chipRow = document.getElementById("categoryChips");
  if (!input || !grid) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll(".product-card"));
  var activeCategory = "All";

  function params() {
    return new URLSearchParams(window.location.search);
  }

  function matches(card, words) {
    var haystack = card.getAttribute("data-search") || "";
    return words.every(function (w) {
      return haystack.indexOf(w) !== -1;
    });
  }

  function applyFilters() {
    var query = input.value.trim().toLowerCase();
    var words = query.length ? query.split(/\s+/) : [];
    var visible = 0;

    cards.forEach(function (card) {
      var categoryOk = activeCategory === "All" || card.getAttribute("data-category") === activeCategory;
      var searchOk = words.length === 0 || matches(card, words);
      var show = categoryOk && searchOk;
      card.style.display = show ? "" : "none";
      if (show) visible++;
    });

    noResults.classList.toggle("show", visible === 0);
    resultCount.textContent = visible + (visible === 1 ? " medicine found" : " medicines found");
  }

  if (chipRow) {
    chipRow.addEventListener("click", function (e) {
      var chip = e.target.closest(".chip");
      if (!chip) return;
      chipRow.querySelectorAll(".chip").forEach(function (c) {
        c.classList.remove("active");
      });
      chip.classList.add("active");
      activeCategory = chip.getAttribute("data-category");
      applyFilters();
    });
  }

  input.addEventListener("input", applyFilters);

  // Pre-fill from ?q= and ?category= on load (header search / footer category links)
  var p = params();
  var initialQuery = p.get("q");
  var initialCategory = p.get("category");
  if (initialQuery) input.value = initialQuery;
  if (initialCategory && chipRow) {
    var target = chipRow.querySelector('[data-category="' + CSS.escape(initialCategory) + '"]');
    if (target) {
      chipRow.querySelectorAll(".chip").forEach(function (c) { c.classList.remove("active"); });
      target.classList.add("active");
      activeCategory = initialCategory;
    }
  }
  applyFilters();
})();
