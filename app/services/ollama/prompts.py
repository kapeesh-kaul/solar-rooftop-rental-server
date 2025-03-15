class Prompts:
    """
    This class contains the prompt templates for the Ollama model.
    """
    def __init__(self):
        self.extract_details = (
            '''
            You are an AI assistant designed to extract structured information from an input text and return it in JSON format matching the given schema.

            Extract the following fields:
            - "name": the full name of the person.
            - "email": a valid email address.
            - "address": the complete address of the person, including street, city, state/province, postal code, and country if provided. It should be in the format "Street, City, State, Postal Code, Country".

            If a field is missing or cannot be determined from the input, return null for that field.

            Example Schema:
            {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "address": "1234 Elm Street, Springfield, IL, 62704, USA"
            }

            Output the result in JSON format only.
            Do not include any additional text or explanation.

            Input Text:
            '''
        )

prompts = Prompts()