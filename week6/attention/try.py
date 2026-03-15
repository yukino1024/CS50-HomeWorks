from mask import *

text = input("Text: ")

# Tokenize input
tokenizer = AutoTokenizer.from_pretrained(MODEL)
inputs = tokenizer(text, return_tensors="tf")
print(inputs["input_ids"].numpy()[0])