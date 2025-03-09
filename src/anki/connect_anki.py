from datetime import datetime

import requests
from PIL.Image import Image
from requests.exceptions import ConnectionError

from src.utils.image_processing import encode_pil_image

from .config import ADD_NOTE_REQUEST_BODY, HOST_PORT
from .response_status import ResponseStatus


class Anki:
    """
    This class is used to communicate with AnkiConnect plugin and add new notes to the chosen deck.
    To use it AnkiConnect Add-on plugin is required.
    """

    def __init__(self):
        self.host_port = HOST_PORT

    @staticmethod
    def validate_response(data: dict) -> ResponseStatus:
        if (
            data.get("error", 0) == 0
        ):  # no error field, if error is missing it will become 0, if error is None everything is all right
            print("response is missing required error field")
            return ResponseStatus.MISSING_ERROR_FIELD
        elif data.get("result", 0) == 0:
            print("response is missing required result field")
            return ResponseStatus.MISSING_RESULT_FIELD
        elif data["error"]:
            print(data["error"])
            return ResponseStatus.ERROR_REPORTED
        return ResponseStatus.SUCCESS

    def get_decks(self) -> list[str]:
        data = {"action": "deckNames", "version": 6}
        try:
            response = requests.post(self.host_port, json=data)
            if response.status_code == 405:
                print(
                    "8765 Port is in use by another program. Please check that you have anki opened and AnkiConnect installed."
                )
            data = response.json()

        except ConnectionError as err:
            print(f"Error: {err}")
            return []

        status = self.validate_response(data)
        if status != ResponseStatus.SUCCESS:
            return []
        return data["result"]

    def add_note(self, deck: str, img: Image, answer: str) -> ResponseStatus:
        current_date = datetime.now()
        filename = f"{current_date.strftime('%Y%m%d%H%M%S')}.jpg"
        base64_data = encode_pil_image(img)
        request_data = ADD_NOTE_REQUEST_BODY

        answer = answer.replace("\n", "<br>")  # anki require <br> for new line

        # update default request body template for adding new notes
        request_data["params"]["note"]["deckName"] = deck
        request_data["params"]["note"]["picture"][0]["filename"] = filename
        request_data["params"]["note"]["picture"][0]["data"] = base64_data
        request_data["params"]["note"]["fields"]["Back"] = answer

        # ADD back information from the field

        # make request to add new note
        try:
            response = requests.post(self.host_port, json=request_data)
        except ConnectionError as err:
            print(f"Error: {err}")
            return ResponseStatus.ERROR_REPORTED

        status = self.validate_response(response.json())
        return status
