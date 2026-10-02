// ================================================================
// MUKURU MONEY COACH - shared API config + resilient fetch
//
// This is the ONLY copy of this file. Every page loads it from here:
//   frontend/Dashboard/index.html        -> ../shared/api-config.js
//   frontend/ai-chat/index.html          -> ../shared/api-config.js
//   frontend/Reports and polish/pages/*  -> ../../shared/api-config.js
//
// It used to be duplicated byte-for-byte in three directories, which meant
// every change had to be made three times and silently drifted. Keep the
// demo identity and endpoints declared once, here.
//
// Loaded as a plain <script>, so values are published on window rather
// than exported as a module.
// ================================================================
(function () {
    "use strict";

    var DEPLOYED_URL = "https://mukuru-jb1l.onrender.com";
    var LOCAL_URL = "http://127.0.0.1:8000";

    // The demo persona. Auth is mocked, so there is no real login to read an
    // identity from - these are the defaults. Override per-environment without
    // editing this file:
    //   window.__MUKURU_API__   -> API base URL
    //   window.__MUKURU_USER__  -> { id, name }
    //   localStorage keys        -> "mukuruApiBase", "mukuruUserId", "mukuruUserName"
    var DEFAULT_USER = { id: "grace", name: "Grace" };

    function trim(url) {
        return String(url).replace(/\/+$/, "");
    }

    function readStored(key) {
        try {
            // localStorage throws in some private-browsing modes.
            return localStorage.getItem(key) || "";
        } catch (e) {
            return "";
        }
    }

    function resolveApiBase() {
        if (window.__MUKURU_API__) {
            return trim(window.__MUKURU_API__);
        }

        var stored = readStored("mukuruApiBase");
        if (stored) {
            return trim(stored);
        }

        // The backend does NOT serve the frontend, so window.location.origin is
        // never the API. It used to be used here, which on GitHub Pages sent
        // every call to github.io and on file:// produced the string "null".
        var host = window.location.hostname;
        var isLocal = !host || host === "localhost" || host === "127.0.0.1";
        return isLocal ? LOCAL_URL : DEPLOYED_URL;
    }

    function resolveUser() {
        var user = window.__MUKURU_USER__ || {};
        var id = user.id || readStored("mukuruUserId") || DEFAULT_USER.id;
        var name = user.name || readStored("mukuruUserName") || DEFAULT_USER.name;
        return { id: id, name: name };
    }

    var user = resolveUser();

    window.MUKURU_API_BASE = resolveApiBase();
    window.MUKURU_USER = user;
    // Retained for existing call sites; prefer window.MUKURU_USER.
    window.MUKURU_USER_ID = user.id;
    window.MUKURU_USER_NAME = user.name;
    window.MUKURU_DEPLOYED_URL = DEPLOYED_URL;
    window.MUKURU_LOCAL_URL = LOCAL_URL;

    // Render's free tier sleeps when idle and takes 30-60s to wake, so the
    // first request of a session can outlast a default fetch. Give it time,
    // then retry once before reporting failure.
    //
    // The retry replays the request, so it must only be used for calls that
    // are safe to send twice. Mutating endpoints should call fetch directly:
    // an abort at the timeout does not prove the server never saw the
    // request, and /goals/{id}/add-funds is not idempotent.
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

    // A single-shot fetch with the same generous timeout but no retry, for
    // writes that must not be applied twice.
    window.mukuruFetchOnce = function (path, opts) {
        return timedFetch(window.MUKURU_API_BASE + path, opts, 45000);
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