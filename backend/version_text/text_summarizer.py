import nltk
from nltk.tokenize import sent_tokenize
from flask import Flask, request, jsonify
from transformers import T5Tokenizer, T5ForConditionalGeneration

nltk.download('punkt')

app = Flask(__name__)

def preprocess_text(text):
    # Tokenization
    sentences = sent_tokenize(text.lower())
    return sentences

def summarize_text(text):
    # Preprocess text
    sentences = preprocess_text(text)

    # Concatenate sentences to form a single string for T5 input
    input_text = " ".join(sentences)

    # Initialize T5 tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained("t5-small")
    model = T5ForConditionalGeneration.from_pretrained("t5-small")

    # Tokenize and summarize the input text using T5
    inputs = tokenizer.encode("summarize: " + input_text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs, max_length=1000, min_length=50, length_penalty=5.0, num_beams=10, early_stopping=True)
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return summary

@app.route('/summarize', methods=['POST'])
def summarize():
    if 'text' not in request.json:
        return jsonify({'error': 'Missing "text" parameter.'}), 400

    text = request.json['text']
    summary = summarize_text(text)
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
