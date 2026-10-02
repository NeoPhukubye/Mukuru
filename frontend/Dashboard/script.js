// ================================================================
// MUKURU MONEY COACH
// Main Dashboard JavaScript
// ================================================================

// ================================================================
// API CONFIGURATION
// ================================================================
// Resolved by shared/api-config.js (window.MUKURU_API_BASE /
// window.MUKURU_USER), which picks the deployed API, a same-origin API, or
// a local override. The demo identity is declared there, not here.
const API_BASE_URL = window.MUKURU_API_BASE;
const USER_ID = window.MUKURU_USER_ID;

// ================================================================
// 1. TRANSLATIONS
// ================================================================

const translations = {

    // ------------------------------------------------------------
    // ENGLISH
    // ------------------------------------------------------------

    en: {
        tagline: "Simple money guidance for you",

        signIn: "Sign In / Log In",
        createAccount: "Sign Up / New Account",

        phoneNumber: "Phone Number or Mukuru ID",
        phoneNumberOnly: "Phone Number",

        currentCountry: "Current Location / Country",
        countryOfResidence: "Country of Residence",

        currency: "Display Currency",
        preferredCurrency: "Preferred Currency",

        pin: "PIN / Password",
        createPin: "Create Secret PIN",

        needHelp: "Need help?",
        forgotPin: "Forgot your PIN?",

        moneyCoach: "Money Coach",

        moneyCoachIntro:
            "Get simple help with saving, spending and reaching your goals.",

        welcome: "👋 Welcome",

        signOut: "Sign Out",

        monthlyOverview: "Monthly Money Overview",

        moneyManaged:
            "Money you managed this month",

        savingsGoals: "My Savings Goals",

        newGoal: "+ New Goal",

        goalName: "Goal Name",

        targetAmount: "Target Amount",

        saveGoal: "Save Goal",

        cancel: "Cancel",

        expenseBreakdown: "Where Your Money Goes",

        moneyTip: "💡 Money Tip",

        coachMessage:
            "Need help with your money? Ask for simple guidance.",

        askCoach: "Ask Money Coach",

        viewReports: "View My Reports",

        schoolFees: "Sister's School Fees",

        fridge: "Fridge Back Home",

        remittances: "Money Sent Home",

        groceries: "Groceries & Rent",

        airtime: "Airtime & Data"
    },


    // ------------------------------------------------------------
    // ISIZULU
    // ------------------------------------------------------------

    zu: {
        tagline: "Usizo olulula lokuphatha imali yakho",

        signIn: "Ngena Ngemvume",
        createAccount: "Bhalisa I-akhawunti Entsha",

        phoneNumber: "Inombolo Yocingo noma i-Mukuru ID",
        phoneNumberOnly: "Inombolo Yocingo",

        currentCountry: "Indawo Yamanje / Izwe",
        countryOfResidence: "Izwe Ohlala Kulo",

        currency: "Imali Ekhonjiswayo",
        preferredCurrency: "Imali Oyithandayo",

        pin: "I-PIN / Iphasiwedi",
        createPin: "Dala I-PIN Eyimfihlo",

        needHelp: "Udinga usizo?",
        forgotPin: "Ukhohlwe i-PIN yakho?",

        moneyCoach: "Umqeqeshi Wezimali",

        moneyCoachIntro:
            "Thola usizo olulula lokonga, ukusebenzisa imali nokufinyelela imigomo yakho.",

        welcome: "👋 Siyakwamukela",

        signOut: "Phuma",

        monthlyOverview: "Isifinyezo Semali Yenyanga",

        moneyManaged:
            "Imali oyiphethe kule nyanga",

        savingsGoals: "Imigomo Yami Yokonga",

        newGoal: "+ Umgomo Omusha",

        goalName: "Igama Lomgomo",

        targetAmount: "Inani Eliqondisiwe",

        saveGoal: "Gcina Umgomo",

        cancel: "Khansela",

        expenseBreakdown: "Lapho Imali Yakho Iya Khona",

        moneyTip: "💡 Ithiphu Yemali",

        coachMessage:
            "Udinga usizo ngemali yakho? Buza ukuze uthole usizo olulula.",

        askCoach: "Buza Umqeqeshi Wezimali",

        viewReports: "Buka Imibiko Yami",

        schoolFees: "Imali Yesikole Kadadewethu",

        fridge: "Isiqandisi Sasekhaya",

        remittances: "Imali Ethunyelwe Ekhaya",

        groceries: "Ukudla Ne-Renti",

        airtime: "I-Airtime Nedatha"
    },


    // ------------------------------------------------------------
    // SESOTHO
    // ------------------------------------------------------------

    st: {
        tagline: "Thuso e bonolo ya ho laola tjhelete ya hao",

        signIn: "Kena",
        createAccount: "Ngodisa Akhaonto e Ntjha",

        phoneNumber: "Nomoro ya Mohala kapa Mukuru ID",
        phoneNumberOnly: "Nomoro ya Mohala",

        currentCountry: "Sebaka sa Hona Jwale / Naha",
        countryOfResidence: "Naha eo o Phelang ho Yona",

        currency: "Mofuta wa Tjhelete",
        preferredCurrency: "Tjhelete eo o e Ratang",

        pin: "PIN / Phasewete",
        createPin: "Theha PIN ya Lekunutu",

        needHelp: "O hloka thuso?",
        forgotPin: "O lebetse PIN ya hao?",

        moneyCoach: "Mokoetlisi wa Ditjhelete",

        moneyCoachIntro:
            "Fumana thuso e bonolo ya ho boloka tjhelete le ho fihlela dipheo tsa hao.",

        welcome: "👋 Rea o amohela",

        signOut: "Tswa",

        monthlyOverview: "Kakaretso ya Tjhelete ya Kgwedi",

        moneyManaged: "Tjhelete eo o e laotseng kgweding ena",

        savingsGoals: "Dipheo tsa Ka tsa Poloko",

        newGoal: "+ Sepheo se Setjha",

        goalName: "Lebitso la Sepheo",

        targetAmount: "Chelete e Lebeletsweng",

        saveGoal: "Boloka Sepheo",

        cancel: "Hlakola",

        expenseBreakdown: "Moo Tjhelete ya Hao e Yang",

        moneyTip: "💡 Keletso ya Tjhelete",

        coachMessage:
            "O hloka thuso ka tjhelete ya hao? Botsa Mokoetlisi wa Ditjhelete.",

        askCoach: "Botsa Mokoetlisi",

        viewReports: "Sheba Ditlaleho Tsa Ka",

        schoolFees: "Tjhelete ya Sekolo sa Kgaitsedi",

        fridge: "Sehatsetsi Lapeng",

        remittances: "Tjhelete e Rometsweng Lapeng",

        groceries: "Dijo le Rente",

        airtime: "Airtime le Data"
    },


    // ------------------------------------------------------------
    // CHISHONA
    // ------------------------------------------------------------

    sn: {
        tagline: "Rubatsiro rwakareruka pakushandisa mari yako",

        signIn: "Pinda",
        createAccount: "Nyoresa Akaundi Itsva",

        phoneNumber: "Nhamba yeFoni kana Mukuru ID",
        phoneNumberOnly: "Nhamba yeFoni",

        currentCountry: "Nzvimbo Yazvino / Nyika",
        countryOfResidence: "Nyika yaunogara",

        currency: "Mari Inoratidzwa",
        preferredCurrency: "Mari yaunoda",

        pin: "PIN / Password",
        createPin: "Gadzira PIN Yakavanzika",

        needHelp: "Unoda rubatsiro?",
        forgotPin: "Wakanganwa PIN yako?",

        moneyCoach: "Mudzidzisi Wemari",

        moneyCoachIntro:
            "Wana rubatsiro rwakareruka pakuchengetedza mari nekuzadzisa zvinangwa zvako.",

        welcome: "👋 Tinokugamuchirai",

        signOut: "Buda",

        monthlyOverview: "Pfupiso yeMari yeMwedzi",

        moneyManaged:
            "Mari yawakabata mumwedzi uno",

        savingsGoals: "Zvinangwa Zvangu Zvekuchengetedza Mari",

        newGoal: "+ Chinangwa Chitsva",

        goalName: "Zita reChinangwa",

        targetAmount: "Mari Yakanangwa",

        saveGoal: "Chengetedza Chinangwa",

        cancel: "Kanzura",

        expenseBreakdown: "Mari Yako Iri Kuenda Kupi",

        moneyTip: "💡 Zano reMari",

        coachMessage:
            "Unoda rubatsiro nemari yako? Bvunza Mudzidzisi Wemari.",

        askCoach: "Bvunza Mudzidzisi Wemari",

        viewReports: "Ona Mishumo Yangu",

        schoolFees: "Mari yeChikoro cheSisi",

        fridge: "Firiji Kumba",

        remittances: "Mari Yakatumirwa Kumba",

        groceries: "Zvokudya neRendi",

        airtime: "Airtime neData"
    },


    // ------------------------------------------------------------
    // CHICHEWA
    // ------------------------------------------------------------

    ny: {
        tagline: "Thandizo losavuta loyendetsera ndalama zanu",

        signIn: "Lowani",
        createAccount: "Pangani Akaunti Yatsopano",

        phoneNumber: "Nambala ya Foni kapena Mukuru ID",
        phoneNumberOnly: "Nambala ya Foni",

        currentCountry: "Malo Amene Muli / Dziko",
        countryOfResidence: "Dziko Limene Mumakhala",

        currency: "Ndalama Zowonetsedwa",
        preferredCurrency: "Ndalama Zomwe Mumakonda",

        pin: "PIN / Chinsinsi",
        createPin: "Pangani PIN Yachinsinsi",

        needHelp: "Mukufuna thandizo?",
        forgotPin: "Mwayiwala PIN yanu?",

        moneyCoach: "Mlangizi wa Ndalama",

        moneyCoachIntro:
            "Pezani thandizo losavuta losungira ndalama ndi kukwaniritsa zolinga zanu.",

        welcome: "👋 Takulandirani",

        signOut: "Tulukani",

        monthlyOverview: "Chidule cha Ndalama za Mwezi",

        moneyManaged:
            "Ndalama zomwe mwayendetsa mwezi uno",

        savingsGoals: "Zolinga Zanga Zosungira Ndalama",

        newGoal: "+ Cholinga Chatsopano",

        goalName: "Dzina la Cholinga",

        targetAmount: "Ndalama Zomwe Mukufuna",

        saveGoal: "Sungani Cholinga",

        cancel: "Letsani",

        expenseBreakdown: "Komwe Ndalama Zanu Zimapita",

        moneyTip: "💡 Malangizo a Ndalama",

        coachMessage:
            "Mukufuna thandizo pa ndalama zanu? Funsani mlangizi.",

        askCoach: "Funsani Mlangizi",

        viewReports: "Onani Malipoti Anga",

        schoolFees: "Ndalama za Sukulu ya Mlongo",

        fridge: "Firiji Kunyumba",

        remittances: "Ndalama Zotumizidwa Kunyumba",

        groceries: "Zakudya ndi Rent",

        airtime: "Airtime ndi Data"
    },


    // ------------------------------------------------------------
    // FRENCH
    // ------------------------------------------------------------

    fr: {
        tagline: "Des conseils simples pour gérer votre argent",

        signIn: "Se connecter",
        createAccount: "Créer un nouveau compte",

        phoneNumber: "Numéro de téléphone ou ID Mukuru",
        phoneNumberOnly: "Numéro de téléphone",

        currentCountry: "Pays / Lieu actuel",
        countryOfResidence: "Pays de résidence",

        currency: "Devise affichée",
        preferredCurrency: "Devise préférée",

        pin: "PIN / Mot de passe",
        createPin: "Créer un PIN secret",

        needHelp: "Besoin d'aide ?",
        forgotPin: "PIN oublié ?",

        moneyCoach: "Coach financier",

        moneyCoachIntro:
            "Obtenez des conseils simples pour économiser et atteindre vos objectifs.",

        welcome: "👋 Bienvenue",

        signOut: "Se déconnecter",

        monthlyOverview: "Résumé financier mensuel",

        moneyManaged:
            "Argent géré ce mois-ci",

        savingsGoals: "Mes objectifs d'épargne",

        newGoal: "+ Nouvel objectif",

        goalName: "Nom de l'objectif",

        targetAmount: "Montant cible",

        saveGoal: "Enregistrer",

        cancel: "Annuler",

        expenseBreakdown: "Où va votre argent",

        moneyTip: "💡 Conseil financier",

        coachMessage:
            "Besoin d'aide avec votre argent ? Demandez des conseils simples.",

        askCoach: "Demander au coach",

        viewReports: "Voir mes rapports",

        schoolFees: "Frais scolaires de ma sœur",

        fridge: "Réfrigérateur à la maison",

        remittances: "Argent envoyé à la maison",

        groceries: "Courses et loyer",

        airtime: "Crédit et données"
    },


    // ------------------------------------------------------------
    // PORTUGUESE
    // ------------------------------------------------------------

    pt: {
        tagline: "Orientação simples para gerir o seu dinheiro",

        signIn: "Entrar",
        createAccount: "Criar nova conta",

        phoneNumber: "Número de telefone ou ID Mukuru",
        phoneNumberOnly: "Número de telefone",

        currentCountry: "Localização / País atual",
        countryOfResidence: "País de residência",

        currency: "Moeda apresentada",
        preferredCurrency: "Moeda preferida",

        pin: "PIN / Palavra-passe",
        createPin: "Criar PIN secreto",

        needHelp: "Precisa de ajuda?",
        forgotPin: "Esqueceu o PIN?",

        moneyCoach: "Orientador Financeiro",

        moneyCoachIntro:
            "Receba ajuda simples para poupar, gastar e alcançar os seus objetivos.",

        welcome: "👋 Bem-vindo",

        signOut: "Sair",

        monthlyOverview: "Resumo financeiro mensal",

        moneyManaged:
            "Dinheiro gerido este mês",

        savingsGoals: "Os meus objetivos de poupança",

        newGoal: "+ Novo objetivo",

        goalName: "Nome do objetivo",

        targetAmount: "Valor pretendido",

        saveGoal: "Guardar objetivo",

        cancel: "Cancelar",

        expenseBreakdown: "Para onde vai o seu dinheiro",

        moneyTip: "💡 Dica financeira",

        coachMessage:
            "Precisa de ajuda com o seu dinheiro? Peça orientação simples.",

        askCoach: "Perguntar ao orientador",

        viewReports: "Ver os meus relatórios",

        schoolFees: "Propinas da minha irmã",

        fridge: "Frigorífico em casa",

        remittances: "Dinheiro enviado para casa",

        groceries: "Comida e renda",

        airtime: "Airtime e dados"
    }
};


