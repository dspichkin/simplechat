from apps.messages.models import Message


def send_message(thread_id, sender_id, message_text, sender_name=None):

    Message.object.create(
        text=message_text,
        thread_id=thread_id,
        sender_id=sender_id
    )
