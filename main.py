from cam.modes import update_image
import requests

url = "https://tsnode.stevethespacefa.repl.co"

update_image()
requests.post(url, "hi")
