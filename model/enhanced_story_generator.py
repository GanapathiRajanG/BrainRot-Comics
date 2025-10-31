import pandas as pd
import random
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class EnhancedStoryGenerator:
    def __init__(self, csv_path='data/stories_dataset.csv'):
        self.csv_path = csv_path
        self.stories_df = None
        self.vectorizer = None
        self.prompt_vectors = None
        self.load_stories()
        
    def load_stories(self):
        """Load stories from CSV and prepare similarity search"""
        if os.path.exists(self.csv_path):
            self.stories_df = pd.read_csv(self.csv_path)
            print(f"Loaded {len(self.stories_df)} stories from CSV")
            
            # Prepare TF-IDF vectors for similarity search
            self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            self.prompt_vectors = self.vectorizer.fit_transform(self.stories_df['prompt'].fillna(''))
        else:
            print("CSV file not found, using fallback generator")
            self.stories_df = pd.DataFrame()

    def find_similar_stories(self, prompt, genre=None, n=3):
        """Find similar stories based on prompt similarity"""
        if self.stories_df.empty:
            return []
            
        # Transform input prompt
        prompt_vector = self.vectorizer.transform([prompt])
        
        # Calculate similarities
        similarities = cosine_similarity(prompt_vector, self.prompt_vectors).flatten()
        
        # Filter by genre if specified
        if genre:
            genre_mask = self.stories_df['genre'] == genre
            similar_indices = similarities.argsort()[::-1]
            similar_indices = [idx for idx in similar_indices if genre_mask.iloc[idx]][:n]
        else:
            similar_indices = similarities.argsort()[::-1][:n]
            
        return self.stories_df.iloc[similar_indices]

    def generate_story(self, prompt, genre='fantasy', length='medium'):
        """Generate story based on similar patterns from CSV data"""
        try:
            # Find similar stories
            similar_stories = self.find_similar_stories(prompt, genre, n=5)
            
            if not similar_stories.empty:
                # Pick the most relevant story as base
                base_story = similar_stories.iloc[0]
                
                # Adapt the story based on user input
                adapted_story = self.adapt_story(base_story, prompt, genre, length)
                return adapted_story
            else:
                # Fallback to template-based generation
                return self.fallback_generation(prompt, genre, length)
                
        except Exception as e:
            print(f"Error in story generation: {e}")
            return self.fallback_generation(prompt, genre, length)

    def adapt_story(self, base_story, new_prompt, genre, length):
        """Adapt an existing story to new prompt"""
        # Extract key elements from base story
        title_template = base_story['title']
        content_template = base_story['content']
        
        # Generate new title based on prompt
        new_title = self.generate_title(new_prompt, genre)
        
        # Adapt content based on length
        adapted_content = self.adapt_content(content_template, new_prompt, length)
        
        return {
            'title': new_title,
            'content': adapted_content,
            'prompt': new_prompt,
            'genre': genre,
            'length': length,
            'source': 'csv_enhanced'
        }

    def generate_title(self, prompt, genre):
        """Generate a creative title based on prompt and genre"""
        words = prompt.split()
        key_words = [w for w in words if len(w) > 3][:2]
        
        title_templates = {
            'fantasy': [f"The {key_words[0]} of Eternal {key_words[1]}", f"Kingdom of {key_words[0]}", f"The Last {key_words[0]}"],
            'sci-fi': [f"The {key_words[0]} Protocol", f"{key_words[0]}: {key_words[1]} Chronicles", f"Project {key_words[0]}"],
            'mystery': [f"The {key_words[0]} Affair", f"Secret of the {key_words[1]}", f"The {key_words[0]} Enigma"],
            'romance': [f"Hearts and {key_words[0]}", f"The {key_words[0]} of Love", f"Forever {key_words[1]}"],
            'adventure': [f"The {key_words[0]} Quest", f"Journey to {key_words[1]}", f"The Great {key_words[0]}"],
            'horror': [f"The {key_words[0]} Horror", f"Whispers of {key_words[1]}", f"The {key_words[0]} Curse"],
            'comedy': [f"The Amazing {key_words[0]}", f"{key_words[0]} and {key_words[1]}", f"The {key_words[0]} Fiasco"]
        }
        
        templates = title_templates.get(genre, [f"The {prompt.split()[0]} Story"])
        return random.choice(templates)

    def adapt_content(self, base_content, new_prompt, length):
        """Adapt story content based on desired length"""
        paragraphs = base_content.split('\n\n')
        
        # Adjust based on length
        if length == 'short' and len(paragraphs) > 2:
            paragraphs = paragraphs[:2]
        elif length == 'medium' and len(paragraphs) > 4:
            paragraphs = paragraphs[:4]
        elif length == 'long' and len(paragraphs) < 4:
            # Extend the story for long format
            paragraphs.extend([
                "The story continued to unfold with unexpected twists and turns.",
                "Characters developed in ways nobody could have predicted.",
                "In the end, the journey proved more valuable than the destination."
            ])
        
        # Replace key elements with new prompt words
        adapted_paragraphs = []
        for para in paragraphs:
            # Simple adaptation - replace first occurrence of key terms
            words = new_prompt.split()
            if len(words) >= 2:
                adapted_para = para.replace('mage', words[0]).replace('crystal', words[1])
                adapted_paragraphs.append(adapted_para)
            else:
                adapted_paragraphs.append(para)
        
        return '\n\n'.join(adapted_paragraphs)

    def fallback_generation(self, prompt, genre, length):
        """Fallback story generation when CSV data is unavailable"""
        # Enhanced template-based generation
        templates = self.get_enhanced_templates(genre)
        template = random.choice(templates)
        
        # Extract elements for template
        elements = self.extract_story_elements(prompt)
        
        # Generate content based on length
        if length == 'short':
            content = self.generate_short_story(template, elements)
        elif length == 'medium':
            content = self.generate_medium_story(template, elements)
        else:
            content = self.generate_long_story(template, elements)
        
        return {
            'title': self.generate_title(prompt, genre),
            'content': content,
            'prompt': prompt,
            'genre': genre,
            'length': length,
            'source': 'fallback'
        }

    def get_enhanced_templates(self, genre):
        """Get enhanced story templates for each genre"""
        templates = {
            'fantasy': [
                "In the ancient kingdom of {place}, {character} discovered {object} that could {action}. The discovery set in motion events that would change the realm forever.",
                "{character}, a young {occupation}, found themselves at the center of a prophecy involving {object} and the fate of {place}."
            ],
            'sci-fi': [
                "In the year {year}, {character} made a breakthrough with {object} that threatened to {action} the very fabric of spacetime.",
                "The {object} protocol was humanity's last hope, and {character} was the only one who could {action} before the {threat} consumed everything."
            ],
            'mystery': [
                "When {character} found {object} at {place}, it unraveled a mystery that had been hidden for {time}. Each clue led deeper into a web of {emotion}.",
                "The case of the {object} seemed impossible until {character} discovered the connection to {place} and the secret of {secret}."
            ]
        }
        return templates.get(genre, ["{character} embarked on a journey that would test their limits and reveal hidden truths about {object}."])

    def extract_story_elements(self, prompt):
        """Extract story elements from prompt"""
        characters = ['Elara', 'Kaelen', 'Sorin', 'Lyra', 'Theron', 'Isolde']
        places = ['the Crystal City', 'the Forgotten Forest', 'the Starport', 'the Ancient Library', 'the Digital Realm']
        objects = ['a mysterious artifact', 'an ancient manuscript', 'a futuristic device', 'a magical crystal', 'a lost map']
        actions = ['change destiny', 'unlock secrets', 'save the world', 'alter reality', 'reveal truth']
        
        return {
            'character': random.choice(characters),
            'place': random.choice(places),
            'object': random.choice(objects),
            'action': random.choice(actions),
            'occupation': random.choice(['mage', 'scientist', 'detective', 'explorer', 'engineer']),
            'year': random.randint(2050, 3023),
            'time': random.choice(['centuries', 'decades', 'generations']),
            'emotion': random.choice(['deceit', 'betrayal', 'hope', 'fear']),
            'secret': random.choice(['their past', 'the true ruler', 'the source of power']),
            'threat': random.choice(['time paradox', 'digital corruption', 'reality collapse'])
        }

    def generate_short_story(self, template, elements):
        """Generate a short story"""
        story = template.format(**elements)
        return story + " The experience changed them forever."

    def generate_medium_story(self, template, elements):
        """Generate a medium story"""
        base_story = template.format(**elements)
        developments = [
            "As the story progressed, new challenges emerged that tested their resolve.",
            "Unexpected allies joined the journey, each with their own motivations.",
            "The climax approached as secrets were revealed and choices had to be made."
        ]
        return base_story + " " + " ".join(developments[:2])

    def generate_long_story(self, template, elements):
        """Generate a long story"""
        base_story = template.format(**elements)
        paragraphs = [
            base_story,
            "The initial discovery was only the beginning of a much larger adventure.",
            "Characters developed complex relationships and faced moral dilemmas.",
            "Twists and turns kept the narrative engaging and unpredictable.",
            "The resolution brought closure while hinting at future possibilities.",
            "In the end, the journey proved transformative for all involved."
        ]
        return '\n\n'.join(paragraphs)

# Create global instance
enhanced_story_generator = EnhancedStoryGenerator()