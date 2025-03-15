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
            - "address": the complete address of the person, including street, city, state/province, postal code, and country if provided. It should be in the format "Street, City, State, Postal Code, Country".
            - "rate": the electricity rate in currency per kWh.
            

            Ensure that the extracted information is accurate and matches the schema provided.

            Example Schema:
            {
            "name": "John Doe",
            "address": "1234 Elm Street, Springfield, IL, 62704, USA"
            "rate": 0.12,
            }

            Output the result in JSON format only.
            Make sure that there are no Illegal trailing comma before end of object.
            Do not include any additional text or explanation.

            Input Text:
            '''
        )

prompts = Prompts()