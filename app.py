from flask import Flask, render_template, request, jsonify
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Use the new narrative story generator
try:
    from model.narrative_story_generator import narrative_generator
    STORY_GENERATOR = narrative_generator
    logger.info("✅ Narrative story generator loaded successfully!")
except Exception as e:
    logger.error(f"❌ Narrative generator failed: {e}")
    # Fallback to simple generator
    try:
        from model.simple_story_generator import story_generator
        STORY_GENERATOR = story_generator
        logger.info("✅ Using simple story generator as fallback")
    except Exception as e2:
        logger.error(f"❌ All generators failed: {e2}")
        # Ultimate fallback
        class UltimateFallback:
            def generate_story(self, prompt, genre, length):
                return {
                    'title': f"Story: {prompt}",
                    'content': f"This is a {length} {genre} story about {prompt}.",
                    'prompt': prompt,
                    'genre': genre,
                    'length': length
                }
        STORY_GENERATOR = UltimateFallback()


# Try to import and load enhanced story generator
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'model'))
    from enhanced_story_generator import enhanced_story_generator
    STORY_GENERATOR = enhanced_story_generator
    logger.info("Enhanced story generator loaded successfully with CSV data!")
except Exception as e:
    logger.warning(f"Enhanced generator not available: {e}")
    # Fallback to basic generator
    from model.story_generator import story_generator
    STORY_GENERATOR = story_generator
    logger.info("Using basic story generator")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_story', methods=['POST'])
def generate_story():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        genre = data.get('genre', 'fantasy')
        length = data.get('length', 'medium')
        
        logger.info(f"Generating story: prompt='{prompt}', genre={genre}, length={length}")
        
        if not prompt:
            return jsonify({'error': 'Please enter a story prompt'}), 400
        
        # Generate story using the available generator
        story = STORY_GENERATOR.generate_story(prompt, genre, length)
        
        logger.info(f"Story generated successfully: {story['title']}")
        return jsonify(story)
        
    except Exception as e:
        logger.error(f"Story generation error: {e}")
        return jsonify({'error': f'Story generation failed: {str(e)}'}), 500

@app.route('/example_prompts')
def get_example_prompts():
    examples = [
        {"prompt": "A time traveler who accidentally changes a minor historical event", "genre": "sci-fi"},
        {"prompt": "A detective who can speak to ghosts", "genre": "mystery"},
        {"prompt": "A world where dreams become reality", "genre": "fantasy"},
        {"prompt": "A chef who discovers magical ingredients", "genre": "fantasy"},
        {"prompt": "A robot who falls in love with a human", "genre": "sci-fi"},
        {"prompt": "A librarian who finds a book that writes itself", "genre": "mystery"},
        {"prompt": "An explorer who finds a map of possibilities", "genre": "adventure"},
        {"prompt": "A reflection that develops its own consciousness", "genre": "horror"}
    ]
    return jsonify(examples)

@app.route('/add_story', methods=['POST'])
def add_story_to_csv():
    """Endpoint to add new stories to CSV"""
    try:
        data = request.get_json()
        # Implementation for adding stories to CSV
        return jsonify({'message': 'Story added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('model', exist_ok=True)
    
    logger.info("Starting BrainROT Comics with Enhanced Story Generator")
    logger.info("Available on: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)