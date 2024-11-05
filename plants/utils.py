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
