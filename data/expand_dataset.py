import pandas as pd
import random

def expand_dataset():
    # Sample additional stories to add to your CSV
    additional_stories = [
        {
            'genre': 'fantasy',
            'title': 'The Dragon\'s Promise',
            'prompt': 'A dragon bonds with a human child',
            'content': 'The last silver dragon, Argentis, made a promise to protect a human village centuries ago. When Elara, a orphaned child, stumbled into his cave during a blizzard, the ancient bond was renewed. Argentis taught Elara the old magic—how to speak with mountains and read stories in starlight. But when dragon hunters discovered their sanctuary, Elara had to protect the very creature sworn to protect her. Using cleverness rather than strength, she turned the hunters against each other, proving that the smallest beings could wield the greatest power. The dragon\'s promise evolved from duty to genuine friendship, changing both their worlds forever.',
            'length': 'long',
            'rating': 9.0
        },
        {
            'genre': 'sci-fi', 
            'title': 'The Memory Thief',
            'prompt': 'A device that can steal and trade memories',
            'content': 'Dr. Aris Thorne invented the Mnemonic Transference Device to help Alzheimer\'s patients, but it soon became the ultimate black market commodity. Memories of perfect vacations, professional skills, even love could be bought and sold. Aris discovered a criminal syndicate using his invention to steal memories from politicians and celebrities. The worst part? He couldn\'t trust his own memories—they might have been altered or stolen. In a desperate move, Aris injected himself with a cocktail of memories from his enemies, becoming a living database of their secrets. The final confrontation happened in the memoryscape itself, a battle fought with recollections and regrets.',
            'length': 'medium',
            'rating': 8.9
        }
    ]
    
    # Add more stories as needed...
    
    try:
        # Load existing CSV or create new
        try:
            df = pd.read_csv('data/stories_dataset.csv')
        except FileNotFoundError:
            df = pd.DataFrame()
            
        # Add new stories
        new_df = pd.DataFrame(additional_stories)
        expanded_df = pd.concat([df, new_df], ignore_index=True)
        
        # Save expanded dataset
        expanded_df.to_csv('data/stories_dataset.csv', index=False)
        print(f"Dataset expanded! Total stories: {len(expanded_df)}")
        
    except Exception as e:
        print(f"Error expanding dataset: {e}")

if __name__ == '__main__':
    expand_dataset()