from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import requests
import os

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

# Función para enviar recordatorios
def send_reminder(chat_id, ticket_number):
    bot_token = "8144990341:AAEKsS6pLjSOYQIDlGZeuRtUO36N2N8hWLo"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": f"🔔 Recordatorio: El ticket {ticket_number} tiene un recordatorio programado para hoy."
    }
    requests.post(url, json=payload)

# Ruta para programar recordatorios
@app.route('/api/schedule-reminder', methods=['POST'])
def schedule_reminder():
    data = request.json
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

    return jsonify({"message": f"Recordatorio programado para el {reminder_date}."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Usa el puerto de Render o 5000 por defecto
    app.run(host='0.0.0.0', port=port)  # Escucha en 0.0.0.0