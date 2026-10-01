const downloadButton = document.getElementById("downloadButton");

downloadButton.addEventListener("click", function () {

    const report = `
MUKURU MONEY COACH
FINANCIAL HEALTH REPORT

========================

MONTHLY MONEY OVERVIEW

Monthly Income: R8,500
Money Sent Home: R2,000
Personal Expenses: R3,200
Money Saved: R3,300

========================

CREDIT SCORE

Current Credit Score: 682
Last Month: 658
Change: +24 points this month

========================

SAVINGS GOAL

Goal: School fees
Amount Saved: R4,000
Goal Amount: R5,000

========================

REMITTANCE HISTORY

25 September - R1,000
Family support

15 September - R500
Family support

05 September - R500
Family support

========================

Thank you for using Mukuru Money Coach.
`;

    const file = new Blob([report], {
        type: "text/plain"
    });

    const downloadLink = document.createElement("a");

    downloadLink.href = URL.createObjectURL(file);

    downloadLink.download = "Mukuru-Financial-Health-Report.txt";

    downloadLink.click();

    URL.revokeObjectURL(downloadLink.href);
});