// ================================================================
// 2. CURRENT LANGUAGE & USER STATE
// ================================================================

let currentLanguage = "en";
let userSymbol = "R";
let userManaged = 0; 
let userSentHome = 0; 
let userName = window.MUKURU_USER_NAME;


// ================================================================
// 3. CHANGE LANGUAGE
// ================================================================

function changeLanguage(language) {

    if (!translations[language]) {
        language = "en";
    }

    currentLanguage = language;

    const elements = document.querySelectorAll("[data-i18n]");

    elements.forEach(function (element) {

        const key = element.getAttribute("data-i18n");

        const translatedText =
            translations[language][key] ||
            translations.en[key] ||
            element.textContent;

        element.textContent = translatedText;
    });

    localStorage.setItem("mukuruLanguage", language);

    const authLanguage =
        document.getElementById("app-language-select");

    const dashboardLanguage =
        document.getElementById("dashboard-language-select");

    if (authLanguage) {
        authLanguage.value = language;
    }

    if (dashboardLanguage) {
        dashboardLanguage.value = language;
    }

    renderGoals();
    renderExpenses();
    renderOverview();
}


// ================================================================
// 4. LOAD SAVED LANGUAGE
// ================================================================

function loadSavedLanguage() {

    const savedLanguage =
        localStorage.getItem("mukuruLanguage");

    if (savedLanguage && translations[savedLanguage]) {
        changeLanguage(savedLanguage);
    } else {
        changeLanguage("en");
    }
}


