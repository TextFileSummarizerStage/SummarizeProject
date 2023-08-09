import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from flask import Flask, request, jsonify
from transformers import T5Tokenizer, T5ForConditionalGeneration
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import re

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

def preprocess_text(input_text):
    print("Text before processing", input_text)

    # Remove special caracters
    pattern = r'[^a-zA-Z0-9\s]'
    cleaned_string = re.sub(pattern, '', input_text)

    # Remove extra whitespace, line breaks, and tabs
    cleaned_text = re.sub(r'\s+', ' ', cleaned_string).strip()

    # Tokenization
    sentences = sent_tokenize(cleaned_text.lower())
    print("Preprocessed Sentences:", sentences, flush=True)

    # Initialize stemming and lemmatization tools
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    # Apply stemming and lemmatization to sentences
    stemmed_sentences = [[stemmer.stem(word) for word in word_tokenize(sentence.lower())] for sentence in sentences]
    lemmatized_sentences = [[lemmatizer.lemmatize(word) for word in word_tokenize(sentence.lower())] for sentence in sentences]
    # Print stemmed sentences
    print("------------Stemmed Sentences:")
    for i, sentence in enumerate(stemmed_sentences):
        print(f"Sentence {i + 1}: {sentence}")
    # Print lemmatized sentences
    print("\n-------------Lemmatized Sentences:")
    for i, sentence in enumerate(lemmatized_sentences):
        print(f"Sentence {i + 1}: {sentence}")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<", stemmed_sentences)
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<", lemmatized_sentences)

    # Sentence scoring
    # def preprocess_text(text):
    #     tokens = nltk.word_tokenize(text)
    #     return ' '.join(tokens)




    return sentences


# print("Preprocessed Sentences:",preprocess_text())
def summarize_text(input_text):
    # Preprocess text
    sentences = preprocess_text(input_text)

    # Concatenate sentences to form a single string for T5 input
    input_text = " ".join(sentences)

    # Initialize T5 tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained("t5-small")
    model = T5ForConditionalGeneration.from_pretrained("t5-small")

    # Tokenize and summarize the input text using T5
    inputs = tokenizer.encode("summarize: " + input_text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs, max_length=1000, min_length=50, length_penalty=5.0, num_beams=10,
                             early_stopping=True)
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("Summary:", summary)
    return summary




if __name__ == '__main__':
    # app.run(debug=True)
    # input_text = "Under the golden rays of the setting sun, the quaint village came alive with a gentle buzz of activity. Children played joyfully in the cobblestone streets, their laughter echoing through the air. The scent of freshly baked bread wafted from the local bakery, enticing passersby to stop and indulge. Colorful flowers adorned window sills, adding a touch of charm to the rustic houses. Amidst the picturesque scene, the village seemed like a time capsule, preserving the beauty of simpler days while embracing the warmth of a tight-knit community."
    input_text = "Hello, @world! This is an example text with #special characters."
    summarized_text = summarize_text(input_text)
    print("Original Text:", input_text)
    print("Summarized Text:", summarized_text)
