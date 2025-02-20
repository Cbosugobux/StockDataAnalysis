console.log("JavaScript is running!");

// Embedded JSON Data (Apple, Nvidia, Microsoft, Amazon, Google, 2017 & 2021)
const diversityData = [
    { "company": "Apple", "year": 2017, "gender_female": 32, "gender_male": 68, "race_white": 54, "race_asian": 21, "race_hispanic": 13, "race_black": 9 },
    { "company": "Apple", "year": 2021, "gender_female": 34.8, "gender_male": 65.2, "race_white": 43.8, "race_asian": 27.9, "race_hispanic": 14.8, "race_black": 9.4 },
    { "company": "Nvidia", "year": 2017, "gender_female": 17, "gender_male": 83, "race_white": 37, "race_asian": 45, "race_hispanic": 3, "race_black": 1 },
    { "company": "Nvidia", "year": 2021, "gender_female": 19.1, "gender_male": 80.3, "race_white": 38.3, "race_asian": 47.5, "race_hispanic": 3.3, "race_black": 2.5 },
    { "company": "Microsoft", "year": 2017, "gender_female": 26, "gender_male": 74, "race_white": 56, "race_asian": 31, "race_hispanic": 6, "race_black": 4 },
    { "company": "Microsoft", "year": 2021, "gender_female": 29.7, "gender_male": 70.3, "race_white": 48.6, "race_asian": 35.6, "race_hispanic": 7.0, "race_black": 5.7 },
    { "company": "Amazon", "year": 2017, "gender_female": 39, "gender_male": 61, "race_white": 48, "race_asian": 13, "race_hispanic": 13, "race_black": 21 },
    { "company": "Amazon", "year": 2021, "gender_female": 44.3, "gender_male": 55.6, "race_white": 30.7, "race_asian": 13.5, "race_hispanic": 23.6, "race_black": 28.6 },
    { "company": "Google (Alphabet)", "year": 2017, "gender_female": 31, "gender_male": 69, "race_white": 56, "race_asian": 35, "race_hispanic": 4, "race_black": 2 },
    { "company": "Google (Alphabet)", "year": 2021, "gender_female": 32.5, "gender_male": 67.5, "race_white": 50.4, "race_asian": 42.3, "race_hispanic": 6.4, "race_black": 4.4 }
];

// Function to Get Selected Values from Multi-Select Dropdowns
function getSelectedValues(selectElement) {
    return Array.from(selectElement.selectedOptions).map(option => option.value);
}

// Function to Update Chart When Selections Change
function updateChart() {
    const selectedCompanies = getSelectedValues(document.getElementById("company-filter"));
    const selectedCategories = getSelectedValues(document.getElementById("category-filter"));
    const selectedYear = document.getElementById("year-filter").value;

    const filteredData = diversityData.filter(entry =>
        (selectedCompanies.length === 0 || selectedCompanies.includes(entry.company)) &&
        entry.year == selectedYear
    );

    if (filteredData.length === 0) {
        console.error("❌ No data available for selected filters.");
        return;
    }

    // Prepare Chart Data
    const labels = filteredData.map(entry => `${entry.company} (${entry.year})`);
    const datasets = selectedCategories.map(category => ({
        label: category.replace("_", " ") + " (%)",
        data: filteredData.map(entry => entry[category] ?? 0),
        backgroundColor: `hsl(${Math.random() * 360}, 70%, 60%)`
    }));

    // Clear Existing Chart
    if (window.diversityChartInstance) {
        window.diversityChartInstance.destroy();
    }

    // Create New Chart
    const ctx = document.getElementById("diversityChart").getContext("2d");
    window.diversityChartInstance = new Chart(ctx, {
        type: "bar",
        data: { labels, datasets },
        options: { 
            responsive: true,
            plugins: { 
                legend: {
                    display: true,
                    labels: { color: "white" },
                    onClick: function (e, legendItem, legend) {
                        const index = legendItem.datasetIndex;
                        legend.chart.toggleDatasetVisibility(index);
                    }
                }
            },
            scales: { 
                y: { beginAtZero: true, ticks: { color: "white" } },
                x: { ticks: { color: "white" } }
            }
        }
    });

    console.log("Chart updated:", selectedCompanies, selectedCategories);
}

// Attach Event Listeners to Dropdowns
document.querySelectorAll("#company-filter, #category-filter, #year-filter").forEach(select => {
    select.addEventListener("change", updateChart);
});

// Load Chart on Page Load
document.addEventListener("DOMContentLoaded", updateChart);