// zsmr.eu (from maltezskyrad.cz) — progressive enhancement only; every page works without this file.
(function () {
  // ---- the menu bar stays at the top once the page scrolls past it (see .site-header.sticky in site.css)
  var header = document.querySelector(".site-header"), bar = header && header.querySelector(".mainnav");
  if (header && bar) {
    var pin = function () {
      var toggle = bar.querySelector(".menu-toggle");
      header.style.setProperty("--stick", bar.offsetTop + "px");
      document.documentElement.style.setProperty("--nav-h", ((toggle && toggle.offsetHeight) || bar.offsetHeight) + "px");
    };
    pin();
    header.classList.add("sticky");
    document.documentElement.classList.add("has-sticky");
    window.addEventListener("resize", pin);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(pin);
  }

  // ---- main menu (mobile) and submenus
  var toggle = document.querySelector(".menu-toggle");
  var menu = document.getElementById("menu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") !== "true";
      toggle.setAttribute("aria-expanded", String(open));
      menu.classList.toggle("open", open);
    });
  }
  document.querySelectorAll(".sub-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var li = btn.parentElement;
      var open = !li.classList.contains("open");
      li.classList.remove("closed");
      li.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", String(open));
    });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    document.querySelectorAll(".has-sub:hover").forEach(function (li) { li.classList.add("closed"); });  // hover-opened dropdown (WCAG 1.4.13)
    if (menu && menu.classList.contains("open")) { menu.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); toggle.focus(); }
    document.querySelectorAll(".has-sub.open").forEach(function (li) {
      li.classList.remove("open");
      var b = li.querySelector(".sub-toggle");
      if (b) b.setAttribute("aria-expanded", "false");
    });
    var li = document.activeElement && document.activeElement.closest(".has-sub");
    if (li) {
      if (document.activeElement.closest(".sub")) {
        var top = li.querySelector("a");
        if (top) top.focus();
      }
      li.classList.add("closed");  // focus stays on the item, so :focus-within would keep the submenu open; .closed holds it shut until focus leaves
    }
  });
  document.addEventListener("focusout", function (e) {
    var li = e.target.closest && e.target.closest(".has-sub.closed");
    if (li && !li.contains(e.relatedTarget)) li.classList.remove("closed");
  });
  document.addEventListener("pointerover", function (e) {  // the mouse re-opens it as usual
    var li = e.target.closest && e.target.closest(".has-sub.closed");
    if (li && !li.contains(e.relatedTarget)) li.classList.remove("closed");  // only when the pointer comes back from outside
  });

  // ---- Schránka důvěry: send the form without leaving the page
  var tf = document.getElementById("trust-form");
  if (tf) tf.addEventListener("submit", function (e) {
    e.preventDefault();
    var msg = document.getElementById("tf-msg"), btn = tf.querySelector("button");
    var say = function (t, bad) { msg.hidden = false; msg.textContent = t; msg.className = "ne-msg" + (bad ? " ne-msg--error" : ""); };
    btn.disabled = true;
    fetch(tf.action, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(Object.fromEntries(new FormData(tf))) })
      .then(function (r) { return r.json().then(function (d) { return [r.status, d]; }); })
      .then(function (x) {
        if (x[0] === 200) { tf.reset(); say("Děkujeme, zpráva byla odeslána."); }
        else say({ email: "Zadejte prosím platný e-mail pro odpověď.", message: "Napište prosím zprávu.", rate: "Odeslali jste příliš mnoho zpráv, zkuste to prosím později." }[x[1].error]
          || "Zprávu se nepodařilo odeslat. Napište prosím na skola@zsmr.cz.", true);
      })
      .catch(function () { say("Zprávu se nepodařilo odeslat. Napište prosím na skola@zsmr.cz.", true); })
      .then(function () { btn.disabled = false; });
  });

  // ---- images still downloading develop out of the paper tone once they arrive (see .is-loading)
  document.querySelectorAll("img.ph-img").forEach(function (img) {
    if (img.complete || img.naturalWidth) return;  // already shown (or progressively painting): leave it alone
    img.classList.add("is-loading");
    var done = function () {
      if (img.getBoundingClientRect().top > innerHeight) {  // arrived off-screen (often from cache): appear without the fade
        img.style.transition = "none"; img.classList.remove("is-loading"); img.offsetWidth; img.style.transition = "";
      } else img.classList.remove("is-loading");
    };
    img.addEventListener("load", done, { once: true });
    img.addEventListener("error", done, { once: true });
  });

})();
