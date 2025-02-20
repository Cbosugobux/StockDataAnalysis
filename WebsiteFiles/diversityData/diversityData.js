console.log("✅ JavaScript is running!");

// ✅ Embedded JSON Data (Apple, Nvidia, Microsoft, Amazon, Google, 2017 & 2021)
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

// ✅ Function to Generate Chart with Toggle Functionality
function generateChart() {
    const ctx = document.getElementById("diversityChart").getContext("2d");

    const categories = ["gender_female", "gender_male", "race_white", "race_asian", "race_hispanic", "race_black"];
    const categoryColors = {
        "gender_female": "#D81B60",
        "gender_male": "#1E88E5",
        "race_white": "#BDBDBD",
        "race_asian": "#03A9F4",
        "race_hispanic": "#FF5722",
        "race_black": "#4CAF50"
    };

    const uniqueCompanies = [...new Set(diversityData.map(entry => entry.company))];

    // ✅ Prepare Dataset for Each Category
    const datasets = categories.map(category => ({
        label: category.replace("_", " ").toUpperCase() + " (%)",
        data: diversityData.map(entry => entry[category]),
        backgroundColor: categoryColors[category],
        hidden: false // Ensure all datasets are visible initially
    }));

    const labels = diversityData.map(entry => `${entry.company} (${entry.year})`);

    // ✅ Destroy Existing Chart (if any)
    if (window.diversityChartInstance) {
        window.diversityChartInstance.destroy();
    }

    // ✅ Create New Chart
    window.diversityChartInstance = new Chart(ctx, {
        type: "bar",
        data: { labels, datasets },
        options: {
            responsive: true,
            plugins: { 
                legend: {
                    display: true,
                    onClick: function (e, legendItem, legend) {
                        const index = legendItem.datasetIndex;
                        legend.chart.toggleDatasetVisibility(index);
                    }
                }
            },
            scales: { 
                y: { beginAtZero: true },
                x: { stacked: false }
            }
        }
    });

    console.log("✅ Chart generated with category toggles.");
}

// ✅ Load Chart on Page Load
document.addEventListener("DOMContentLoaded", generateChart);
