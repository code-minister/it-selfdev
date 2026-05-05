fetch('https://api.portfolio.local')
    .then(response => response.json())
    .then(data => {
        document.getElementById('api-response').innerText = 
            `Сообщение: ${data.message} | Обработано портом: ${data.port}`;
    })
    .catch(err => {
        document.getElementById('api-response').innerText = "Ошибка CORS или API недоступно!";
        console.error(err);
    });