// ================================================================
// 5. GOALS (Backend is the single source of truth)
// ================================================================
//
// Goals used to be cached in localStorage as well as in the API. After a
// server restart the browser still showed goals the API no longer had, and
// adding money updated only the screen. Every mutation now goes through the
// API and the server's response is what gets rendered.

let goals = [];

const esc = window.mukuruEsc || function (value) { return value; };

// ================================================================
// 6. DISPLAY GOALS
// ================================================================

function renderGoals() {
    const container = document.getElementById("goals-container");

    if (!container) {
        return;
    }

    container.innerHTML = "";

    if (goals.length === 0) {
        container.innerHTML = `
            <p style="color: #aaa; font-size: 0.9rem; text-align: center; padding: 12px 0;">
                No savings goals added yet. Click <strong>+ New Goal</strong> above to start saving!
            </p>
        `;
        return;
    }

    goals.forEach(function (goal, index) {
        const title = goal.customTitle
            || (translations[currentLanguage][goal.titleKey]
                || translations.en[goal.titleKey]
                || goal.title
                || "");

        const percentage = goal.target > 0
            ? Math.min(Math.round((goal.current / goal.target) * 100), 100)
            : 0;

        const goalCard = document.createElement("div");
        goalCard.className = "goal-item";
        goalCard.style.cssText = "margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #2a2a2a;";

        // The title is user-supplied, so it is escaped before going into
        // innerHTML. It was injected raw before.
        goalCard.innerHTML = `
            <div class="goal-top" style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <strong>${esc(title)}</strong>
                <span style="color: #FF6B00; font-weight: bold;">${percentage}%</span>
            </div>

            <div class="progress-bar" style="background: #333; height: 10px; border-radius: 5px; overflow: hidden; margin-bottom: 8px;">
                <div class="progress-fill"
                    style="width: ${percentage}%; background: #FF6B00; height: 100%; transition: width 0.3s ease;">
                </div>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center;">
                <p style="margin: 0;">
                    ${userSymbol}${goal.current.toLocaleString()} / ${userSymbol}${goal.target.toLocaleString()}
                </p>

                <div>
                    <button
                        class="btn-action"
                        style="background: #2a2a2a; color: #fff; border: 1px solid #444; border-radius: 6px; padding: 4px 10px; cursor: pointer; margin-right: 4px;"
                        onclick="addMoneyToGoal(${index})">
                        + Add Money
                    </button>
                    <button
                        class="btn-action"
                        style="background: #333; color: #ff5252; border: 1px solid #444; border-radius: 6px; padding: 4px 8px; cursor: pointer;"
                        onclick="deleteGoal(${index})">
                        TRASH
                    </button>
                </div>
            </div>
        `;

        container.appendChild(goalCard);
    });
}


