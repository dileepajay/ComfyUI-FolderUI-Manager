
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

class folderui_sync:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "sync_name": ("STRING", {"default": ""}),
                "sync_data": (any, {"forceInput": True}),
                "sync_ip": ("STRING", {"default": ""}),
                "sync_port": ("INT", {"default": 8082}),
                "sync_auth": ("STRING", {"default": ""}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }
 
    RETURN_TYPES = ()  # No outputs
    OUTPUT_NODE = True 
    FUNCTION = "execute"
    
    def execute(self, sync_name,sync_data,sync_ip,sync_port,sync_auth, unique_id=None, extra_pnginfo=None):
        print_data=f'sync_name:{sync_name}\tsync_data:{sync_data}\tsync_ip:{sync_ip}\tsync_port:{sync_port}\tsync_auth:{sync_auth}'
        print(print_data)
        self.save_tensor_as_image(sync_data,'C:/Users/medre/OneDrive/Desktop/aaa.png')
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
