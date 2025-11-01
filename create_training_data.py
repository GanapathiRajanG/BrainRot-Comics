import json
import os
import sys

# Add the current directory to Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.synthetic_data_generator import SyntheticDataGenerator

def create_training_data():
    print("Generating synthetic training data...")
    generator = SyntheticDataGenerator()
    
    # Generate a smaller dataset for demonstration
    dataset = generator.generate_dataset(500)
    
    # Ensure data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Save the dataset
    with open('data/training_data.json', 'w') as f:
        json.dump(dataset, f, indent=2)
    
    print(f"Training data generated with {len(dataset)} samples")
    print(f"Saved to: data/training_data.json")
    return dataset

if __name__ == "__main__":
    create_training_data()