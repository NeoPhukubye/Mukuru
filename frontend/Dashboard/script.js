// ================================================================
// MUKURU MONEY COACH
// Main Dashboard JavaScript
// ================================================================

// ================================================================
// API CONFIGURATION
// ================================================================
const API_BASE_URL = "http://127.0.0.1:8000"; // Local FastAPI server URL

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
let userName = "Grace";


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
// 5. GOALS (Dynamic Array - Syncs with LocalStorage & Backend API)
// ================================================================

let goals = JSON.parse(localStorage.getItem("mukuruGoals")) || [];

// ================================================================
// 6. DISPLAY GOALS
// ================================================================

function renderGoals() {
    const container = document.getElementById("goals-container");

    if (!container) {
        return;
    }

    container.innerHTML = "";

    // Save updated goals list to local storage
    localStorage.setItem("mukuruGoals", JSON.stringify(goals));

    // Show message if user has no active goals
    if (goals.length === 0) {
        container.innerHTML = `
            <p style="color: #aaa; font-size: 0.9rem; text-align: center; padding: 12px 0;">
                No savings goals added yet. Click <strong>+ New Goal</strong> above to start saving!
            </p>
        `;
        return;
    }

    goals.forEach(function (goal, index) {
        let title = goal.customTitle || (translations[currentLanguage][goal.titleKey] || translations.en[goal.titleKey] || goal.title);

        const percentage = goal.target > 0 
            ? Math.min(Math.round((goal.current / goal.target) * 100), 100)
            : 0;

        const goalCard = document.createElement("div");
        goalCard.className = "goal-item";
        goalCard.style.cssText = "margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #2a2a2a;";

        goalCard.innerHTML = `
            <div class="goal-top" style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <strong>${title}</strong>
                <span style="color: #FF6B00; font-weight: bold;">${percentage}%</span>
            </div>

            <div class="progress-bar" style="background: #333; height: 10px; border-radius: 5px; overflow: hidden; margin-bottom: 8px;">
                <div
                    class="progress-fill"
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
                        🗑️
                    </button>
                </div>
            </div>
        `;

        container.appendChild(goalCard);
    });
}

// Function to allow deleting a goal
async function deleteGoal(index) {
    if (confirm("Are you sure you want to delete this goal?")) {
        const goalToDelete = goals[index];
        if (goalToDelete.id) {
            try {
                await fetch(`${API_BASE_URL}/goals/${goalToDelete.id}`, { method: "DELETE" });
            } catch (err) {
                console.warn("Backend delete endpoint unreachable, deleting locally:", err);
            }
        }
        goals.splice(index, 1);
        renderGoals();
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

        alert(
            "Please enter a valid amount."
        );

        return;
    }

    goals[index].current += number;

    // Send update to FastAPI backend if goal ID exists
    if (goals[index].id) {
        try {
            await fetch(`${API_BASE_URL}/goals/${goals[index].id}/add-funds`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ amount: number })
            });
        } catch (err) {
            console.warn("Backend update unreachable, updated locally:", err);
        }
    }

    renderGoals();
}

// ================================================================
// 8. EXPENSES (Starts empty for new users)
// ================================================================

let expenses = JSON.parse(localStorage.getItem("mukuruExpenses")) || [];


// ================================================================
// 9. DISPLAY EXPENSES
// ================================================================

function renderExpenses() {
    const container = document.getElementById("expenses-container");

    if (!container) {
        return;
    }

    container.innerHTML = "";

    // Save state
    localStorage.setItem("mukuruExpenses", JSON.stringify(expenses));

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
                <span>${title}</span>
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

            const newGoalObj = {
                titleKey: null,
                customTitle: title,
                current: 0,
                target: target
            };

            // Post new goal to FastAPI backend router
            try {
                const response = await fetch(`${API_BASE_URL}/goals/`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        title: title,
                        target_amount: target,
                        current_amount: 0
                    })
                });
                if (response.ok) {
                    const savedBackendGoal = await response.json();
                    newGoalObj.id = savedBackendGoal.id;
                }
            } catch (err) {
                console.warn("Backend server offline, saved goal locally:", err);
            }

            goals.push(newGoalObj);

            form.style.display = "none";

            document.getElementById("new-goal-title").value = "";

            document.getElementById("new-goal-target").value = "";

            renderGoals();

        });
    }
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

    if (loginForm) {
        loginForm.addEventListener("submit", async function (e) {
            e.preventDefault();
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

    const coachButton =
        document.getElementById("open-ai-chat");

    const coachButtonTop =
        document.getElementById("open-coach-btn");

    const reportsButton =
        document.getElementById("open-reports");


    if (coachButton) {

        coachButton.addEventListener(
            "click",
            function () {

                window.location.href =
                    "../ai-chat/index.html";

            }
        );

    }


    if (coachButtonTop) {

        coachButtonTop.addEventListener(
            "click",
            function () {

                window.location.href =
                    "../ai-chat/index.html";

            }
        );

    }


    if (reportsButton) {

        reportsButton.addEventListener(
            "click",
            function () {

                window.location.href =
                    "../Reports and polish/pages/onboarding.html";

            }
        );

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

async function fetchDashboardData() {
    try {
        // 1. Fetch budget overview from FastAPI
        const overviewRes = await fetch(`${API_BASE_URL}/budget/overview`);
        if (overviewRes.ok) {
            const overviewData = await overviewRes.json();
            userManaged = overviewData.total_managed || 0;
            userSentHome = overviewData.sent_home || 0;
            renderOverview();
        }

        // 2. Fetch savings goals from FastAPI
        const goalsRes = await fetch(`${API_BASE_URL}/goals/`);
        if (goalsRes.ok) {
            const goalsData = await goalsRes.json();
            if (Array.isArray(goalsData) && goalsData.length > 0) {
                goals = goalsData.map(g => ({
                    id: g.id,
                    customTitle: g.title,
                    current: g.current_amount || 0,
                    target: g.target_amount || 0
                }));
            }
            renderGoals();
        }

        // 3. Fetch expense breakdown from FastAPI
        const expensesRes = await fetch(`${API_BASE_URL}/budget/expenses`);
        if (expensesRes.ok) {
            const expensesData = await expensesRes.json();
            if (Array.isArray(expensesData) && expensesData.length > 0) {
                expenses = expensesData.map(e => ({
                    key: e.category ? e.category.toLowerCase() : "other",
                    customTitle: e.category,
                    amount: e.amount || 0,
                    percentage: e.percentage || 0
                }));
            }
            renderExpenses();
        }
    } catch (error) {
        console.warn("Backend API server not reachable. Running on local state:", error);
        renderOverview();
        renderGoals();
        renderExpenses();
    }
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