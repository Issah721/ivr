import africastalking
from app.config.settings import settings

class VoiceService:
    def __init__(self):
        africastalking.initialize(settings.at_username, settings.at_api_key)
        self.voice = africastalking.Voice

    def initiate_call(self, phone_number: str):
        """
        Initiates an outbound call to the patient via Africa's Talking API.
        """
        try:
            # AT SDK expects a string for callFrom and a list for callTo
            response = self.voice.call(
                callFrom=settings.at_virtual_number,
                callTo=[phone_number]
            )
            return response
        except Exception as e:
            print(f"Error initiating call to {phone_number}: {e}")
            return None
