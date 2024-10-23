// Event listener for the button to fetch the weather summary
document.getElementById('fetch-summary').addEventListener('click', function () {
    const selectedCity = document.getElementById('city-select').value; // Get the selected city
    if (selectedCity) {
        fetchWeatherSummary(selectedCity); // Fetch summary for the selected city
    } else {
        alert("Please select a city."); // Alert if no city is selected
    }
});

// Function to fetch weather summary for a specific city
function fetchWeatherSummary(city) {
    fetch(`/api/weather_summary?city=${city}`) // Fetch summary from the API
        .then(response => response.json())
        .then(data => {
            const summaryDiv = document.getElementById('weather-summary');
            summaryDiv.innerHTML = ''; // Clear previous summary

            if (data.length > 0) {
                const summary = data[0]; // Get the summary for the selected city
                summaryDiv.innerHTML += `
                    <h3>${summary.city}</h3>
                    <p>Average Temperature: ${summary.average_temp.toFixed(2)} °C</p>
                    <p>Max Temperature: ${summary.max_temp.toFixed(2)} °C</p>
                    <p>Min Temperature: ${summary.min_temp.toFixed(2)} °C</p>
                    <p>Dominant Condition: ${summary.dominant_condition}</p>
                `;
            } else {
                summaryDiv.innerHTML = '<p>No data available for this city.</p>'; // Handle no data case
            }
        })
        .catch(error => console.error('Error fetching weather summary:', error)); // Log errors
};
