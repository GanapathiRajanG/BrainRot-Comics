import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Embedding, Dropout, concatenate
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import json
import pickle
import os

class StoryGeneratorModel:
    def __init__(self, vocab_size=10000, max_sequence_length=50, embedding_dim=100, lstm_units=256):
        self.vocab_size = vocab_size
        self.max_sequence_length = max_sequence_length
        self.embedding_dim = embedding_dim
        self.lstm_units = lstm_units
        self.tokenizer = None
        self.model = None
        self.genre_mapping = {
            'fantasy': 0, 'sci-fi': 1, 'mystery': 2, 'adventure': 3,
            'romance': 4, 'comedy': 5, 'horror': 6
        }
        self.length_mapping = {
            'short': 0, 'medium': 1, 'long': 2
        }

    def build_model(self):
        # Prompt input
        prompt_input = Input(shape=(self.max_sequence_length,), name='prompt_input')
        prompt_embedding = Embedding(self.vocab_size, self.embedding_dim)(prompt_input)
        prompt_lstm = LSTM(self.lstm_units, return_sequences=False)(prompt_embedding)
        
        # Genre input
        genre_input = Input(shape=(1,), name='genre_input')
        genre_embedding = Embedding(7, 10)(genre_input)
        genre_embedding = tf.keras.layers.Flatten()(genre_embedding)
        
        # Length input
        length_input = Input(shape=(1,), name='length_input')
        length_embedding = Embedding(3, 5)(length_input)
        length_embedding = tf.keras.layers.Flatten()(length_embedding)
        
        # Concatenate all inputs
        concatenated = concatenate([prompt_lstm, genre_embedding, length_embedding])
        
        # Dense layers
        dense1 = Dense(512, activation='relu')(concatenated)
        dropout1 = Dropout(0.3)(dense1)
        dense2 = Dense(256, activation='relu')(dropout1)
        dropout2 = Dropout(0.3)(dense2)
        
        # Output layers for title and content
        title_output = Dense(self.vocab_size, activation='softmax', name='title_output')(dropout2)
        content_output = Dense(self.vocab_size, activation='softmax', name='content_output')(dropout2)
        
        self.model = Model(
            inputs=[prompt_input, genre_input, length_input],
            outputs=[title_output, content_output]
        )
        
        self.model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return self.model

    def preprocess_data(self, data):
        prompts = [item['prompt'] for item in data]
        genres = [self.genre_mapping[item['genre']] for item in data]
        lengths = [self.length_mapping[item['length']] for item in data]
        titles = [item['title'] for item in data]
        contents = [item['content'] for item in data]
        
        # Fit tokenizer on all text
        all_text = prompts + titles + contents
        self.tokenizer = Tokenizer(num_words=self.vocab_size, oov_token='<OOV>')
        self.tokenizer.fit_on_texts(all_text)
        
        # Convert to sequences
        prompt_sequences = self.tokenizer.texts_to_sequences(prompts)
        title_sequences = self.tokenizer.texts_to_sequences(titles)
        content_sequences = self.tokenizer.texts_to_sequences(contents)
        
        # Pad sequences
        X_prompt = pad_sequences(prompt_sequences, maxlen=self.max_sequence_length, padding='post')
        X_genre = np.array(genres).reshape(-1, 1)
        X_length = np.array(lengths).reshape(-1, 1)
        
        # For training, we'll use the same input for both outputs (simplified approach)
        y_title = pad_sequences(title_sequences, maxlen=self.max_sequence_length, padding='post')
        y_content = pad_sequences(content_sequences, maxlen=self.max_sequence_length * 3, padding='post')
        
        return [X_prompt, X_genre, X_length], [y_title, y_content]

    def train(self, data, epochs=10, batch_size=32, validation_split=0.2):
        X, y = self.preprocess_data(data)
        
        history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=1
        )
        
        return history

    def save_model(self, model_path='model/trained_model/story_model.h5', tokenizer_path='model/trained_model/tokenizer.pickle'):
        if not os.path.exists('model/trained_model'):
            os.makedirs('model/trained_model')
            
        self.model.save(model_path)
        
        with open(tokenizer_path, 'wb') as handle:
            pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_model(self, model_path='model/trained_model/story_model.h5', tokenizer_path='model/trained_model/tokenizer.pickle'):
        self.model = tf.keras.models.load_model(model_path)
        
        with open(tokenizer_path, 'rb') as handle:
            self.tokenizer = pickle.load(handle)

    def generate_story(self, prompt, genre, length):
        if self.model is None or self.tokenizer is None:
            raise Exception("Model not loaded. Please load the model first.")
        
        # Preprocess inputs
        prompt_sequence = self.tokenizer.texts_to_sequences([prompt])
        prompt_padded = pad_sequences(prompt_sequence, maxlen=self.max_sequence_length, padding='post')
        
        genre_encoded = np.array([[self.genre_mapping[genre]]])
        length_encoded = np.array([[self.length_mapping[length]]])
        
        # Generate predictions
        title_pred, content_pred = self.model.predict([prompt_padded, genre_encoded, length_encoded])
        
        # Convert predictions to text
        title = self._sequence_to_text(title_pred[0])
        content = self._sequence_to_text(content_pred[0])
        
        return {
            'title': title,
            'content': content,
            'prompt': prompt,
            'genre': genre,
            'length': length
        }

    def _sequence_to_text(self, sequence):
        # Convert probability sequence to text
        word_indices = np.argmax(sequence, axis=-1)
        words = []
        
        for idx in word_indices:
            if idx > 0 and idx < self.vocab_size:
                word = self.tokenizer.index_word.get(idx, '')
                if word:
                    words.append(word)
        
        return ' '.join(words)

def train_model():
    # Load synthetic data
    with open('data/training_data.json', 'r') as f:
        data = json.load(f)
    
    # Initialize and train model
    model = StoryGeneratorModel()
    model.build_model()
    
    print("Training model...")
    history = model.train(data, epochs=5, batch_size=32)
    
    # Save model
    model.save_model()
    print("Model trained and saved successfully!")
    
    return model, history

if __name__ == "__main__":
    train_model()