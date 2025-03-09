HOST_PORT = "http://127.0.0.1:8765"
ADD_NOTE_REQUEST_BODY = {
    "action": "addNote",
    "version": 6,
    "params": {
        "note": {
            "deckName": None,
            "modelName": "Basic",
            "fields": {"Front": "", "Back": None},
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
            },
            "picture": [
                {
                    "filename": None,
                    "data": None,
                    "fields": ["Front"],
                }
            ],
        }
    },
}