// Delete a goal, confirming with the API before dropping it from the view.
async function deleteGoal(index) {
    if (!confirm("Are you sure you want to delete this goal?")) {
        return;
    }

    const goal = goals[index];

    try {
        const res = await window.mukuruFetch(
            `/goals/${goal.id}?user_id=${encodeURIComponent(USER_ID)}`,
            { method: "DELETE" }
        );
        // 404 means it is already gone, which is the state we wanted anyway.
        if (!res.ok && res.status !== 404) {
            throw new Error("HTTP " + res.status);
        }
        goals.splice(index, 1);
        renderGoals();
    } catch (err) {
        console.warn("Delete failed:", err);
        alert("Could not delete the goal. Please try again.");
    }
}


// ================================================================
// 7. ADD MONEY TO A GOAL
// ================================================================

async function addMoneyToGoal(index) {

    const amount = prompt(
        "How much would you like to add?"
    );

    const number = Number(amount);

    if (!amount || isNaN(number) || number <= 0) {
        alert("Please enter a valid amount.");
        return;
    }

    try {
        // Not mukuruFetch: this increments saved_amount server-side, so a blind
        // retry after an aborted timeout could credit the goal twice. An abort
        // only proves we stopped waiting, not that the server never saw it.
        const res = await window.mukuruFetchOnce(`/goals/${goals[index].id}/add-funds`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: USER_ID, amount: number })
        });
        if (!res.ok) {
            throw new Error("HTTP " + res.status);
        }
        const updated = await res.json();
        // Trust the server's number rather than our own arithmetic.
        goals[index].current = updated.saved_amount;
        renderGoals();
    } catch (err) {
        console.warn("Add funds failed:", err);
        alert("Could not add money right now. Nothing was changed.");
    }
}


