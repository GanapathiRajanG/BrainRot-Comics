import json
import random
from datetime import datetime

class SyntheticDataGenerator:
    def __init__(self):
        self.genres = ['fantasy', 'sci-fi', 'mystery', 'adventure', 'romance', 'comedy', 'horror']
        self.themes = {
            'fantasy': ['dragons', 'magic', 'kingdoms', 'quests', 'mythical creatures'],
            'sci-fi': ['robots', 'space', 'time travel', 'aliens', 'future technology'],
            'mystery': ['detective', 'crime', 'secrets', 'investigation', 'clues'],
            'adventure': ['exploration', 'journey', 'discovery', 'danger', 'treasure'],
            'romance': ['love', 'relationships', 'heartbreak', 'passion', 'destiny'],
            'comedy': ['humor', 'misunderstandings', 'pranks', 'situations', 'characters'],
            'horror': ['ghosts', 'fear', 'supernatural', 'darkness', 'suspense']
        }
        
        self.story_structures = {
            'short': [2, 3],
            'medium': [3, 5],
            'long': [5, 8]
        }
        
        self.characters = [
            'Alex', 'Morgan', 'Jordan', 'Casey', 'Riley', 'Taylor', 'Avery', 'Quinn',
            'Sam', 'Jamie', 'Dakota', 'Skyler', 'Peyton', 'Rowan', 'Sage', 'Finley'
        ]
        
        self.locations = [
            'ancient forest', 'futuristic city', 'hidden temple', 'abandoned spaceship',
            'magical academy', 'underground bunker', 'floating islands', 'crystal caves',
            'digital realm', 'parallel universe', 'dream world', 'time vortex'
        ]

    def generate_prompt(self, genre):
        theme = random.choice(self.themes[genre])
        character = random.choice(self.characters)
        location = random.choice(self.locations)
        
        prompts = [
            f"A {character} who discovers {theme} in the {location}",
            f"The {theme} of {character} in the {location}",
            f"When {character} finds {theme} while exploring the {location}",
            f"The secret of {theme} that {character} uncovers in the {location}",
            f"How {character}'s encounter with {theme} changes the {location} forever"
        ]
        
        return random.choice(prompts)

    def generate_story(self, prompt, genre, length):
        words = prompt.split()
        character = next((word for word in words if word in self.characters), random.choice(self.characters))
        theme = next((word for word in words if word in sum(self.themes.values(), [])), random.choice(self.themes[genre]))
        
        paragraphs = random.randint(*self.story_structures[length])
        story = []
        
        for i in range(paragraphs):
            paragraph = self._generate_paragraph(character, theme, genre, i, paragraphs)
            story.append(paragraph)
        
        title = self._generate_title(prompt, genre)
        
        return {
            'title': title,
            'content': '\n\n'.join(story),
            'prompt': prompt,
            'genre': genre,
            'length': length,
            'word_count': sum(len(para.split()) for para in story)
        }

    def _generate_paragraph(self, character, theme, genre, paragraph_num, total_paragraphs):
        if paragraph_num == 0:
            # Introduction
            openings = [
                f"In a world where {theme} shaped reality,",
                f"{character} had always been fascinated by {theme},",
                f"Little did {character} know that {theme} would change everything,",
                f"When {character} first encountered {theme}, it seemed ordinary,"
            ]
            content = f"{random.choice(openings)} they couldn't have imagined the adventure that awaited."
            
        elif paragraph_num == total_paragraphs - 1:
            # Conclusion
            endings = [
                f"And so, {character} realized that {theme} was just the beginning.",
                f"With {theme} now understood, {character} looked toward new horizons.",
                f"The mystery of {theme} had been solved, but new questions emerged.",
                f"{character} knew that their journey with {theme} was far from over."
            ]
            content = random.choice(endings)
            
        else:
            # Middle paragraphs
            developments = [
                f"As {character} delved deeper into {theme}, they discovered",
                f"The connection between {character} and {theme} grew stronger when",
                f"Unexpectedly, {theme} revealed its true nature to {character} as",
                f"{character}'s understanding of {theme} was completely transformed by"
            ]
            discoveries = [
                "a hidden truth that changed everything.",
                "an ancient power waiting to be unleashed.",
                "a secret that had been buried for centuries.",
                "a mystery that defied all explanation."
            ]
            content = f"{random.choice(developments)} {random.choice(discoveries)}"
        
        return content

    def _generate_title(self, prompt, genre):
        words = prompt.split()
        key_words = [word for word in words if word.lower() not in ['a', 'the', 'of', 'in', 'who', 'discovers', 'finds']]
        
        if len(key_words) >= 2:
            title_formats = [
                f"The {key_words[1]} of {key_words[0]}",
                f"{key_words[0]} and the {key_words[1]}",
                f"When {key_words[0]} Met {key_words[1]}",
                f"The {key_words[1]}'s {key_words[0]}"
            ]
        else:
            title_formats = [
                f"The {genre.title()} Adventure",
                f"Secrets of the {random.choice(self.themes[genre])}",
                f"{random.choice(self.characters)}'s Journey"
            ]
        
        return random.choice(title_formats)

    def generate_dataset(self, num_samples=1000):
        dataset = []
        
        for i in range(num_samples):
            genre = random.choice(self.genres)
            prompt = self.generate_prompt(genre)
            length = random.choice(['short', 'medium', 'long'])
            
            story = self.generate_story(prompt, genre, length)
            dataset.append(story)
            
            if (i + 1) % 100 == 0:
                print(f"Generated {i + 1} samples...")
        
        return dataset

    def save_dataset(self, dataset, filename='training_data.json'):
        with open(f'data/{filename}', 'w') as f:
            json.dump(dataset, f, indent=2)
        
        print(f"Dataset saved with {len(dataset)} samples")

if __name__ == "__main__":
    generator = SyntheticDataGenerator()
    dataset = generator.generate_dataset(1000)
    generator.save_dataset(dataset)