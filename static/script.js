let timeRemaining = 300; // 5 minutes in seconds
const timerElement = document.getElementById('time-remaining');

function startTimer() {
    const interval = setInterval(() => {
        const minutes = Math.floor(timeRemaining / 60);
        const seconds = timeRemaining % 60;
        timerElement.innerText = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

        if (timeRemaining <= 0) {
            clearInterval(interval);
            fetchWeatherData(); // Fetch new data after timer expires
            timeRemaining = 300; // Reset timer
            startTimer(); // Restart timer
        }
        timeRemaining--;
    }, 1000);
}

// Function to fetch weather data
async function fetchWeatherData() {
    try {
        const response = await fetch('/api/weather');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        updateWeatherData(data);
    } catch (error) {
        console.error('Error fetching weather data:', error);
    }
}

function updateWeatherData(data) {
    // Update alerts section - New Addition
    const alertsContainer = document.getElementById('alerts');
    alertsContainer.innerHTML = ''; // Clear previous alerts
    if (data.alerts) {
        data.alerts.forEach(alert => {
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert';
            alertDiv.innerText = alert;
            alertsContainer.appendChild(alertDiv);
        });
    }

    // Update weather summary
    const weatherSummaryDiv = document.getElementById('weather-summary');
    weatherSummaryDiv.innerHTML = ''; // Clear previous data

    for (const city in data.weather_data) {
        const cityData = data.weather_data[city];
        const cityDiv = document.createElement('div');
        cityDiv.className = 'city-summary';
        cityDiv.innerHTML =
            `<h3>${city}</h3>` +
            `<i class="fas ${cityData.main_icon}"></i>` +
            `<p>Main Condition : ${cityData.main}</p>` +
            `<p>Current Temperature : ${cityData.temp.toFixed(2)} °C</p>` +
            `<p>Feels Like : ${cityData.feels_like.toFixed(2)} °C</p>` +
            `<p>Humidity : ${cityData.humidity}%</p>` +
            `<p>Wind Speed : ${cityData.wind_speed} m/s</p>` +
            `<p>Pressure : ${cityData.pressure} hPa</p>` +
            `<p>Visibility : ${cityData.visibility.toFixed(2)} km</p>` +
            `<p>Last Updated : ${new Date(cityData.dt * 1000).toLocaleString()}</p>`;

        weatherSummaryDiv.appendChild(cityDiv);
    }
}

// Fetch daily weather summary on button click
document.getElementById('daily-summary-button').addEventListener('click', fetchDailySummary);

// Function to fetch daily weather summary
async function fetchDailySummary() {
    try {
        const response = await fetch('/api/daily_summary');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const dailyData = await response.json();
        console.log('Daily Summary Data:', dailyData); // Log the data received

        const dailySummaryBody = document.getElementById('daily-summary-body');
        dailySummaryBody.innerHTML = ''; // Clear previous summary data

        // Check if dailyData is an array and log its length
        if (!Array.isArray(dailyData) || dailyData.length === 0) {
            console.log('No data available or not an array');
            dailySummaryBody.innerHTML = '<tr><td colspan="5">No data available</td></tr>';
            return;
        }

        // Populate the table with the fetched data
        dailyData.forEach(summary => {
            const row = document.createElement('tr');
            row.innerHTML =
                `<td>${summary.date}</td>` +
                `<td>${summary.avg_temp.toFixed(2)}</td>` +
                `<td>${summary.max_temp.toFixed(2)}</td>` +
                `<td>${summary.min_temp.toFixed(2)}</td>` +
                `<td>${summary.dominant_condition}</td>`;
            dailySummaryBody.appendChild(row);
        });

        // Now render the chart with the fetched data
        renderChart(dailyData);

    } catch (error) {
        console.error('Error fetching daily summary:', error);
        const dailySummaryBody = document.getElementById('daily-summary-body');
        dailySummaryBody.innerHTML = '<tr><td colspan="5">Error fetching data</td></tr>';
    }
}

// Function to render the chart with daily summary data
function renderChart(dailyData) {
    const ctx = document.getElementById('weatherChart').getContext('2d');
    const labels = dailyData.map(summary => summary.date);
    const avgTemps = dailyData.map(summary => summary.avg_temp);
    const maxTemps = dailyData.map(summary => summary.max_temp);
    const minTemps = dailyData.map(summary => summary.min_temp);

    const weatherChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Average Temperature (°C)',
                    data: avgTemps,
                    borderColor: 'rgba(75,192,192,1)',
                    fill: false,
                },
                {
                    label: 'Max Temperature (°C)',
                    data: maxTemps,
                    borderColor: 'rgba(255,99,132,1)',
                    fill: false,
                },
                {
                    label: 'Min Temperature (°C)',
                    data: minTemps,
                    borderColor: 'rgba(54,162,235,1)',
                    fill: false,
                },
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        }
    });
}

// Auto-fetch weather data when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchWeatherData();
    startTimer(); // Start the timer
});