// ================================================================
// 8. EXPENSES (Starts empty for new users)
// ================================================================

let expenses = [];


// ================================================================
// 9. DISPLAY EXPENSES
// ================================================================

function renderExpenses() {
    const container = document.getElementById("expenses-container");

    if (!container) {
        return;
    }

    container.innerHTML = "";

    // Show empty message for new users
    if (expenses.length === 0) {
        container.innerHTML = `
            <p style="color: #aaa; font-size: 0.9rem; text-align: center; padding: 12px 0;">
                No expense history found. Your spending breakdown will appear here once you make transactions!
            </p>
        `;
        return;
    }

    expenses.forEach(function (expense) {
        const title =
            translations[currentLanguage][expense.key] ||
            translations.en[expense.key] ||
            expense.customTitle ||
            expense.key;

        const row = document.createElement("div");
        row.className = "expense-item";
        row.style.cssText = "margin-bottom: 12px;";

        row.innerHTML = `
            <div class="expense-top" style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span>${esc(title)}</span>
                <strong>
                    ${userSymbol}${expense.amount.toLocaleString()}
                </strong>
            </div>

            <div class="progress-bar" style="background: #333; height: 8px; border-radius: 4px; overflow: hidden;">
                <div
                    class="progress-fill"
                    style="width: ${expense.percentage}%; background: #FF6B00; height: 100%;">
                </div>
            </div>
        `;

        container.appendChild(row);
    });
}


