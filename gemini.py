import google.generativeai as genai

class Gemini:
    def __init__(self,  model_name):
        genai.configure(api_key="API_Key")
        self.model = genai.GenerativeModel(model_name)

    def generate_code(self, prompts):
        responses = []
        for prompt in prompts:
            response = self.model.generate_content(prompt)
            responses.append(response.text)
        return responses