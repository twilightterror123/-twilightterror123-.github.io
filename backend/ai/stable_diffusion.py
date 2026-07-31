from diffusers import StableDiffusionPipeline
import torch
import base64
from io import BytesIO

class StableDiffusionService:
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5", device="cpu"):
        self.device = device
        self.pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
        self.pipe.to(device)
        if device == "cuda":
            self.pipe.enable_attention_slicing()

    async def generate(self, prompt: str) -> str:
        image = self.pipe(prompt).images[0]
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
