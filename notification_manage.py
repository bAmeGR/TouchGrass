from plyer import notification
import winsound
import os

def show_notification(title, message, sound_enabled=True):
    notification.notify(
        title=title,
        message=message,
        timeout=10,
        app_name="Touch Grass"
    )
    if sound_enabled:
        try:
            if os.path.exists('sounds/notification.wav'):
                winsound.PlaySound('sounds/notification.wav', winsound.SND_FILENAME)
            else:
                # Fallback to system sound
                winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        except Exception as e:
            print(f"Sound error: {e}")