import google.generativeai as genai

class Gemini:
    def __init__(self, model_name):
        genai.configure(api_key="YAIzaSyC_ArUx14IiC7Fo2Z1TlFQ-_QmBbi2HdM4")  # Replace with your actual API key
        self.model = genai.GenerativeModel(model_name)

    def generate_code(self, prompts):
        responses = []
        for prompt in prompts:
            full_prompt = f"You are Eve. Eve is a personal AI assistant developed by Yadnit. " \
                          f"Eve is dedicated to assisting Yadnit with a wide range of tasks. " \
                          f"Eve's responses are tailored to Yadnit's needs and preferences. " \
                          f"Make answers as short as possible unless asked in detail. {prompt}"
            response = self.model.generate_content(full_prompt)
            responses.append(response.text)
        return responses

def run_gemini_model(user_prompts):
    gemini = Gemini(model_name='models/gemini-1.5-pro-latest')  # or 'models/gemini-1.5-flash-latest'
    return gemini.generate_code(user_prompts)

if __name__ == "__main__":
    user_prompts = ["Write a Python function to add two numbers.", "Explain the importance of data privacy."]
    responses = run_gemini_model(user_prompts)
    for response in responses:
        print(response)
