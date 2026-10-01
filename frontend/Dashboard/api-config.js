// ================================================================
// MUKURU MONEY COACH
// API configuration
// ================================================================
//
// Loaded before script.js as a plain <script>, so values are published on
// window rather than exported as a module.
//
// Resolution order, most specific first:
//   1. window.__MUKURU_API__  — injected, for deployments
//   2. localStorage           — developer override, survives reloads
//   3. same-origin            — works when the API serves the frontend
//   4. DEPLOYED_URL           — fallback for the static Pages build
//
// This used to be hardcoded to http://127.0.0.1:8000, so the deployed site
// could never reach the live API.

(function () {
    "use strict";

    var DEPLOYED_URL = "https://mukuru-jb1l.onrender.com";

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
            // localStorage can throw in private browsing; fall through.
        }

        if (window.location && window.location.origin) {
            return window.location.origin;
        }

        return DEPLOYED_URL;
    }

    window.MUKURU_API_BASE = resolveApiBase();
    window.MUKURU_USER_ID = "grace";
    window.MUKURU_DEPLOYED_URL = DEPLOYED_URL;
})();