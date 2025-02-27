import base64
from io import BytesIO
from typing import TYPE_CHECKING, cast

import customtkinter as ctk
from dotenv import dotenv_values
from openai import OpenAI
from PIL.Image import Image
from pytesseract import image_to_string

if TYPE_CHECKING:
    from main import App
from settings import PROMPT_EXPLANATION, Colors, Fonts, Geometry


class SolutionButton(ctk.CTkButton):
    def __init__(
        self, parent: ctk.CTkFrame, text: str, image: Image, main_window: "App"
    ):
        super().__init__(
            master=parent,
            text=text,
            command=self.generate_solution,
            fg_color=Colors.BUTTON,
            hover_color=Colors.BUTTON_HOVER,
            font=ctk.CTkFont(
                family=Fonts.ANSWER,
                size=Fonts.ANSWER_SIZE,
                weight="bold",
            ),
            corner_radius=Geometry.CORNER_RADIUS,
        )
        self.main_window = main_window
        self.image = image
        # .env file - API KEY for OpenRuoter
        self.api_key = dotenv_values(".env")["API_KEY"]

        self.place(
            rely=0.9,
            relx=0,
            relheight=0.1,
            relwidth=1,
        )

    def encode_pil_image(self, pil_image: Image) -> str:
        """
        Encode a PIL Image object to base64 without saving to disk

        Args:
            pil_image (PIL.Image.Image): The PIL Image object to encode

        Returns:
            str: Base64 encoded string of the image
        """
        buffered = BytesIO()
        # You can specify the format and quality here
        pil_image.convert("RGB").save(buffered, format="JPEG")
        # Get the byte data and encode it
        img_bytes = buffered.getvalue()
        return base64.b64encode(img_bytes).decode("utf-8")

    def generate_solution(self):
        # # change image to text
        # text = image_to_string(
        #     image=self.image,
        #     lang="pol",
        # )

        # prompt = f'{PROMPT_EXPLANATION}\nPytanie załączyłem jako tekst: "{text}"'
        prompt = f"{PROMPT_EXPLANATION}\nPytanie załączyłem jako zdjęcie."
        base64_string = self.encode_pil_image(cast(Image, self.image))
        correct_answer = self.chatbot(prompt, base64_string)

        # showing solution
        if self.main_window.provide_solution(correct_answer):
            # the solution was correctly generated so we can add export settings and delete this button
            self.main_window.export_settings_section(self.image)

            self.place_forget()

    def chatbot(self, prompt: str, base64_img: str | None = None) -> str | None:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
        if base64_img:
            content = [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"},
                },
            ]
        else:
            content = prompt

        completion = client.chat.completions.create(
            model="google/gemini-exp-1206:free",
            messages=[{"role": "user", "content": content}],
            temperature=0.7,
            top_p=0.5,
        )
        return completion.choices[0].message.content
