from firebase_admin import firestore

def save_user_to_firestore(user):
    db = firestore.client()
    users_ref = db.collection('users')
    users_ref.add({
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'timestamp': firestore.SERVER_TIMESTAMP
    })

def save_plant_to_firestore(plant):
    db = firestore.client()
    plants_ref = db.collection('plants')
    plants_ref.add({
        'user_id': plant.user.id,
        'name': plant.name,
        'planting_date': plant.planting_date,
        'soil_type': plant.soil_type,
        'timestamp': firestore.SERVER_TIMESTAMP
    })

def save_growth_history_to_firestore(growth_history):
    db = firestore.client()
    growth_history_ref = db.collection('growth_history')
    growth_history_ref.add({
        'plant_id': growth_history.plant.id,
        'date': growth_history.date,
        'growth_stage': growth_history.growth_stage,
        'timestamp': firestore.SERVER_TIMESTAMP
    })

def save_notification_to_firestore(user_id, title, body):
    db = firestore.client()
    notifications_ref = db.collection('notifications')
    notifications_ref.add({
        'user_id': user_id,
        'title': title,
        'body': body,
        'timestamp': firestore.SERVER_TIMESTAMP
    })

from firebase_admin import messaging


def send_firebase_notification(user_token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=user_token,
    )
    response = messaging.send(message)
    return response

def get_notifications_from_firestore(user_id):
    db = firestore.client()
    notifications_ref = db.collection('notifications')
    notifications = notifications_ref.where('user_id', '==', user_id).get()
    return [{
        'id': doc.id,
        'data': doc.to_dict()
    } for doc in notifications]



