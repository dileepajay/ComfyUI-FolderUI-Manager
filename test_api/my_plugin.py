import json
 
from server import PromptServer
from aiohttp import web
import aiohttp
import json
import zipfile
import urllib.request

class MyCustomRoutes:
    def __init__(self):
        self.app = PromptServer.instance.app  # Access Flask app instance
        self.register_routes()

    def register_routes(self):
        @PromptServer.instance.routes.get("/custom_endpoint")
        def custom_endpoint(request):
            message = request.rel_url.query["message"]
            js={"status": "success", "received_message": message}
            return web.json_response(js, content_type='application/json')
           

# Initialize the plugin when imported
MyCustomRoutes()
