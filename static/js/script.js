let forecastData = [];
const themeBtn = document.getElementById('theme-btn');
const themeIcon = document.getElementById('theme-icon');

themeBtn.onclick = () => {
    document.body.classList.toggle('light-theme');
    const isLight = document.body.classList.contains('light-theme');
    themeIcon.innerText = isLight ? '☀️' : '🌙';
};

async function loadWeatherIntelligence() {
    try {
        const response = await fetch('/api/forecast_data');
        const result = await response.json();
        forecastData = result.forecast;
        
        renderForecastList();
        updateMainDisplay(0);
        
        // Live Professional Clock
        setInterval(() => {
            const time = new Date();
            document.getElementById('live-clock').innerText = 
                time.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'short' }).toUpperCase() + 
                " | " + time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        }, 1000);

    } catch (err) {
        console.error("Dashboard failed to sync:", err);
        document.getElementById('city-title').innerText = "CONNECTION LOST";
    }
}

function updateMainDisplay(index) {
    const day = forecastData[index];
    document.getElementById('big-temp').innerText = Math.round(day.temp);
    document.getElementById('main-condition').innerText = day.condition.toUpperCase();
    document.getElementById('hum-val').innerText = day.humidity + "%";
    document.getElementById('wind-val').innerText = day.wind + " km/h";
    document.getElementById('pres-val').innerText = day.pressure + " hPa";
    document.getElementById('rise-val').innerText = day.sunrise;
    document.getElementById('set-val').innerText = day.sunset;

    const hourBox = document.getElementById('hour-row');
    hourBox.innerHTML = day.hourly.map(h => `
        <div class="hour-item">
            <div style="font-size: 11px; opacity: 0.6; margin-bottom: 8px;">${h.time}</div>
            <div style="font-size: 24px; margin-bottom: 8px;">${day.temp > 25 ? '☀️' : '☁️'}</div>
            <div style="font-weight: 700; font-size: 20px;">${Math.round(h.t)}°</div>
        </div>
    `).join('');
    document.querySelectorAll('.day-item').forEach((item, i) => {
        item.classList.toggle('active', i === index);
    });
}

function renderForecastList() {
    const list = document.getElementById('day-list');
    list.innerHTML = forecastData.map((d, i) => `
        <div class="day-item" onclick="updateMainDisplay(${i})">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-weight: 700; font-size: 17px;">${d.day_name}</div>
                    <div style="font-size: 11px; opacity: 0.6;">${d.date}</div>
                </div>
                <div style="font-size: 22px; font-weight: 700;">${Math.round(d.temp)}°</div>
            </div>
        </div>
    `).join('');
}

document.addEventListener('DOMContentLoaded', loadWeatherIntelligence);