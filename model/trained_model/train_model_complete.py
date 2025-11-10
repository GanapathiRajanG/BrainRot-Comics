import tensorflow as tf
import numpy as np
import json
import pickle
import os
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Embedding, Dropout, concatenate
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

class CompleteStoryGeneratorModel:
    def __init__(self, vocab_size=5000, max_sequence_length=30, embedding_dim=64, lstm_units=128):
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
        genre_embedding = Embedding(7, 8)(genre_input)
        genre_embedding = tf.keras.layers.Flatten()(genre_embedding)
        
        # Length input
        length_input = Input(shape=(1,), name='length_input')
        length_embedding = Embedding(3, 4)(length_input)
        length_embedding = tf.keras.layers.Flatten()(length_embedding)
        
        # Concatenate all inputs
        concatenated = concatenate([prompt_lstm, genre_embedding, length_embedding])
        
        # Dense layers
        dense1 = Dense(256, activation='relu')(concatenated)
        dropout1 = Dropout(0.3)(dense1)
        dense2 = Dense(128, activation='relu')(dropout1)
        dropout2 = Dropout(0.3)(dense2)
        
        # Output layers
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
        
        print("Model built successfully!")
        return self.model

    def create_synthetic_training_data(self, num_samples=1000):
        """Create simple synthetic training data for demonstration"""
        prompts = []
        titles = []
        contents = []
        genres = []
        lengths = []
        
        story_elements = {
            'characters': ['Alex', 'Morgan', 'Jordan', 'Casey', 'Riley'],
            'actions': ['discovers', 'finds', 'creates', 'solves', 'explores'],
            'objects': ['magic', 'secret', 'mystery', 'power', 'truth'],
            'places': ['forest', 'city', 'mountain', 'ocean', 'desert']
        }
        
        for i in range(num_samples):
            char = np.random.choice(story_elements['characters'])
            action = np.random.choice(story_elements['actions'])
            obj = np.random.choice(story_elements['objects'])
            place = np.random.choice(story_elements['places'])
            genre = np.random.choice(list(self.genre_mapping.keys()))
            length = np.random.choice(list(self.length_mapping.keys()))
            
            prompt = f"{char} {action} {obj} in the {place}"
            title = f"The {obj} of {place}"
            
            # Simple content generation
            if length == 'short':
                content = f"{char} found something amazing in the {place}. It was a {obj} that changed everything."
            elif length == 'medium':
                content = f"{char} had always been curious about the {place}. When they found the {obj}, their life transformed. The {obj} held powers nobody understood."
            else:
                content = f"{char}'s journey began in the mysterious {place}. The discovery of the {obj} was just the start. Little did they know that this {obj} would lead to incredible adventures and life-changing experiences."
            
            prompts.append(prompt)
            titles.append(title)
            contents.append(content)
            genres.append(genre)
            lengths.append(length)
        
        return {
            'prompts': prompts,
            'titles': titles,
            'contents': contents,
            'genres': genres,
            'lengths': lengths
        }

    def preprocess_data(self, data):
        prompts = data['prompts']
        genres = [self.genre_mapping[g] for g in data['genres']]
        lengths = [self.length_mapping[l] for l in data['lengths']]
        titles = data['titles']
        contents = data['contents']
        
        # Fit tokenizer
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
        
        # For this simplified version, we'll use the same target for both outputs
        y_title = pad_sequences(title_sequences, maxlen=10, padding='post')
        y_content = pad_sequences(content_sequences, maxlen=50, padding='post')
        
        return [X_prompt, X_genre, X_length], [y_title, y_content]

    def train(self, epochs=5, batch_size=32):
        print("Generating training data...")
        data = self.create_synthetic_training_data(1000)
        
        print("Preprocessing data...")
        X, y = self.preprocess_data(data)
        
        print("Starting training...")
        history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            verbose=1
        )
        
        return history

    def save_model(self, model_path='model/trained_model/story_model.h5', tokenizer_path='model/trained_model/tokenizer.pickle'):
        if not os.path.exists('model/trained_model'):
            os.makedirs('model/trained_model')
            
        self.model.save(model_path)
        
        with open(tokenizer_path, 'wb') as handle:
            pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
        print(f"Model saved to {model_path}")
        print(f"Tokenizer saved to {tokenizer_path}")

    def load_model(self, model_path='model/trained_model/story_model.h5', tokenizer_path='model/trained_model/tokenizer.pickle'):
        if os.path.exists(model_path):
            self.model = tf.keras.models.load_model(model_path)
            
            with open(tokenizer_path, 'rb') as handle:
                self.tokenizer = pickle.load(handle)
            
            print("Model loaded successfully!")
            return True
        else:
            print("Model file not found!")
            return False

    def generate_story(self, prompt, genre, length):
        if self.model is None or self.tokenizer is None:
            raise Exception("Model not loaded. Please load or train the model first.")
        
        # Preprocess inputs
        prompt_sequence = self.tokenizer.texts_to_sequences([prompt])
        prompt_padded = pad_sequences(prompt_sequence, maxlen=self.max_sequence_length, padding='post')
        
        genre_encoded = np.array([[self.genre_mapping[genre]]])
        length_encoded = np.array([[self.length_mapping[length]]])
        
        # Generate predictions
        title_pred, content_pred = self.model.predict([prompt_padded, genre_encoded, length_encoded], verbose=0)
        
        # Convert predictions to text
        title = self._sequence_to_text(title_pred[0])
        content = self._sequence_to_text(content_pred[0])
        
        return {
            'title': title if title else f"The {genre.title()} Adventure",
            'content': content if content else f"This is a story about {prompt}. In the world of {genre}, anything is possible.",
            'prompt': prompt,
            'genre': genre,
            'length': length
        }

    def _sequence_to_text(self, sequence):
        word_indices = np.argmax(sequence, axis=-1)
        words = []
        
        for idx in word_indices:
            if idx > 0 and idx < self.vocab_size:
                word = self.tokenizer.index_word.get(idx, '')
                if word and word != '<OOV>':
                    words.append(word)
        
        return ' '.join(words) if words else ""

def main():
    # Create and train the model
    model = CompleteStoryGeneratorModel()
    model.build_model()
    
    print("Training the model...")
    history = model.train(epochs=3)  # Reduced epochs for faster training
    
    # Save the model
    model.save_model()
    
    # Test the model
    print("\nTesting the model...")
    test_story = model.generate_story(
        prompt="A robot who falls in love with a human",
        genre="sci-fi",
        length="medium"
    )
    
    print(f"Title: {test_story['title']}")
    print(f"Content: {test_story['content']}")

if __name__ == "__main__":
    main()