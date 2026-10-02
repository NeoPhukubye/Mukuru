// ================================================================
// MUKURU MONEY COACH - shared API config + resilient fetch
//
// The same file is used in:
//   frontend/Dashboard/api-config.js
//   frontend/ai-chat/api-config.js
//   frontend/Reports and polish/js/api-config.js
//
// Loaded as a plain <script>, so values are published on window rather
// than exported as a module.
// ================================================================
(function () {
    "use strict";

    var DEPLOYED_URL = "https://mukuru-jb1l.onrender.com";
    var LOCAL_URL = "http://127.0.0.1:8000";

    function trim(url) {
        return String(url).replace(/\/+$/, "");
    }

    function resolveApiBase() {
        if (window.__MUKURU_API__) {
            return trim(window.__MUKURU_API__);
        }

        try {
            var stored = localStorage.getItem("mukuruApiBase");
            if (stored) {
                return trim(stored);
            }
        } catch (e) {
            // localStorage throws in some private-browsing modes.
        }

        // The backend does NOT serve the frontend, so window.location.origin is
        // never the API. It used to be used here, which on GitHub Pages sent
        // every call to github.io and on file:// produced the string "null".
        var host = window.location.hostname;
        var isLocal = !host || host === "localhost" || host === "127.0.0.1";
        return isLocal ? LOCAL_URL : DEPLOYED_URL;
    }

    window.MUKURU_API_BASE = resolveApiBase();
    window.MUKURU_USER_ID = "grace";
    window.MUKURU_DEPLOYED_URL = DEPLOYED_URL;
    window.MUKURU_LOCAL_URL = LOCAL_URL;

    // Render's free tier sleeps when idle and takes 30-60s to wake, so the
    // first request of a session can outlast a default fetch. Give it time,
    // then retry once before reporting failure.
    function timedFetch(url, opts, ms) {
        var controller = new AbortController();
        var timer = setTimeout(function () { controller.abort(); }, ms);
        var options = Object.assign({}, opts || {}, { signal: controller.signal });
        return fetch(url, options).finally(function () { clearTimeout(timer); });
    }

    window.mukuruFetch = function (path, opts) {
        var url = window.MUKURU_API_BASE + path;
        return timedFetch(url, opts, 45000).catch(function () {
            return timedFetch(url, opts, 45000);
        });
    };

    // Fire-and-forget: starts waking the server as soon as any page loads.
    try {
        window.mukuruFetch("/health").catch(function () {});
    } catch (e) {
        // Never let the warm-up break the page.
    }

    // Escape text before inserting it into innerHTML. Goal names and category
    // labels are user-supplied and were previously injected raw.
    window.mukuruEsc = function (value) {
        return String(value == null ? "" : value).replace(/[&<>"']/g, function (ch) {
            return {
                "&": "&amp;",
                "<": "&lt;",
                ">": "&gt;",
                '"': "&quot;",
                "'": "&#39;"
            }[ch];
        });
    };
})();
