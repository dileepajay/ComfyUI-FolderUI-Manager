
class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __eq__(self, _) -> bool:
        return True

    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")

import torch
import numpy as np
from PIL import Image
import folder_paths
import os

class node_save:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image_type": (["input", "temp", "output"], {"default": "output"}),
                "save_path": ("STRING", {"default": ""}),
                "save_data": (any, {"forceInput": True})
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }
 
    RETURN_TYPES = ()  # No outputs
    OUTPUT_NODE = True 
    FUNCTION = "execute"
    
    def get_dir_by_type(self, dir_type):
        """Returns the corresponding directory path based on the selected image type."""
        if dir_type is None:
            dir_type = "input"

        if dir_type == "input":
            return folder_paths.get_input_directory(), "input"
        elif dir_type == "temp":
            return folder_paths.get_temp_directory(), "temp"
        elif dir_type == "output":
            return folder_paths.get_output_directory(), "output"

        return None, None
    
    def execute(self, image_type,save_path,save_data, unique_id=None, extra_pnginfo=None):
        upload_dir, image_upload_type = self.get_dir_by_type(image_type)
        img_path = os.path.normpath(os.path.join(upload_dir, save_path))
        print_data=f'sync_name:{save_path}\tsave_data:{save_data}\timg_path:{img_path}'
       # print(print_data)
        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        self.save_tensor_as_image(save_data,img_path)
        return ()
    
    def save_tensor_as_image(self,tensor, filename="abc.png"):
        # Remove batch dimension if present
        if len(tensor.shape) == 4:
            tensor = tensor[0]  # Shape now: (H, W, C)

        # Convert to NumPy array
        np_image = tensor.numpy()

        # Scale to 0-255 if necessary
        np_image = np.clip(np_image * 255, 0, 255).astype(np.uint8)

        # Convert to PIL image
        image = Image.fromarray(np_image)

        # Save image
        image.save(filename)
        print(f"Image saved as {filename}")