// ================================================================
// 10. OVERVIEW RENDERING
// ================================================================

function renderOverview() {
    const totalEl = document.getElementById("total-managed");
    const summaryEl = document.getElementById("remittance-summary");
    const greetingEl = document.getElementById("user-greeting");

    if (totalEl) {
        totalEl.textContent = `${userSymbol}${userManaged.toLocaleString()}`;
    }

    if (summaryEl) {
        summaryEl.textContent = `💸 ${userSymbol}${userSentHome.toLocaleString()} sent home this month`;
    }

    if (greetingEl) {
        const welcomeText = translations[currentLanguage]?.welcome || translations.en.welcome;
        greetingEl.textContent = `${welcomeText}, ${userName}`;
    }
}


// ================================================================
// 11. ADD NEW GOAL FORM SETUP
// ================================================================

function setupGoalForm() {

    const openButton =
        document.getElementById("toggle-goal-form-btn");

    const form =
        document.getElementById("add-goal-form");

    const saveButton =
        document.getElementById("save-goal-btn");

    const cancelButton =
        document.getElementById("cancel-goal-btn");

    if (!openButton || !form) {
        return;
    }

    openButton.addEventListener("click", function () {
        form.style.display = "block";
    });

    if (cancelButton) {
        cancelButton.addEventListener("click", function () {
            form.style.display = "none";
        });
    }

    if (saveButton) {
        saveButton.addEventListener("click", async function () {

            const title =
                document.getElementById("new-goal-title").value.trim();

            const target =
                Number(
                    document.getElementById("new-goal-target").value
                );

            if (!title || !target || target <= 0) {

                alert(
                    "Please enter a goal name and target amount."
                );

                return;
            }

            // The goal form has no date field, so default to six months out.
            const deadline = new Date();
            deadline.setMonth(deadline.getMonth() + 6);

            // Create server-side first. Pushing locally and then attempting the
            // API meant a failed request still showed the goal in the list.
            try {
                // Not mukuruFetch: a retry after an aborted timeout would create a second
                // goal with the same name.
                const response = await window.mukuruFetchOnce("/goals", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        user_id: USER_ID,
                        name: title,
                        target_amount: target,
                        saved_amount: 0,
                        deadline: deadline.toISOString().slice(0, 10)
                    })
                });
                if (!response.ok) {
                    throw new Error("HTTP " + response.status);
                }
                const saved = await response.json();
                goals.push({
                    id: saved.id,
                    customTitle: saved.name,
                    current: saved.saved_amount || 0,
                    target: saved.target_amount
                });
            } catch (err) {
                console.warn("Create goal failed:", err);
                alert("Could not save the goal. Please try again.");
                return;
            }

            form.style.display = "none";

            document.getElementById("new-goal-title").value = "";

            document.getElementById("new-goal-target").value = "";

            renderGoals();

        });
    }
}


// ================================================================
// PHONE VALIDATION
// ================================================================
// The country code lives in its own select, so the input holds the
// national number only. The placeholder ("82 123 4567") is 9 digits,
// while longer schemes run to 13, so a single fixed length would be
// wrong for some countries. Separators are stripped before counting so
// "82 123 4567", "082-123-4567" and "(082) 123 4567" all pass, while a
// stray letter or a lone digit is rejected.

const MIN_PHONE_DIGITS = 9;
const MAX_PHONE_DIGITS = 13;

function readPhoneDigits(value) {
    return (value || "").replace(/[^0-9]/g, "");
}

