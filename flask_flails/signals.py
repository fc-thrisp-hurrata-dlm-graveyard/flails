import blinker

signals = blinker.Namespace()

app_created_successfully = signals.signal("flails-app-created-successfully")
