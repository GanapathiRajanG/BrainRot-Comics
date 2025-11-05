import pandas as pd
import random
import os

class NarrativeStoryGenerator:
    def __init__(self, csv_path='data/stories_dataset.csv'):
        self.csv_path = csv_path
        self.stories_df = None
        self.load_stories()
        
    def load_stories(self):
        """Load stories from CSV"""
        if os.path.exists(self.csv_path):
            try:
                self.stories_df = pd.read_csv(self.csv_path)
                print(f"✅ Loaded {len(self.stories_df)} stories from CSV")
            except Exception as e:
                print(f"❌ Error loading CSV: {e}")
                self.stories_df = pd.DataFrame()
        else:
            print("❌ CSV file not found")
            self.stories_df = pd.DataFrame()

    def generate_story(self, prompt, genre='fantasy', length='medium'):
        """Generate a coherent, well-structured story"""
        try:
            # Extract key elements from prompt
            elements = self.extract_story_elements(prompt, genre)
            
            # Generate title
            title = self.generate_title(prompt, genre)
            
            # Generate structured content
            content = self.generate_structured_content(elements, genre, length)
            
            return {
                'title': title,
                'content': content,
                'prompt': prompt,
                'genre': genre,
                'length': length,
                'source': 'narrative_generator'
            }
            
        except Exception as e:
            print(f"Error in narrative generation: {e}")
            return self.create_fallback_story(prompt, genre, length)

    def extract_story_elements(self, prompt, genre):
        """Extract meaningful story elements from prompt"""
        words = prompt.lower().split()
        
        # Character names
        characters = {
            'fantasy': ['Elara', 'Kaelen', 'Sorin', 'Lyra', 'Theron', 'Isolde'],
            'sci-fi': ['Jaxon', 'Nyra', 'Kael', 'Zara', 'Roric', 'Elara'],
            'mystery': ['Detective Morgan', 'Inspector Reed', 'Agent Carter', 'Prof. Bennett'],
            'romance': ['Emma', 'Liam', 'Sophia', 'Noah', 'Olivia', 'Ethan'],
            'adventure': ['Captain Drake', 'Explorer Reed', 'Dr. Bennett', 'Agent Cross'],
            'horror': ['Alex', 'Sarah', 'Marcus', 'Dr. Evans', 'The Curator'],
            'comedy': ['Barry', 'Chloe', 'Marcus', 'Dr. Funnybone', 'The Mayor']
        }
        
        # Settings based on genre
        settings = {
            'fantasy': ['Ancient Forest of Whispers', 'Crystal City of Eldoria', 'Dragon Spine Mountains', 'Enchanted Kingdom'],
            'sci-fi': ['Abandoned Space Station', 'Mars Colony Alpha', 'Virtual Reality Grid', 'Neo-Tokyo Megacity'],
            'mystery': ['Abandoned Mansion', 'Private Detective Office', 'Ancient Library', 'Secluded Island Estate'],
            'romance': ['Parisian Café', 'Italian Villa', 'New York Loft', 'Countryside Cottage'],
            'adventure': ['Amazon Jungle', 'Himalayan Peaks', 'Lost City', 'Deep Ocean Trench'],
            'horror': ['Haunted Asylum', 'Dark Forest', 'Abandoned Subway', 'Isolated Cabin'],
            'comedy': ['Quirky Office', 'Small Town Festival', 'Family Reunion', 'Road Trip']
        }
        
        # Objects/Goals
        objects = {
            'fantasy': ['Crystal of Truth', 'Dragon Egg', 'Ancient Spellbook', 'Magic Amulet'],
            'sci-fi': ['AI Core', 'Time Device', 'Alien Artifact', 'Memory Chip'],
            'mystery': ['Hidden Diary', 'Coded Message', 'Lost Heirloom', 'Secret File'],
            'romance': ['Love Letter', 'Family Heirloom', 'Secret Promise', 'Shared Dream'],
            'adventure': ['Treasure Map', 'Ancient Key', 'Lost Compass', 'Secret Code'],
            'horror': ['Cursed Object', 'Haunted Mirror', 'Ancient Tome', 'Forbidden Relic'],
            'comedy': ['Misplaced Invention', 'Secret Recipe', 'Lost Pet', 'Wrong Package']
        }
        
        # Conflicts
        conflicts = {
            'fantasy': ['an ancient curse', 'a dark prophecy', 'a magical imbalance', 'a dragon war'],
            'sci-fi': ['a rogue AI', 'a time paradox', 'an alien invasion', 'a reality collapse'],
            'mystery': ['a hidden conspiracy', 'a family secret', 'a stolen identity', 'a forgotten crime'],
            'romance': ['a misunderstanding', 'family opposition', 'past heartbreak', 'different worlds'],
            'adventure': ['a rival explorer', 'natural disasters', 'ancient traps', 'treacherous terrain'],
            'horror': ['a supernatural entity', 'a psychological breakdown', 'an ancient evil', 'a cursed bloodline'],
            'comedy': ['a case of mistaken identity', 'a series of misunderstandings', 'an elaborate prank', 'a technological glitch']
        }
        
        return {
            'character': random.choice(characters.get(genre, ['Morgan'])),
            'setting': random.choice(settings.get(genre, ['Mysterious Location'])),
            'object': random.choice(objects.get(genre, ['Mysterious Object'])),
            'conflict': random.choice(conflicts.get(genre, ['Mysterious Conflict'])),
            'prompt_words': words
        }

    def generate_title(self, prompt, genre):
        """Generate a creative, relevant title"""
        words = [w for w in prompt.split() if len(w) > 3]
        
        if len(words) >= 2:
            first, second = words[0], words[1]
        else:
            first = words[0] if words else "Mysterious"
            second = "Adventure"
        
        title_templates = {
            'fantasy': [
                f"The {first.title()} of {second.title()}",
                f"Quest for the {first.title()}",
                f"{first.title()}'s Legacy",
                f"The Last {first.title()}"
            ],
            'sci-fi': [
                f"The {first.title()} Protocol",
                f"Project {first.title()}",
                f"{first.title()} Initiative",
                f"The {first.title()} Equation"
            ],
            'mystery': [
                f"The {first.title()} Enigma",
                f"Case of the {first.title()}",
                f"{first.title()} Conspiracy",
                f"The {first.title()} Affair"
            ]
        }
        
        templates = title_templates.get(genre, [f"The {first.title()} Story"])
        return random.choice(templates)

    def generate_structured_content(self, elements, genre, length):
        """Generate a properly structured story with beginning, middle, and end"""
        
        # Introduction paragraph
        introduction = self.generate_introduction(elements, genre)
        
        # Development paragraphs
        if length == 'short':
            development = [self.generate_development(elements, genre)]
            resolution = self.generate_resolution(elements, genre)
            paragraphs = [introduction] + development + [resolution]
            
        elif length == 'medium':
            development1 = self.generate_development(elements, genre)
            development2 = self.generate_complication(elements, genre)
            resolution = self.generate_resolution(elements, genre)
            paragraphs = [introduction, development1, development2, resolution]
            
        else:  # long
            development1 = self.generate_development(elements, genre)
            development2 = self.generate_complication(elements, genre)
            climax = self.generate_climax(elements, genre)
            resolution = self.generate_resolution(elements, genre)
            conclusion = self.generate_conclusion(elements, genre)
            paragraphs = [introduction, development1, development2, climax, resolution, conclusion]
        
        return '\n\n'.join(paragraphs)

    def generate_introduction(self, elements, genre):
        """Generate story introduction"""
        introductions = {
            'fantasy': [
                f"In the mystical land of {elements['setting']}, {elements['character']} discovered {elements['object']} that would change their destiny forever.",
                f"{elements['character']} had always been drawn to the legends of {elements['setting']}, but never imagined they would uncover {elements['object']} and become part of the very stories they admired."
            ],
            'sci-fi': [
                f"When {elements['character']} activated the mysterious device at {elements['setting']}, they unlocked secrets that would challenge everything humanity knew about the universe.",
                f"In the year 2077, {elements['character']} made a discovery at {elements['setting']} that would either save civilization or destroy it completely."
            ],
            'mystery': [
                f"The case began when {elements['character']} found the first clue at {elements['setting']}, unaware it would lead to {elements['conflict']} that had remained hidden for decades.",
                f"{elements['character']} thought it was just another routine investigation at {elements['setting']}, but the discovery of {elements['object']} revealed a web of deception far deeper than imagined."
            ],
            'romance': [
                f"When {elements['character']} arrived at {elements['setting']}, they expected a quiet retreat, not the life-changing encounter that would challenge their heart and redefine their understanding of love.",
                f"The meeting at {elements['setting']} seemed accidental, but for {elements['character']} it was the beginning of a journey that would test everything they believed about relationships and destiny."
            ],
            'adventure': [
                f"The expedition to {elements['setting']} was supposed to be {elements['character']}'s greatest achievement, but the discovery of {elements['object']} turned it into a fight for survival against impossible odds.",
                f"When {elements['character']} set out for {elements['setting']}, they sought adventure and discovery, but found themselves facing challenges that would push them beyond their limits."
            ],
            'horror': [
                f"The silence at {elements['setting']} was the first warning, but {elements['character']} ignored it, unaware they were about to confront {elements['conflict']} that defied all logic and reason.",
                f"{elements['character']} thought the stories about {elements['setting']} were just legends, until they encountered the terrifying reality of {elements['conflict']} that threatened to consume them."
            ],
            'comedy': [
                f"What started as a simple misunderstanding at {elements['setting']} quickly escalated into the most absurd series of events {elements['character']} had ever experienced.",
                f"{elements['character']} expected a normal day at {elements['setting']}, but the discovery of {elements['object']} launched them into a hilarious chain reaction of mishaps and misunderstandings."
            ]
        }
        
        return random.choice(introductions.get(genre, [f"{elements['character']} began their journey at {elements['setting']}, unaware of the incredible adventure that awaited."]))

    def generate_development(self, elements, genre):
        """Generate story development"""
        developments = {
            'fantasy': [
                f"As {elements['character']} learned to control the power of {elements['object']}, they encountered both allies and enemies in the magical realm. Each challenge revealed new aspects of their abilities and the true nature of the magical imbalance affecting the world.",
                f"The journey through enchanted forests and ancient ruins taught {elements['character']} that true power came not from magic alone, but from wisdom and courage in facing {elements['conflict']}."
            ],
            'sci-fi': [
                f"The implications of the discovery at {elements['setting']} became terrifyingly clear as {elements['character']} realized they were dealing with technology that could rewrite reality itself. Each test brought new revelations about the nature of existence.",
                f"As {elements['character']} delved deeper into the mystery, they uncovered a web of corporate secrets and government cover-ups surrounding {elements['object']}, realizing they were just one piece in a much larger conspiracy."
            ],
            'mystery': [
                f"Each clue {elements['character']} uncovered led to more questions than answers, revealing connections to {elements['conflict']} that spanned generations. The investigation became personal when they realized their own safety was at risk.",
                f"The puzzle pieces began fitting together in unexpected ways, showing {elements['character']} that the case was about more than just finding answers—it was about uncovering truths that powerful people wanted buried forever."
            ]
        }
        
        return random.choice(developments.get(genre, [f"As the story progressed, {elements['character']} faced challenges that tested their resolve and revealed hidden strengths."]))

    def generate_complication(self, elements, genre):
        """Generate story complication"""
        complications = {
            'fantasy': [
                f"Just when {elements['character']} thought they understood their quest, a shocking betrayal revealed that {elements['conflict']} was more complex than anyone had imagined. The very foundations of their mission were called into question.",
                f"The appearance of an ancient prophecy complicated everything, suggesting that {elements['character']}'s role in events was predetermined in ways that challenged their free will and moral convictions."
            ],
            'sci-fi': [
                f"A system-wide alert revealed that {elements['object']} was causing unexpected temporal anomalies, threatening to unravel the fabric of spacetime. {elements['character']} had to make impossible choices with consequences spanning multiple dimensions.",
                f"The discovery that {elements['conflict']} was actually a failsafe mechanism created by future humans to prevent their own extinction forced {elements['character']} to question whether they should interfere with destiny."
            ],
            'mystery': [
                f"A sudden threat to someone close to {elements['character']} raised the stakes dramatically, forcing them to work against the clock while dealing with unexpected personal connections to {elements['conflict']}.",
                f"The revelation that key evidence had been fabricated created a crisis of trust, making {elements['character']} question every assumption and ally in their investigation of {elements['conflict']}."
            ]
        }
        
        return random.choice(complications.get(genre, [f"Unexpected complications arose, forcing {elements['character']} to adapt their strategy and confront new challenges."]))

    def generate_climax(self, elements, genre):
        """Generate story climax"""
        climaxes = {
            'fantasy': [
                f"In the final confrontation at the heart of {elements['setting']}, {elements['character']} faced the source of {elements['conflict']}, using all their knowledge and courage in a desperate attempt to restore balance to the magical world.",
                f"The ultimate test came when {elements['character']} had to choose between using {elements['object']}'s full power—risking everything—or finding another way to resolve {elements['conflict']} through sacrifice and wisdom."
            ],
            'sci-fi': [
                f"As reality itself began to fracture around {elements['setting']}, {elements['character']} initiated the final protocol, knowing it could either save humanity or erase their entire timeline from existence.",
                f"The countdown to system collapse reached its final moments, forcing {elements['character']} to make a decision that would determine the future of human consciousness and artificial intelligence forever."
            ],
            'mystery': [
                f"In a dramatic confrontation that revealed the shocking truth behind {elements['conflict']}, {elements['character']} faced the mastermind, uncovering motives that were both personal and profoundly universal.",
                f"The final pieces of the puzzle clicked into place during a tense standoff, revealing that the solution to {elements['conflict']} required understanding rather than punishment, redemption rather than revenge."
            ]
        }
        
        return random.choice(climaxes.get(genre, [f"In the story's climax, {elements['character']} faced their greatest challenge and made decisions that would change everything."]))

    def generate_resolution(self, elements, genre):
        """Generate story resolution"""
        resolutions = {
            'fantasy': [
                f"In the aftermath, {elements['character']} understood that true power came from balance and compassion. The world had changed, but new beginnings emerged from the resolution of {elements['conflict']}.",
                f"With peace restored to {elements['setting']}, {elements['character']} realized their journey had been about more than just defeating evil—it was about understanding the delicate balance between all magical beings."
            ],
            'sci-fi': [
                f"As systems stabilized and new protocols were established, {elements['character']} reflected on how close they had come to catastrophe. The experience changed their understanding of technology's role in human evolution.",
                f"The resolution brought not just safety, but new possibilities for humanity's future. {elements['character']} had learned that progress required both innovation and responsibility in equal measure."
            ],
            'mystery': [
                f"With the truth finally revealed and justice served, {elements['character']} understood that some mysteries are solved not by finding answers, but by asking better questions about human nature and redemption.",
                f"The case closed, but the lessons learned about {elements['conflict']} would stay with {elements['character']} forever, changing how they approached both their work and their understanding of human complexity."
            ]
        }
        
        return random.choice(resolutions.get(genre, [f"In the end, {elements['character']} found resolution and new understanding through their experiences."]))

    def generate_conclusion(self, elements, genre):
        """Generate story conclusion"""
        conclusions = {
            'fantasy': [
                f"And so, {elements['character']} returned to a world forever changed by their actions, carrying the wisdom of their journey and the knowledge that magic exists in the balance between light and shadow.",
                f"The legend of {elements['character']}'s quest would be told for generations, inspiring others to seek balance and understanding in a world where magic and reality intertwine in mysterious ways."
            ],
            'sci-fi': [
                f"Looking at the stars from their station at {elements['setting']}, {elements['character']} understood that humanity's greatest adventures were just beginning, with new frontiers of discovery awaiting beyond the horizon.",
                f"The experience had transformed {elements['character']}, leaving them with a profound appreciation for the delicate dance between technological advancement and ethical responsibility in shaping humanity's destiny."
            ],
            'mystery': [
                f"As life returned to normal, {elements['character']} carried the lessons of the case forward, understanding that every mystery solved revealed new questions about truth, justice, and the human capacity for both darkness and redemption.",
                f"The resolution brought closure, but {elements['character']} knew that the world was full of stories waiting to be uncovered, each with its own lessons about the complex tapestry of human experience."
            ]
        }
        
        return random.choice(conclusions.get(genre, [f"The journey had changed {elements['character']} in ways they were only beginning to understand, opening new paths for future adventures."]))

    def create_fallback_story(self, prompt, genre, length):
        """Create a simple but coherent fallback story"""
        elements = self.extract_story_elements(prompt, genre)
        content = self.generate_structured_content(elements, genre, length)
        
        return {
            'title': self.generate_title(prompt, genre),
            'content': content,
            'prompt': prompt,
            'genre': genre,
            'length': length,
            'source': 'fallback'
        }

# Create global instance
narrative_generator = NarrativeStoryGenerator()