function validatePhoneField(input) {
    if (!input) {
        return true;
    }

    const digits = readPhoneDigits(input.value);
    let error = "";

    if (digits.length === 0) {
        error = input.value.trim() === ""
            ? "Please enter your mobile number."
            : "Please enter digits only - no letters or symbols.";
    } else if (digits.length < MIN_PHONE_DIGITS || digits.length > MAX_PHONE_DIGITS) {
        error = "Please enter a valid mobile number (" +
            MIN_PHONE_DIGITS + "-" + MAX_PHONE_DIGITS +
            " digits, e.g. 82 123 4567).";
    }

    // setCustomValidity lets the browser block submit and show the message
    // itself, so the error styling matches the rest of the form validation.
    input.setCustomValidity(error);

    if (error) {
        input.reportValidity();
        return false;
    }

    return true;
}

// ================================================================
// PIN VALIDATION
// ================================================================
// Auth itself is mocked for the demo, but the field still has to behave:
// `required` alone lets a single digit through, and maxlength="4" silently
// truncates a longer entry instead of telling the user. Exactly four
// digits, validated the same way as the phone so the browser blocks submit
// and renders the message inline rather than in an alert().

const PIN_LENGTH = 4;

function validatePinField(input) {
    if (!input) {
        return true;
    }

    const value = input.value.trim();
    let error = "";

    if (value === "") {
        error = "Please enter your PIN.";
    } else if (!/^[0-9]+$/.test(value)) {
        error = "Your PIN must be digits only.";
    } else if (value.length !== PIN_LENGTH) {
        error = "Your PIN must be exactly " + PIN_LENGTH + " digits.";
    }

    input.setCustomValidity(error);

    if (error) {
        input.reportValidity();
        return false;
    }

    return true;
}

// ================================================================
// 12. AUTHENTICATION & LOGIN FLOW
// ================================================================

function setupAuthFlow() {
    const tabLogin = document.getElementById("tab-login");
    const tabRegister = document.getElementById("tab-register");
    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");
    const authScreen = document.getElementById("auth-screen");
    const dashboardScreen = document.getElementById("dashboard-screen");
    const logoutBtn = document.getElementById("logout-btn");

    const currencySymbols = {
        ZAR: "R", USD: "$", MWK: "MK", ZMW: "K",
        KES: "KSh", GBP: "£", EUR: "€"
    };

    if (tabLogin && tabRegister) {
        tabLogin.addEventListener("click", function () {
            tabLogin.classList.add("active-tab");
            tabRegister.classList.remove("active-tab");
            loginForm.style.display = "block";
            registerForm.style.display = "none";
        });

        tabRegister.addEventListener("click", function () {
            tabRegister.classList.add("active-tab");
            tabLogin.classList.remove("active-tab");
            registerForm.style.display = "block";
            loginForm.style.display = "none";
        });
    }

    const loginPhone = document.getElementById("login-id");
    const regPhone = document.getElementById("reg-phone");
    const loginPin = document.getElementById("login-pin");
    const regPin = document.getElementById("reg-pin");

    // Clear a stale error as soon as the user edits, so the bubble does
    // not linger while they retype.
    [loginPhone, regPhone, loginPin, regPin].forEach(function (field) {
        if (field) {
            field.addEventListener("input", function () {
                field.setCustomValidity("");
            });
        }
    });

    if (loginForm) {
        loginForm.addEventListener("submit", async function (e) {
            e.preventDefault();

            if (!validatePhoneField(loginPhone)) {
                return;
            }

            if (!validatePinField(loginPin)) {
                return;
            }

            const selectedCurrency = document.getElementById("login-currency")?.value || "ZAR";
            userSymbol = currencySymbols[selectedCurrency] || "R";

            authScreen.style.display = "none";
            dashboardScreen.style.display = "block";

            // Fetch live overview & goals from FastAPI backend on sign-in
            await fetchDashboardData();
        });
    }

    if (registerForm) {
        registerForm.addEventListener("submit", async function (e) {
            e.preventDefault();

            if (!validatePhoneField(regPhone)) {
                return;
            }

            if (!validatePinField(regPin)) {
                return;
            }

            const nameInput = document.getElementById("reg-name")?.value.trim();
            const selectedCurrency = document.getElementById("reg-currency")?.value || "ZAR";

            if (nameInput) {
                userName = nameInput;
            }
            userSymbol = currencySymbols[selectedCurrency] || "R";

            authScreen.style.display = "none";
            dashboardScreen.style.display = "block";

            // Fetch initial dashboard state from backend
            await fetchDashboardData();
        });
    }

    if (logoutBtn) {
        logoutBtn.addEventListener("click", function () {
            dashboardScreen.style.display = "none";
            authScreen.style.display = "block";
        });
    }
}


