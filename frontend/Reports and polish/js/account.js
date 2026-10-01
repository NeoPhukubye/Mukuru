// ================================================================
// MUKURU MONEY COACH
// My Account — live data
// ================================================================
//
// Figures are read from the FastAPI backend. This page previously rendered
// hardcoded values (score 682, income R8,500) that matched nothing.

(function () {
    "use strict";

    var API_BASE_URL = window.MUKURU_API_BASE;
    var USER_ID = window.MUKURU_USER_ID;
    var SYMBOL = "R";

    var el = function (id) { return document.getElementById(id); };

    function money(amount) {
        if (amount === null || amount === undefined || isNaN(amount)) {
            return "—";
        }
        return SYMBOL + Math.abs(amount).toLocaleString("en-ZA", {
            maximumFractionDigits: 0
        });
    }

    function setText(id, value) {
        var node = el(id);
        if (node) { node.textContent = value; }
    }

    function renderCredit(payload) {
        setText("creditScore", payload.score);

        var history = payload.history || [];
        if (history.length >= 2) {
            var previous = history[history.length - 2].score;
            var change = payload.score - previous;
            var sign = change >= 0 ? "+" : "";
            setText(
                "scoreChange",
                sign + change + " points this month · " + payload.band
            );
        } else {
            setText("scoreChange", payload.band);
        }
    }

    function renderGoal(goals) {
        if (!goals.length) {
            setText("goalName", "No savings goal yet");
            setText("goalAmount", "Create one from the dashboard");
            var bar = el("goalProgress");
            if (bar) { bar.style.width = "0%"; }
            return;
        }

        // Largest target wins, so the card shows the most meaningful goal.
        var goal = goals.slice().sort(function (a, b) {
            return (b.target_amount || 0) - (a.target_amount || 0);
        })[0];

        var pct = goal.target_amount > 0
            ? Math.min(100, Math.round((goal.saved_amount / goal.target_amount) * 100))
            : 0;

        setText("goalName", goal.name);
        setText(
            "goalAmount",
            money(goal.saved_amount) + " saved of " + money(goal.target_amount) +
            " (" + pct + "%)"
        );

        var bar = el("goalProgress");
        if (bar) { bar.style.width = pct + "%"; }
    }

    function renderOverview(budget) {
        setText("monthlyIncome", money(budget.total_income));

        var remittance = Math.abs((budget.totals_by_category || {}).remittance || 0);
        setText("sentHome", money(remittance));

        // Personal expenses exclude remittances, which are shown separately.
        var personal = Object.entries(budget.totals_by_category || {})
            .filter(function (entry) { return entry[0] !== "remittance" && entry[1] < 0; })
            .reduce(function (sum, entry) { return sum + Math.abs(entry[1]); }, 0);
        setText("personalExpenses", money(personal));

        setText("moneySaved", money(budget.surplus_deficit));

        setText("accountSubtitle", "Your money overview for " + budget.month + ".");
    }

    function load() {
        Promise.all([
            fetch(API_BASE_URL + "/analyze-budget?user_id=" + encodeURIComponent(USER_ID))
                .then(function (r) { return r.ok ? r.json() : null; }),
            fetch(API_BASE_URL + "/goals?user_id=" + encodeURIComponent(USER_ID))
                .then(function (r) { return r.ok ? r.json() : []; }),
            fetch(API_BASE_URL + "/calculate-credit-score?user_id=" + encodeURIComponent(USER_ID))
                .then(function (r) { return r.ok ? r.json() : null; })
        ]).then(function (results) {
            var budget = results[0];
            var goals = results[1] || [];
            var credit = results[2];

            if (budget) { renderOverview(budget); }
            else { setText("accountSubtitle", "Could not reach the Money Coach service."); }

            renderGoal(Array.isArray(goals) ? goals : []);

            if (credit) { renderCredit(credit); }
            else { setText("scoreChange", "Score unavailable right now."); }
        }).catch(function (error) {
            console.warn("Account data unavailable:", error);
            setText("accountSubtitle", "Could not reach the Money Coach service.");
            setText("scoreChange", "Score unavailable right now.");
        });
    }

    var reportButton = el("reportButton");
    if (reportButton) {
        reportButton.addEventListener("click", function () {
            window.location.href = "financial-report.html";
        });
    }

    load();
})();