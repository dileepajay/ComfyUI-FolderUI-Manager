import os
import mimetypes
import re
from aiohttp import web
from server import PromptServer
import folder_paths

class ViewFile:
    def __init__(self):
        self.app = PromptServer.instance.app  # Access Flask app instance
        self.register_routes()

    def get_dir_by_type(self, dir_type):
        if dir_type is None:
            dir_type = "output"

        if dir_type == "input":
            type_dir = folder_paths.get_input_directory()
        elif dir_type == "temp":
            type_dir = folder_paths.get_temp_directory()
        elif dir_type == "output":
            type_dir = folder_paths.get_output_directory()
        else:
            raise ValueError("Invalid directory type")
        
        return type_dir, dir_type

    def register_routes(self):
        @PromptServer.instance.routes.get('/folderui/view')
        @PromptServer.instance.routes.get('/folderui/view/')
        @PromptServer.instance.routes.get('/folderui/view/{workspace_path:.+}')
        async def route_serve_workspace(request):
            workspace_path = request.match_info.get("workspace_path", "")
            components = re.split(r'[\\/]', workspace_path)
            
            if not components or len(components) < 1:
                return web.json_response({"status": "error", "message": "Invalid workspace path"}, status=400)
            
            base_folder = components[0]
            component_A = "/".join(components[1:-1]) if len(components) > 1 else ""
            component_B = components[-1] if len(components) > 1 else ""
            print(f'base_folder:{base_folder}')
            print(f'component_A:{component_A}')
            print(f'component_B:{component_B}')
            try:
                upload_dir, dir_type = self.get_dir_by_type(base_folder)
            except ValueError as e:
                return web.json_response({"status": "error", "message": str(e)}, status=400)
            
            view_path = os.path.join(upload_dir, component_A, component_B) if component_A else os.path.join(upload_dir, component_B)
            
            print(f'view_path: {view_path}')
            
            return web.FileResponse(view_path, headers={"Content-Type": self.get_file_type(component_B)})
    
    def get_file_type(self, file_path):
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        if ext in [".html", ".htm"]:
            return "text/html"
        elif ext == ".css":
            return "text/css"
        elif ext == ".js":
            return "application/javascript"
        elif ext in [".jpg", ".jpeg"]:
            return "image/jpeg"
        elif ext == ".png":
            return "image/png"
        elif ext == ".mp4":
            return "video/mp4"
        elif ext == ".json":
            return "application/json"
        elif ext == ".txt":
            return "text/plain"
        else:
            return "application/octet-stream"
 
ViewFile()