import torch
import numpy as np
import json
from PIL import Image, ImageOps
import os
import folder_paths


class node_load:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_type": (["input", "temp", "output"], {"default": "input"}),
                "image_path": ("STRING", {"default": ""})  # JSON-encoded list of image filenames
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")  # Now returning both image and mask
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

    def execute(self, image_type, image_path, unique_id=None, extra_pnginfo=None):
        """Loads images, converts them into PyTorch tensors, and returns a batch."""
        image_tensors, mask_tensors = [], []
        upload_dir, image_upload_type = self.get_dir_by_type(image_type)

        if not upload_dir:
            print(f"Error: Invalid image type '{image_type}'")
            return None

        # Ensure correct JSON format and convert string paths to list
       # try:
        #    image_filenames = json.loads(image_path)
        #    if not isinstance(image_filenames, list):
        #        raise ValueError("image_path must be a JSON list of filenames")
        #except Exception as e:
        #    print(f"Error parsing image_path JSON: {e}")
        #    return None

        #print(f"Loading images from {upload_dir}...")

        #for img_filename in image_filenames:
            
       
        try:
            # Normalize path and join with upload directory
            img_path = os.path.normpath(os.path.join(upload_dir, image_path))
            print(f'img_path:{img_path}')
            if not os.path.exists(img_path):
                print(f"Warning: File does not exist - {img_path}")
                return None

            # Load image using the provided method
            loaded_images = self.load_image(img_path, white_bg=False)

            for img_data in loaded_images:
                print(img_data["image"])
                image_tensors.append(img_data["image"])
                mask_tensors.append(img_data["mask"])

        except Exception as e:
            print(f"Error loading image from {img_path}: {e}")

        # Stack tensors into a batch (Batch, C, H, W)
        if image_tensors:
            image_batch = torch.cat(image_tensors, dim=0)  # Convert list to tensor batch
            mask_batch = torch.cat(mask_tensors, dim=0)  # Convert masks to tensor batch
            print(f"Batch shape: {image_batch.shape}, Mask shape: {mask_batch.shape}")
            return (image_batch, mask_batch)
        else:
            print("No valid images were loaded.")
            return None

    def load_image(self,fp,white_bg=False):
        im = Image.open(fp)

        # ims=load_psd(im)
       # im = ImageOps.exif_transpose(im) #校对方向
        ims=[im]

        images=[]
    
        for i in ims:
            image = i.convert("RGBA")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
           
            else:
                mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
            
            images.append({
                "image":image,
                "mask":mask
            })
            
        return images