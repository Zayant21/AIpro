$(document).ready(function () {
    /* Define a dictionary to keep track of the state of each word */
    const wordState = {};

    function updateVocabularyDisplay() {
        const vocabularyDisplay = document.getElementById('vocabulary-display');
        vocabularyDisplay.textContent = ''; 

        vocabulary.forEach(word => {
            const wordSpan = document.createElement('span');
            wordSpan.textContent = word;
            wordSpan.className = 'vocabulary-word'; 

            if (wordState[word] === 'X') {
                wordSpan.textContent = word;
            }

            wordSpan.addEventListener('click', () => {
                if (wordState[word] === 'X') {
                    const wordIndex = vocabulary.indexOf(word);
                    if (wordIndex !== -1) {
                        /* Make an AJAX DELETE request to remove the word */
                        $.ajax({
                            url: '/remove_vocab_word/' + word,
                            type: 'DELETE',
                            success: function (data) {
                                if (data.success) {
                                    vocabulary.splice(wordIndex, 1);
                                    delete wordState[word];
                                    updateVocabularyDisplay();
                                    sendRequest();
                                } else {
                                    console.error('Failed to remove the word.');
                                }
                            },
                            error: function () {
                                console.error('Error removing the word.');
                            }
                        });
                    }
                } else {
                    wordState[word] = 'X';
                    wordSpan.textContent = word;
                    wordSpan.classList.toggle('vocabulary-word-selected');
                }
            });

            vocabularyDisplay.appendChild(wordSpan);
        });

        const inputBox = document.createElement('input');
        inputBox.id = 'word-input';
        inputBox.placeholder = 'Add vocab...';
        inputBox.style.display = 'none'; 

        inputBox.addEventListener('keypress', function (event) {
            if (event.key === 'Enter') {
                const newWord = inputBox.value.trim();
                if (newWord !== '') {
                    // Make an AJAX POST request to add the word
                    $.ajax({
                        url: '/add_vocab_word',
                        type: 'POST',
                        data: JSON.stringify({ word: newWord }),
                        contentType: 'application/json',
                        success: function (data) {
                            if (data.success) {
                                vocabulary.push(newWord);
                                wordState[newWord] = newWord;
                                updateVocabularyDisplay();
                                sendRequest();
                                inputBox.style.display = 'none'; 
                                addWordButton.style.display = 'block'; 
                                inputBox.value = '';
                            } else {
                                console.error('Failed to add the word.');
                            }
                        },
                        error: function () {
                            console.error('Error adding the word.');
                        }
                    });
                }
            }
        });

        vocabularyDisplay.appendChild(inputBox);

        const addWordButton = document.createElement('button');
        addWordButton.id = 'add-word-button';
        addWordButton.textContent = '+';
        addWordButton.className = 'add-word-button';

        addWordButton.addEventListener('click', () => {
            addWordButton.style.display = 'none'; 
            inputBox.style.display = 'inline-block'; 
            inputBox.style.marginLeft = '5px';
            inputBox.focus();
        });

        vocabularyDisplay.appendChild(addWordButton);
    }

    /* Function to fetch vocabulary data from the server */
    function fetchVocabularyData() {
        fetch('/get_vocabulary_data')
            .then(response => response.json())
            .then(data => {
                vocabulary = data.map(item => item[1]);
                updateVocabularyDisplay();
            })
            .catch(error => {
                console.error('Error fetching vocabulary data: ' + error);
            });
    }

    fetchVocabularyData();
});
