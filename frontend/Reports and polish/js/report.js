// ================================================================
// MUKURU MONEY COACH
// Financial Report — live data and real PDF download
// ================================================================
//
// This page previously rendered a hardcoded report (score 682, income
// R8,500) and the download button produced a hand-written text blob that
// contained no real data. Both now come from the backend.

(function () {
    "use strict";

    var API_BASE_URL = window.MUKURU_API_BASE;
    var USER_ID = window.MUKURU_USER_ID;
    var SYMBOL = "R";
    var SCORE_MIN = 300;
    var SCORE_MAX = 850;

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

    function shortDate(iso) {
        var d = new Date(iso);
        if (isNaN(d)) { return iso; }
        return d.toLocaleDateString("en-ZA", {
            day: "2-digit", month: "short", year: "numeric"
        });
    }

    function renderCredit(payload) {
        setText("creditScore", payload.score);

        var history = payload.history || [];
        var fill = el("creditProgressFill");
        if (fill) {
            var pct = ((payload.score - SCORE_MIN) / (SCORE_MAX - SCORE_MIN)) * 100;
            fill.style.width = Math.max(0, Math.min(100, pct)) + "%";
        }

        if (history.length >= 2) {
            var previous = history[history.length - 2];
            var change = payload.score - previous.score;
            setText("creditPrevious", previous.score + " last month");
            setText("creditCurrent", payload.score + " this month");
            setText(
                "scoreChange",
                (change >= 0 ? "+" : "") + change + " points this month · " + payload.band
            );
        } else {
            setText("creditPrevious", "— last month");
            setText("creditCurrent", payload.score + " now");
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

    function renderRemittances(items) {
        var container = el("remittanceList");
        if (!container) { return; }

        container.innerHTML = "";

        if (!items.length) {
            container.innerHTML = '<p class="report-note">No remittances recorded yet.</p>';
            return;
        }

        items.slice(0, 5).forEach(function (tx) {
            var row = document.createElement("div");
            row.className = "remittance-row";

            var left = document.createElement("div");

            var date = document.createElement("strong");
            date.textContent = shortDate(tx.date);

            var note = document.createElement("p");
            note.textContent = (tx.recipient_country
                ? "To " + tx.recipient_country
                : "Family support");

            left.appendChild(date);
            left.appendChild(note);

            var amount = document.createElement("strong");
            amount.textContent = money(tx.amount);

            row.appendChild(left);
            row.appendChild(amount);
            container.appendChild(row);
        });
    }

    function renderReport(report) {
        // Only the period context comes from the report. The headline figures
        // stay scoped to the current month via /analyze-budget, so this must
        // not overwrite them.
        setText(
            "reportSubtitle",
            "Money overview for the current month · report covers the last " +
            report.period_months + " months"
        );
    }

    function renderOverview(budget) {
        var remittance = Math.abs((budget.totals_by_category || {}).remittance || 0);
        setText("monthlyIncome", money(budget.total_income));
        setText("monthlyRemittances", money(remittance));
        setText("monthlyExpenses", money(budget.total_expenses - remittance));
        setText("moneySaved", money(budget.surplus_deficit));
        setText("reportSubtitle", "Your money overview for " + budget.month + ".");
    }

    function load() {
        Promise.all([
            fetch(API_BASE_URL + "/analyze-budget?user_id=" + encodeURIComponent(USER_ID))
                .then(function (r) { return r.ok ? r.json() : null; }),
            fetch(API_BASE_URL + "/goals?user_id=" + encodeURIComponent(USER_ID))
                .then(function (r) { return r.ok ? r.json() : []; }),
            fetch(API_BASE_URL + "/calculate-credit-score?user_id=" + encodeURIComponent(USER_ID))
                .then(function (r) { return r.ok ? r.json() : null; }),
            fetch(API_BASE_URL + "/transactions?user_id=" + encodeURIComponent(USER_ID))
                .then(function (r) { return r.ok ? r.json() : { items: [] }; }),
            fetch(API_BASE_URL + "/generate-financial-report?user_id=" + encodeURIComponent(USER_ID))
                .then(function (r) { return r.ok ? r.json() : null; })
        ]).then(function (results) {
            var budget = results[0];
            var goals = results[1] || [];
            var credit = results[2];
            var transactions = results[3] || { items: [] };
            var report = results[4];

            if (budget) { renderOverview(budget); }
            if (report) { renderReport(report); }
            else if (!budget) { setText("reportSubtitle", "Could not reach the Money Coach service."); }

            renderGoal(Array.isArray(goals) ? goals : []);
            if (credit) { renderCredit(credit); }
            else { setText("scoreChange", "Score unavailable right now."); }

            var remittances = (transactions.items || []).filter(function (tx) {
                return tx.is_remittance;
            }).slice().reverse();

            renderRemittances(remittances);
        }).catch(function (error) {
            console.warn("Report data unavailable:", error);
            setText("reportSubtitle", "Could not reach the Money Coach service.");
            setText("scoreChange", "Score unavailable right now.");
        });
    }

    // Download the real PDF the backend renders, instead of a text blob.
    var downloadButton = el("downloadButton");
    if (downloadButton) {
        downloadButton.addEventListener("click", function () {
            var url = API_BASE_URL + "/generate-financial-report/pdf?user_id=" +
                encodeURIComponent(USER_ID);

            downloadButton.disabled = true;
            setText("downloadNote", "Preparing your report…");

            fetch(url)
                .then(function (response) {
                    if (!response.ok) { throw new Error("HTTP " + response.status); }
                    return response.blob();
                })
                .then(function (blob) {
                    var href = URL.createObjectURL(blob);
                    var link = document.createElement("a");
                    link.href = href;
                    link.download = "Mukuru-Financial-Health-Report.pdf";
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    URL.revokeObjectURL(href);
                    setText("downloadNote", "Downloaded. This document is for information only.");
                })
                .catch(function (error) {
                    console.warn("PDF download failed:", error);
                    setText("downloadNote", "Could not build the PDF. Please try again.");
                })
                .finally(function () {
                    downloadButton.disabled = false;
                });
        });
    }

    load();
})();