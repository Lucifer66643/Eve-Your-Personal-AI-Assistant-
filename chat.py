import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import torch

df = pd.read_csv('dataset.csv')
df.columns = ['text', 'intent']

label_to_int = {label: i for i, label in enumerate(df['intent'].unique())}
int_to_label = {i: label for label, i in label_to_int.items()}
df['label'] = df['intent'].map(label_to_int)

train_texts, val_texts, train_labels, val_labels = train_test_split(
    df['text'].tolist(), df['label'].tolist(), test_size=0.2, random_state=42)

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

train_encodings = tokenizer(train_texts, padding=True, max_length=128)
val_encodings = tokenizer(val_texts, padding=True, max_length=128)

class IntentDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = IntentDataset(train_encodings, train_labels)
val_dataset = IntentDataset(val_encodings, val_labels)

model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(label_to_int))

training_args = TrainingArguments(
    output_dir='./results',          
    num_train_epochs=30,             
    per_device_train_batch_size=8,       
    warmup_steps=500,                
)

trainer = Trainer(
    model=model,                         
    args=training_args,                  
    train_dataset=train_dataset,         
    eval_dataset=val_dataset             
)

trainer.train()

val_preds = trainer.predict(val_dataset)
val_pred_labels = torch.argmax(torch.tensor(val_preds.predictions), axis=1)
accuracy = accuracy_score(val_labels, val_pred_labels)
print("Validation Accuracy:", accuracy)
print(classification_report(val_labels, val_pred_labels, target_names=list(label_to_int.keys())))

model.save_pretrained('./intent_model')
tokenizer.save_pretrained('./intent_model')

def predict_intent(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=128)
    outputs = model(**inputs)
    predicted_label = torch.argmax(outputs.logits, axis=1).item()
    intent = int_to_label[predicted_label]
    return intent

text = "who are you"
print("Predicted Intent:", predict_intent(text))
