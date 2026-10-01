

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
});
