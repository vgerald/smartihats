/* SmartiHats shared UI: theme persistence, mobile nav, trap switch, forms,
   interactive demos. Progressive enhancement — every interactive element
   has a static fallback so content is readable without JS. */
(function () {
  "use strict";

  /* ---- theme (persisted, respects OS preference by default) ---- */
  function currentTheme() {
    return document.documentElement.getAttribute("data-theme")
      || (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  }
  function applyTheme(t) {
    document.documentElement.setAttribute("data-theme", t);
    try { localStorage.setItem("smartihats-theme", t); } catch (e) { /* ignore */ }
    var btn = document.getElementById("themeToggle");
    if (btn) btn.textContent = (t === "dark" ? "☀" : "🌙");
  }

  /* ---- mobile nav ---- */
  function wireNav() {
    var burger = document.querySelector(".nav-burger");
    var nav = document.querySelector(".site-nav");
    if (!burger || !nav) return;
    burger.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (e) {
      if (e.target && e.target.closest && e.target.closest("a")) {
        nav.classList.remove("open");
        burger.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ---- generic aria-pressed switches (trap, before/after) ---- */
  function wireSwitches() {
    document.querySelectorAll("[data-switch-target]").forEach(function (sw) {
      if (sw.dataset.wired) return;
      sw.dataset.wired = "1";
      var target = document.getElementById(sw.getAttribute("data-switch-target"));
      if (!target) return;
      var other = target.querySelector("[data-switch-peer]") || null;
      sw.addEventListener("click", function () {
        var pressed = sw.getAttribute("aria-pressed") === "true";
        var next = !pressed;
        sw.setAttribute("aria-pressed", next ? "true" : "false");
        target.classList.toggle("show-on", next);
        target.classList.toggle("show-off", !next);
        target.setAttribute("aria-hidden", next ? "true" : "false");
        if (other) {
          other.classList.toggle("show-on", !next);
          other.setAttribute("aria-hidden", !next ? "true" : "false");
        }
        if (sw.getAttribute("data-label-on")) {
          var lbl = document.getElementById(sw.getAttribute("data-label-on"));
          if (lbl) lbl.textContent = (next ? sw.dataset.labelOnTxt : sw.dataset.labelOffTxt) || "";
        }
      });
    });
  }

  /* ---- forms: basic client-side success handling + validation feedback ---- */
  function wireForms() {
    document.querySelectorAll("form[data-client-validate]").forEach(function (form) {
      if (form.dataset.wired) return;
      form.dataset.wired = "1";
      form.addEventListener("submit", function (e) {
        var required = form.querySelectorAll("[required]");
        var firstBad = null;
        required.forEach(function (el) {
          var valid = true;
          if (!el.value.trim()) valid = false;
          if (el.type === "email") {
            var v = el.value.trim().toLowerCase();
            if (!v || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) valid = false;
          }
          el.setAttribute("aria-invalid", valid ? "false" : "true");
          el.classList.toggle("invalid", !valid);
          if (!valid && !firstBad) firstBad = el;
        });
        if (firstBad) {
          e.preventDefault();
          var msg = document.getElementById(form.id + "-error");
          if (msg) { msg.hidden = false; }
          firstBad.focus();
          return;
        }
        var ok = document.getElementById(form.id + "-ok");
        if (ok) { ok.hidden = false; }
        // Let it POST if it's a real form (formspree) - we don't block.
      });
    });
  }

  /* ---- demo: mock HA dashboard state machine ---- */
  function wireDash() {
    var dash = document.getElementById("mockDash");
    if (!dash) return;
    var lights = {
      kitchen: { el: dash.querySelector("#tileKitchen"), state: false },
      porch: { el: dash.querySelector("#tilePorch"), state: false },
      bedroom: { el: dash.querySelector("#tileBedroom"), state: false },
      office: { el: dash.querySelector("#tileOffice"), state: false }
    };
    Object.keys(lights).forEach(function (k) {
      var tile = lights[k].el;
      var btn = tile ? tile.querySelector(".tile-toggle") : null;
      if (btn) btn.addEventListener("click", function () {
        lights[k].state = !lights[k].state;
        tile.classList.toggle("on", lights[k].state);
        btn.setAttribute("aria-pressed", lights[k].state ? "true" : "false");
        var lbl = tile.querySelector(".tile-val");
        if (lbl) lbl.textContent = (lights[k].state ? "On" : "Off");
      });
    });
    var thermo = dash.querySelector("#thermSlider");
    if (thermo) {
      var tval = dash.querySelector("#thermVal");
      var mode = dash.querySelector("#thermMode");
      thermo.addEventListener("input", function () {
        if (tval) tval.textContent = thermo.value + "°";
        if (mode) {
          var v = parseFloat(thermo.value);
          mode.textContent = v < 68 ? "Heating" : (v > 74 ? "Cooling" : "Idle");
        }
      });
    }
    var sceneBtns = dash.querySelectorAll(".scene-btn");
    var banner = dash.querySelector("#sceneBanner");
    var cam = dash.querySelector("#camScene");
    var camLabel = dash.querySelector("#camState");
    sceneBtns.forEach(function (b) {
      b.addEventListener("click", function () {
        sceneBtns.forEach(function (x) {
          x.classList.remove("active");
          x.setAttribute("aria-pressed", "false");
        });
        b.classList.add("active");
        b.setAttribute("aria-pressed", "true");
        var preset = b.getAttribute("data-preset");
        // lights
        var states = presets[preset] || { kitchen: true, porch: true, bedroom: false, office: true, lightK: true, lightP: true };
        Object.keys(lights).forEach(function (k) {
          var want = !!states[k];
          if (lights[k].el) {
            lights[k].state = want;
            lights[k].el.classList.toggle("on", want);
            var btn = lights[k].el.querySelector(".tile-toggle");
            if (btn) btn.setAttribute("aria-pressed", want ? "true" : "false");
            var lbl = lights[k].el.querySelector(".tile-val");
            if (lbl) lbl.textContent = (want ? "On" : "Off");
          }
        });
        if (banner) {
          banner.textContent = "Scene applied: " + b.textContent;
          banner.classList.add("show");
        }
        if (cam) {
          cam.style.background = (camGrads[preset] || camGrads.movie);
        }
        if (camLabel) camLabel.textContent = "Active · " + b.textContent;
      });
    });
  }
  var presets = {
    "movie": { kitchen: false, porch: true, bedroom: false, office: true },
    "away": { kitchen: false, porch: true, bedroom: false, office: false },
    "goodnight": { kitchen: false, porch: false, bedroom: false, office: false },
    "morning": { kitchen: true, porch: false, bedroom: true, office: false }
  };
  var camGrads = {
    "movie": "linear-gradient(135deg,#18222f,#10161f)",
    "away": "linear-gradient(135deg,#22303f,#101820)",
    "goodnight": "linear-gradient(135deg,#1a1522,#0c1018)",
    "morning": "linear-gradient(135deg,#223142,#0c131d)"
  };

  /* ---- demo: FaceID mock ---- */
  function wireFid() {
    var wrap = document.getElementById("fidWrap");
    if (!wrap) return;
    var btn = wrap.querySelector("#fidScan");
    var box = wrap.querySelector(".fid-box");
    var tag = wrap.querySelector(".fid-tag");
    var chips = wrap.querySelectorAll(".fid-person-chip");
    btn.addEventListener("click", function () {
      var known = chips[Math.floor(Math.random() * Math.min(2, chips.length))];
      var stranger = chips[chips.length - 1];
      var target = Math.random() < 0.7 ? known : stranger;
      chips.forEach(function (c) { c.classList.remove("match"); });
      if (box) box.classList.remove("show");
      if (tag) { tag.classList.remove("show"); }
      setTimeout(function () {
        if (box) box.classList.add("show");
        if (tag) {
          tag.textContent = (target === stranger ? "Unknown face" : "Match: " + target.querySelector(".fid-name").textContent);
          tag.classList.add("show");
        }
        target.classList.add("match");
      }, 550);
    });
  }

  /* ---- interactive demo pages (scene / security / voice / daily) ---- */
  function wireDemos() {
    /* --- scene demos — toggle the room state via data-scene --- */
    var stage = document.getElementById("sceneStage");
    if (stage) {
      var status = document.getElementById("sceneStatus");
      var therm = document.getElementById("thermVal");
      var btns = document.querySelectorAll("[data-scene-btn]");
      var copy = {
        "movie-night": { s: "Movie Night active — lights dim to ~10%, doors locked, hold at 68°", t: "68" },
        "away":        { s: "Away active — non-security lights off, doors secured, cameras armed", t: "65" },
        "good-morning":{ s: "Good Morning active — lights warming up, comfort temp, door still locked", t: "70" },
        "off":         { s: "No scene active", t: "70" }
      };
      function setScene(n) {
        stage.setAttribute("data-scene", n);
        btns.forEach(function (b) {
          b.classList.toggle("active", b.getAttribute("data-scene-btn") === n && n !== "off");
        });
        var c = copy[n] || copy["off"];
        if (status) status.textContent = c.s;
        if (therm) therm.textContent = c.t;
      }
      btns.forEach(function (b) {
        b.addEventListener("click", function () { setScene(b.getAttribute("data-scene-btn")); });
      });
    }

    /* --- smart security walkthrough — replay the timeline --- */
    var replay = document.getElementById("replaySec");
    var tl = document.getElementById("secTimeline");
    if (replay && tl) {
      replay.addEventListener("click", function () {
        var items = tl.querySelectorAll(".tl-item");
        items.forEach(function (i) { i.classList.remove("active"); i.classList.add("pending"); });
        items.forEach(function (i, idx) {
          setTimeout(function () {
            i.classList.remove("pending");
            i.classList.add("active");
          }, 250 + idx * 850);
        });
      });
    }

    /* --- voice assistant clone — command → response feed --- */
    var vaInput = document.getElementById("vaInput");
    var vaSend = document.getElementById("vaSend");
    var vaFeed = document.getElementById("vaFeed");
    if (vaInput && vaSend && vaFeed) {
      var answers = {
        "movie-night": { tag: "Scene", body: ["Turning lights down to ~10%", "Doors: locked", "Thermostat: hold at 68°", "Movie Night is active."] },
        "away":        { tag: "Scene", body: ["Lights: off (bath + hallway excepted)", "Doors: locked", "Cameras: armed", "Thermostat: 65° for the day", "Away is active."] },
        "good-morning":{ tag: "Scene", body: ["Lights: warming up to 100% over 3 min", "Thermostat: 70°", "Door: still locked until you unlock", "Good Morning is active."] },
        "lights-off":  { tag: "Lights", body: ["Kitchen: off", "Porch: off", "Bedroom: off", "All non-security lights are off."] },
        "lock-all":    { tag: "Security", body: ["Front door: locked", "Back door: locked", "Garage: secured", "All doors are locked."] },
        "temp-72":     { tag: "Thermostat", body: ["Set to 72°", "Mode: heating", "You&rsquo;re all set."] }
      };
      function normalize(s) {
        s = s.toLowerCase();
        if (s.indexOf("movie") >= 0) return "movie-night";
        if (s.indexOf("away") >= 0 || s.indexOf("leave") >= 0) return "away";
        if (s.indexOf("morning") >= 0 || s.indexOf("wake") >= 0) return "good-morning";
        if (s.indexOf("lock") >= 0) return "lock-all";
        if (/72|temperature|thermostat/.test(s)) return "temp-72";
        if (s.indexOf("light") >= 0 && (s.indexOf("off") >= 0)) return "lights-off";
        return null;
      }
      function respond(cmd) {
        var key = (answers[cmd] ? cmd : normalize(cmd)) ;
        if (!key) {
          vaFeed.innerHTML = '<p class="va-empty">I didn&rsquo;t catch that. Try one of the suggestions above, or type &ldquo;movie night&rdquo; / &ldquo;lock every door&rdquo;.</p>';
          return;
        }
        var a = answers[key];
        var li = a.body.map(function (x) { return "<li>" + x + "</li>"; }).join("");
        vaFeed.innerHTML = '<div class="vo"><span class="vo-tag">' + a.tag + ' · done</span><ul>' + li + "</ul></div>";
      }
      vaSend.addEventListener("click", function () {
        respond(vaInput.value.trim());
        vaInput.value = "";
      });
      vaInput.addEventListener("keydown", function (e) {
        if (e.key === "Enter") { e.preventDefault(); respond(vaInput.value.trim()); vaInput.value = ""; }
      });
      document.querySelectorAll(".chip-btn[data-cmd]").forEach(function (c) {
        c.addEventListener("click", function () { respond(c.getAttribute("data-cmd")); });
      });
    }

    /* --- daily automation — play the day loop --- */
    var stages = document.getElementById("dayStages");
    var play = document.getElementById("playDay"), pause = document.getElementById("pauseDay"), reset = document.getElementById("resetDay");
    var status = document.getElementById("dayStatus");
    if (stages && play) {
      var cards = stages.querySelectorAll(".day-card");
      var idx = 0, timer = null;
      function paint() {
        cards.forEach(function (c, i) { c.classList.toggle("active", i === idx); });
      }
      function tick() { idx = (idx + 1) % cards.length; paint(); if (status) status.textContent = "Playing · " + cards[idx].querySelector(".day-time").textContent; }
      function setPlaying(on) {
        if (on) {
          timer = setInterval(tick, 1300);
          if (status) status.textContent = "Playing · " + cards[idx].querySelector(".day-time").textContent;
        } else {
          if (timer) { clearInterval(timer); timer = null; }
          if (status) status.textContent = "Paused";
        }
      }
      function resetDay() {
        setPlaying(false); idx = 0; paint();
        if (status) status.textContent = "Paused";
      }
      play.addEventListener("click", function () { if (!timer) setPlaying(true); });
      if (pause) pause.addEventListener("click", function () { setPlaying(false); });
      if (reset) reset.addEventListener("click", resetDay);
    }
  }

  function init() {
    // theme init (early, from a small inline script) + toggle button
    var btn = document.getElementById("themeToggle");
    if (btn && !btn.dataset.wired) {
      btn.dataset.wired = "1";
      btn.addEventListener("click", function () {
        applyTheme(currentTheme() === "dark" ? "light" : "dark");
      });
    }
    wireNav();
    wireSwitches();
    wireForms();
    wireDash();
    wireFid();
    wireDemos();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
