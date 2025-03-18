from transformers import BertTokenizer, BertForSequenceClassification
import torch

model = BertForSequenceClassification.from_pretrained('./intent_model')
tokenizer = BertTokenizer.from_pretrained('./intent_model')

model.eval()

def predict_intent(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=128)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    predicted_label = torch.argmax(outputs.logits, axis=1).item()
    
    int_to_label = {0: "show_windows", 1: "check_system_status", 2: "close_window", 3: "check_time",
                    4: "check_internet_speed", 5: "greet", 6: "exit", 7: "open_app",
                    8: "search_wikipedia", 9: "get_weather", 10: "minimize_window",
                    11: "maximize_window", 12: "read_pdf"}

    intent = int_to_label[predicted_label]
    return intent

if __name__ == "__main__":

    while (True):
        text = input("please enter input : ")
        predicted_intent = predict_intent(text)
        print(f"Predicted Intent: {predicted_intent}")
