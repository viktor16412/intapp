// Inicializar la Web App de Telegram
const tg = window.Telegram.WebApp;

tg.ready(); // Mostrar la interfaz de la Web App

// Manejar el envío del formulario
document.getElementById('ticketForm').addEventListener('submit', (e) => {
    e.preventDefault();

    const ticketNumber = document.getElementById('ticketNumber').value;
    const profileDate = document.getElementById('profileDate').value;

    // Enviar datos al backend
    fetch('https://tudominio.com/api/schedule-reminder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            ticketNumber,
            profileDate,
            chatId: tg.initDataUnsafe.user.id, // Obtener el ID del usuario
        }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('message').textContent = data.message;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});