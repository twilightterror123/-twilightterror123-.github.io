from ai.stable_diffusion import StableDiffusionService

class ImageService:
    def __init__(self, sd: StableDiffusionService):
        self.sd = sd

    async def generate(self, prompt: str) -> str:
        return await self.sd.generate(prompt)
