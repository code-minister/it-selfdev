const http = require('http');

// Берем порт из аргументов командной строки (например: node server.js 3000)
const port = process.argv[2] || 3000;

const requestHandler = (request, response) => {
    console.log(`Получен запрос на порт ${port}`);
    response.setHeader('Content-Type', 'application/json');

    response.writeHead(200);
    response.end(JSON.stringify({ 
        message: "Привет от бэкенда!", 
        port: port,
        time: new Date().toISOString()
    }));
};

const server = http.createServer(requestHandler);

server.listen(port, (err) => {
    if (err) return console.log('Ошибка', err);
    console.log(`API Сервер запущен на порту ${port}`);
});