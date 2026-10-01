const startButton = document.getElementById("startButton");
const welcomeSection = document.querySelector(".welcome-section");

startButton.addEventListener("click", function () {

    welcomeSection.innerHTML = `
        <h1>What are you working towards?</h1>

        <p>Choose your main financial goal to get started.</p>

        <label>
            <input type="radio" name="goal" value="Saving money">
            Saving money
        </label>

        <br><br>

        <label>
            <input type="radio" name="goal" value="Sending money home">
            Sending money home
        </label>

        <br><br>

        <label>
            <input type="radio" name="goal" value="Building credit">
            Building my credit history
        </label>

        <br><br>

        <label>
            <input type="radio" name="goal" value="Managing expenses">
            Managing my expenses
        </label>

        <br><br>

        <button id="continueButton">Continue</button>
    `;

    const continueButton = document.getElementById("continueButton");

    continueButton.addEventListener("click", function () {

        welcomeSection.innerHTML = `
            <h1>Tell us a little about you</h1>

            <p>
                This will help us personalise your Money Coach experience.
            </p>

            <label for="income">
                What is your monthly income?
            </label>

            <br><br>

            <input
                type="number"
                id="income"
                placeholder="Enter amount in R"
            >

            <br><br>

            <button id="incomeButton">Continue</button>
        `;

        const incomeButton = document.getElementById("incomeButton");

        incomeButton.addEventListener("click", function () {

            welcomeSection.innerHTML = `
                <h1>What would you like help with?</h1>

                <p>
                    Choose an area you want your Money Coach
                    to focus on.
                </p>

                <label>
                    <input
                        type="radio"
                        name="priority"
                        value="Budgeting"
                    >
                    Managing my budget
                </label>

                <br><br>

                <label>
                    <input
                        type="radio"
                        name="priority"
                        value="Saving"
                    >
                    Saving more money
                </label>

                <br><br>

                <label>
                    <input
                        type="radio"
                        name="priority"
                        value="Credit"
                    >
                    Improving my credit
                </label>

                <br><br>

                <label>
                    <input
                        type="radio"
                        name="priority"
                        value="Remittances"
                    >
                    Managing money I send home
                </label>

                <br><br>

                <button id="completeButton">Finish</button>
            `;

            const completeButton =
                document.getElementById("completeButton");

            completeButton.addEventListener("click", function () {

                welcomeSection.innerHTML = `
                    <h1>You're all set!</h1>

                    <p>
                        Your Money Coach profile is ready.
                        Let's start managing your money.
                    </p>

                    <button id="accountButton">
                        Go to My Account
                    </button>
                `;

                const accountButton =
                    document.getElementById("accountButton");

                accountButton.addEventListener("click", function () {
                    window.location.href = "account.html";
                });
            });
        });
    });
});