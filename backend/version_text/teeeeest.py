import nltk
from nltk.tokenize import sent_tokenize
from flask import Flask, request, jsonify
from transformers import T5Tokenizer, T5ForConditionalGeneration

import subprocess



def call_script2():
    try:
        # Call the second script using subprocess.run()
        subprocess.run(["python", "text_summarizer.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while calling script2.py: {e}")

def add_numbers():
    text = "On a $50,000 mortgage of 30 years at 8 percent, the monthly payment would be $366.88."
    sentences = sent_tokenize(text.lower())
    print("ssssss")
    return text

result = add_numbers()
print("hhhhhhhhhhhh", result)
call_script2()
