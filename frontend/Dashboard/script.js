let schoolFeesCurrent = 400;
const schoolFeesTarget = 1000;

let fridgeCurrent = 300;
const fridgeTarget = 1500;

const schoolText = document.getElementById('school-text');
const schoolBar = document.getElementById('school-bar');
const addSchoolBtn = document.getElementById('add-school-btn');

const fridgeText = document.getElementById('fridge-text');
const fridgeBar = document.getElementById('fridge-bar');
const addFridgeBtn = document.getElementById('add-fridge-btn');

addSchoolBtn.addEventListener('click', () => {
  if (schoolFeesCurrent < schoolFeesTarget) {
    schoolFeesCurrent = Math.min(schoolFeesCurrent + 50, schoolFeesTarget);
    const percentage = Math.round((schoolFeesCurrent / schoolFeesTarget) * 100);
    schoolText.textContent = `R${schoolFeesCurrent} / R${schoolFeesTarget}`;
    schoolBar.style.width = `${percentage}%`;
  }
});

addFridgeBtn.addEventListener('click', () => {
  if (fridgeCurrent < fridgeTarget) {
    fridgeCurrent = Math.min(fridgeCurrent + 50, fridgeTarget);
    const percentage = Math.round((fridgeCurrent / fridgeTarget) * 100);
    fridgeText.textContent = `R${fridgeCurrent} / R${fridgeTarget}`;
    fridgeBar.style.width = `${percentage}%`;
  }
});