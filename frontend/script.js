async function getWeather() {
    const city = document.getElementById("cityInput").value;
    if (!city) {
        alert("Please enter a city name");
        return;
    }

    const response = await fetch(`http://127.0.0.1:8000/weather/${city}`);
    const data = await response.json();

    if (response.ok) {
        document.getElementById("weatherResult").innerHTML = `
            <h2>${data.location.name}, ${data.location.country}</h2>
            <p>Temperature: ${data.current.temp_c}°C</p>
            <p>Condition: ${data.current.condition.text}</p>
            <img src="${data.current.condition.icon}" alt="Weather icon">
        `;
    } else {
        document.getElementById("weatherResult").innerHTML = `<p>Error: ${data.detail}</p>`;
    }
}
