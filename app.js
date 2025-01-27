// Inicializar la Web App de Telegram
const tg = window.Telegram.WebApp;

tg.ready(); // Mostrar la interfaz de la Web App

// Manejar el envío del formulario
document.getElementById('ticketForm').addEventListener('submit', (e) => {
    e.preventDefault();

    // Deshabilitar el botón de envío
    const submitButton = document.getElementById('submitButton');
    submitButton.disabled = true;

    // Obtener los valores del formulario
    const ticketNumber = document.getElementById('ticketNumber').value;
    const profileDate = document.getElementById('profileDate').value + 'T00:00:00'; // Añadir hora
    const chatId = tg.initDataUnsafe?.user?.id; // Obtener el ID del usuario

    // Verificar si el chatId está disponible
    if (!chatId) {
        console.error("No se pudo obtener el ID del usuario.");
        document.getElementById('message').textContent = "Error: No se pudo obtener el ID del usuario.";
        document.getElementById('message').style.color = 'red';
        submitButton.disabled = false; // Rehabilitar el botón
        return;
    }

    // Enviar datos al backend
    fetch('https://intapp-4.onrender.com/api/schedule-reminder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            ticketNumber,
            profileDate,
            chatId,
        }),
    })
    .then(response => {
        if (!response.ok) {
            // Si la respuesta no es exitosa, lanzar un error
            return response.json().then(err => {
                throw new Error(err.error || "Error en el servidor");
            });
        }
        return response.json();
    })
    .then(data => {
        // Mostrar mensaje de éxito
        document.getElementById('message').textContent = data.message;
        document.getElementById('message').style.color = 'green';
    })
    .catch(error => {
        // Mostrar mensaje de error
        console.error('Error:', error);
        document.getElementById('message').textContent = error.message;
        document.getElementById('message').style.color = 'red';
    })
    .finally(() => {
        submitButton.disabled = false; // Rehabilitar el botón
    });
});