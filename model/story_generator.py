import random
import json
import os

class StoryGenerator:
    def __init__(self):
        self.genres = ['fantasy', 'sci-fi', 'mystery', 'adventure', 'romance', 'comedy', 'horror']
        self.templates = self._load_templates()
    def _load_templates(self):
        return {
            'fantasy': [
                "In the kingdom of {place}, {character} discovered {object} that held the power to {action}.",
                "The ancient prophecy spoke of {character} who would {action} with the {object} in {place}.",
                "When {character} found the magical {object} in {place}, they never imagined it would {action}."
            ],
            'sci-fi': [
                "On the spaceship {place}, {character} encountered an AI that could {action} with the {object}.",
                "In the year 3023, {character} made a discovery about {object} that would {action} humanity.",
                "The alien artifact known as {object} gave {character} the ability to {action} across {place}."
            ],
            'mystery': [
                "Detective {character} found the {object} at {place}, which held the clue to {action}.",
                "The mysterious disappearance was connected to {object} that {character} discovered in {place}.",
                "When {character} investigated {place}, they uncovered {object} that would {action} the case."
            ]
        }
    
    def generate_story(self, prompt, genre='fantasy', length='medium'):
        # Extract elements from prompt
        elements = self._extract_elements(prompt)
        
        # Generate title
        title = self._generate_title(prompt, genre)
        
        # Generate content based on length
        if length == 'short':
            paragraphs = 2
        elif length == 'medium':
            paragraphs = 4
        else:  # long
            paragraphs = 6
            
        content = self._generate_content(elements, genre, paragraphs)
        
        return {
            'title': title,
            'content': content,
            'prompt': prompt,
            'genre': genre,
            'length': length
        }
    
    def _extract_elements(self, prompt):
        characters = ['Alex', 'Morgan', 'Jordan', 'Casey', 'Riley', 'Taylor']
        places = ['the ancient forest', 'the futuristic city', 'the hidden temple', 'the abandoned spaceship']
        objects = ['a mysterious crystal', 'an ancient book', 'a futuristic device', 'a magical amulet']
        actions = ['change destiny', 'unlock secrets', 'save the world', 'alter reality']
        
        return {
            'character': random.choice(characters),
            'place': random.choice(places),
            'object': random.choice(objects),
            'action': random.choice(actions)
        }
    
    def _generate_title(self, prompt, genre):
        words = prompt.split()[:3]
        base_title = ' '.join(words).title()
        
        titles = {
            'fantasy': f"The {base_title} of Destiny",
            'sci-fi': f"{base_title}: Future Chronicles",
            'mystery': f"The {base_title} Mystery",
            'adventure': f"{base_title}'s Great Adventure",
            'romance': f"The {base_title} of Love",
            'comedy': f"The Amazing {base_title}",
            'horror': f"The {base_title} Horror"
        }
        
        return titles.get(genre, f"The {base_title} Story")
    
    def _generate_content(self, elements, genre, paragraphs):
        content = []
        
        for i in range(paragraphs):
            if genre in self.templates:
                template = random.choice(self.templates[genre])
                paragraph = template.format(**elements)
            else:
                paragraph = f"{elements['character']} continued their journey in {elements['place']}."
            
            # Add some variation
            variations = [
                "Little did they know what awaited them.",
                "The adventure was only beginning.",
                "Nothing could have prepared them for what came next.",
                "The truth was more incredible than they ever imagined."
            ]
            
            if random.random() > 0.7:  # 30% chance to add variation
                paragraph += " " + random.choice(variations)
                
            content.append(paragraph)
        
        return '\n\n'.join(content)

# Create a global instance for the app to use
story_generator = StoryGenerator()