// ================================================================
// 13. DASHBOARD NAVIGATION
// ================================================================

function setupNavigation() {

    const coachButton = document.getElementById("open-ai-chat");
    const coachButtonTop = document.getElementById("open-coach-btn");
    const reportsButton = document.getElementById("open-reports");

    if (coachButton) {
        coachButton.addEventListener("click", function () {
            window.location.href = "../ai-chat/index.html";
        });
    }

    if (coachButtonTop) {
        coachButtonTop.addEventListener("click", function () {
            window.location.href = "../ai-chat/index.html";
        });
    }

    if (reportsButton) {
        reportsButton.addEventListener("click", function () {
            // Standard relative path to Lead 3's onboarding page:
            window.location.href = "../Reports and polish/pages/onboarding.html";
        });
    }
}

// ================================================================
// 14. LANGUAGE SELECTORS
// ================================================================

function setupLanguageSelectors() {

    const authSelector =
        document.getElementById("app-language-select");

    const dashboardSelector =
        document.getElementById(
            "dashboard-language-select"
        );


    if (authSelector) {

        authSelector.addEventListener(
            "change",
            function () {

                changeLanguage(this.value);

            }
        );

    }


    if (dashboardSelector) {

        dashboardSelector.addEventListener(
            "change",
            function () {

                changeLanguage(this.value);

            }
        );

    }

}


// ================================================================
// 15. BACKEND API FETCH ENGINE
// ================================================================
// Maps onto the real FastAPI contract:
//   /budget/overview   -> GET  /analyze-budget   (current calendar month)
//   /budget/expenses   -> totals_by_category on the same /analyze-budget call
//   /goals/            -> GET  /goals
// The old /budget/* paths do not exist on the API and returned 404.

async function fetchDashboardData() {
    try {
        const [budgetRes, goalsRes] = await Promise.all([
            window.mukuruFetch(`/analyze-budget?user_id=${encodeURIComponent(USER_ID)}`),
            window.mukuruFetch(`/goals?user_id=${encodeURIComponent(USER_ID)}`)
        ]);

        // Overview and expenses both come from /analyze-budget, which is scoped
        // to the current calendar month. The old /budget/overview and
        // /budget/expenses paths do not exist on the API and returned 404.
        if (budgetRes.ok) {
            const budget = await budgetRes.json();

            userManaged = budget.total_income || 0;
            userSentHome = Math.abs(budget.totals_by_category?.remittance || 0);

            // Signed totals: debits are negative. Show only outflows, and size
            // each bar by its share of total spending.
            const outflows = Object.entries(budget.totals_by_category || {})
                .filter(([, amount]) => amount < 0)
                .map(([category, amount]) => ({ category, amount: Math.abs(amount) }));

            const totalSpend = outflows.reduce((sum, row) => sum + row.amount, 0);

            expenses = outflows.map(row => ({
                key: row.category,
                customTitle: row.category,
                amount: row.amount,
                percentage: totalSpend > 0 ? (row.amount / totalSpend) * 100 : 0
            }));
        }

        if (goalsRes.ok) {
            const goalsData = await goalsRes.json();
            if (Array.isArray(goalsData)) {
                goals = goalsData.map(g => ({
                    id: g.id,
                    customTitle: g.name,
                    current: g.saved_amount || 0,
                    target: g.target_amount || 0
                }));
            }
        }
    } catch (error) {
        console.warn("Backend API not reachable:", error);
    }

    renderOverview();
    renderGoals();
    renderExpenses();
}


// ================================================================
// 16. START THE DASHBOARD
// ================================================================

function startDashboard() {

    renderOverview();

    renderGoals();

    renderExpenses();

    setupGoalForm();

    setupNavigation();

    setupAuthFlow();

}


// ================================================================
// 17. START EVERYTHING
// ================================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        setupLanguageSelectors();

        startDashboard();

        loadSavedLanguage();

        fetchDashboardData();

    }
);