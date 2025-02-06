import json
import os
import urllib.request
from datetime import datetime
from aiohttp import web
from server import PromptServer
import folder_paths

class Upload:
    def __init__(self):
        self.app = PromptServer.instance.app  # Access Flask app instance
        self.register_routes()

    def get_dir_by_type(self,dir_type):
            if dir_type is None:
                dir_type = "input"

            if dir_type == "input":
                type_dir = folder_paths.get_input_directory()
            elif dir_type == "temp":
                type_dir = folder_paths.get_temp_directory()
            elif dir_type == "output":
                type_dir = folder_paths.get_output_directory()

            return type_dir, dir_type
        
    def register_routes(self):
        @PromptServer.instance.routes.post("/folderui/upload")
        async def folderui_upload(request):
            try:
                # Read the request data
                data = await request.post()
                
                # Extract file and path details
                imagepath = data.get('imagepath')
                uploaded_file = data.get('file')
                
                image_upload_type = data.get("type")
                upload_dir, image_upload_type = self.get_dir_by_type(image_upload_type)

                if not imagepath or not uploaded_file:
                    return web.json_response({"status": "error", "message": "Missing required fields"}, status=400)

                # Define save path
                save_path = os.path.join(upload_dir,imagepath) #f"input/{imagepath}" 
                print(f'save_path:{save_path}')

                os.makedirs(os.path.dirname(save_path), exist_ok=True)

                # Save the uploaded file
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.file.read())

                # Get file metadata
                file_size = os.path.getsize(save_path)
                file_type = uploaded_file.content_type
                timestamp = datetime.now().isoformat()

                # Response
                response_data = {
                    "status": "success",
                    "filesize": file_size,
                    "filetype": file_type,
                    "datetime": timestamp,
                    "filepath": save_path
                }

                return web.json_response(response_data, content_type='application/json')

            except Exception as e:
                return web.json_response({"status": "error", "message": str(e)}, status=500)

# Initialize the plugin when imported
Upload()
