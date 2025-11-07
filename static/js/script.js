document.addEventListener('DOMContentLoaded', function() {
    const storyForm = document.getElementById('story-form');
    const promptInput = document.getElementById('prompt');
    const genreSelect = document.getElementById('genre');
    const lengthSelect = document.getElementById('length');
    const clearBtn = document.getElementById('clear-btn');
    const loadingElement = document.getElementById('loading');
    const storyOutput = document.getElementById('story-output');
    const storyTitle = document.getElementById('story-title');
    const storyContent = document.getElementById('story-content');
    const copyBtn = document.getElementById('copy-btn');
    const newStoryBtn = document.getElementById('new-story-btn');
    const errorMessage = document.getElementById('error-message');
    const examplePromptsContainer = document.getElementById('example-prompts');
    
    // Load example prompts from server
    fetch('/example_prompts')
        .then(response => response.json())
        .then(examples => {
            examples.forEach(example => {
                const promptElement = document.createElement('div');
                promptElement.className = 'example-prompt';
                promptElement.textContent = example.prompt;
                promptElement.setAttribute('data-prompt', example.prompt);
                promptElement.setAttribute('data-genre', example.genre);
                
                promptElement.addEventListener('click', function() {
                    promptInput.value = this.getAttribute('data-prompt');
                    genreSelect.value = this.getAttribute('data-genre');
                    errorMessage.style.display = 'none';
                });
                
                examplePromptsContainer.appendChild(promptElement);
            });
        })
        .catch(error => {
            console.error('Error loading example prompts:', error);
        });
    
    // Form submission
    storyForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const prompt = promptInput.value.trim();
        const genre = genreSelect.value;
        const length = lengthSelect.value;
        
        if (!prompt) {
            errorMessage.style.display = 'block';
            return;
        }
        
        errorMessage.style.display = 'none';
        loadingElement.style.display = 'flex';
        storyOutput.style.display = 'none';
        
        // Send request to server
        fetch('/generate_story', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                genre: genre,
                length: length
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            loadingElement.style.display = 'none';
            storyTitle.textContent = data.title;
            storyContent.textContent = data.content;
            storyOutput.style.display = 'flex';
        })
        .catch(error => {
            loadingElement.style.display = 'none';
            errorMessage.textContent = `Error: ${error.message}`;
            errorMessage.style.display = 'block';
        });
    });
    
    // Clear form
    clearBtn.addEventListener('click', function() {
        promptInput.value = '';
        genreSelect.value = 'fantasy';
        lengthSelect.value = 'short';
        errorMessage.style.display = 'none';
    });
    
    // Copy story to clipboard
    copyBtn.addEventListener('click', function() {
        const storyText = `${storyTitle.textContent}\n\n${storyContent.textContent}`;
        navigator.clipboard.writeText(storyText).then(() => {
            const originalText = copyBtn.innerHTML;
            copyBtn.innerHTML = '<i>✓</i> Copied!';
            setTimeout(() => {
                copyBtn.innerHTML = originalText;
            }, 2000);
        });
    });
    
    // New story button
    newStoryBtn.addEventListener('click', function() {
        storyOutput.style.display = 'none';
        promptInput.value = '';
        promptInput.focus();
    });
    
    // Initialize with an example story
    promptInput.value = "A robot who falls in love with a human";
});