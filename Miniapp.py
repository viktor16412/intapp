from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import requests
import os
import logging
from flask_cors import CORS  # Importar CORS

# Inicializar la aplicación Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS para todos los dominios

# Configura el logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar el scheduler
scheduler = BackgroundScheduler()
scheduler.start()
logger.info("Scheduler iniciado correctamente.")

# Función para enviar recordatorios
def send_reminder(chat_id, ticket_number):
    bot_token = "8144990341:AAEKsS6pLjSOYQIDlGZeuRtUO36N2N8hWLo"  # Reemplaza con tu token de bot
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": 1462654118,
        "text": f"🔔 Recordatorio: El ticket {ticket_number} tiene un recordatorio programado para hoy."
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Lanza una excepción si la respuesta no es 2xx
        logger.info(f"Recordatorio enviado correctamente a {chat_id} para el ticket {ticket_number}.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error al enviar el recordatorio: {e}")

# Ruta raíz
@app.route('/')
def home():
    return "¡Bienvenido a la API de recordatorios!"

# Ruta para programar recordatorios
@app.route('/api/schedule-reminder', methods=['POST'])
def schedule_reminder():
    # Verificar que el Content-Type sea application/json
    if not request.is_json:
        logger.error("Content-Type debe ser application/json")
        return jsonify({"error": "Content-Type debe ser application/json"}), 415

    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.get_json()
        ticket_number = data['ticketNumber']
        profile_date = datetime.fromisoformat(data['profileDate'])
        chat_id = data['chatId']

        # Programar recordatorio para 6 días después de la fecha de perfilado
        reminder_date = profile_date + timedelta(days=6)
        scheduler.add_job(
            send_reminder,
            'date',
            run_date=reminder_date,
            args=[chat_id, ticket_number]
        )

        logger.info(f"Recordatorio programado para el {reminder_date}.")
        return jsonify({"message": f"Recordatorio programado para el {reminder_date}."}), 200

    except KeyError as e:
        logger.error(f"Falta un campo requerido en la solicitud: {e}")
        return jsonify({"error": f"Falta un campo requerido: {e}"}), 400
    except ValueError as e:
        logger.error(f"Formato de fecha inválido: {e}")
        return jsonify({"error": "Formato de fecha inválido"}), 400
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500



# Detener el scheduler cuando la aplicación se detenga
@app.teardown_appcontext
def shutdown_scheduler(exception=None):
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler detenido correctamente.")

# Iniciar la aplicación
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)  # Escucha en 0.0.0.0