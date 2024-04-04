function setupSuggestions(inputId, suggestionsContainerId, dataFile) {
    document.addEventListener('DOMContentLoaded', function () {
        const inputField = document.getElementById(inputId);
        const suggestionsContainer = document.getElementById(suggestionsContainerId);

        let suggestions = [];

        // Fetch suggestions from the data file
        fetch(dataFile)
            .then(response => response.text())
            .then(data => {
                suggestions = data.split('\n').filter(item => item.trim() !== '');
            });

        inputField.addEventListener('input', function () {
            const inputValue = inputField.value.toLowerCase();
            const filteredSuggestions = suggestions.filter(suggestion => suggestion.toLowerCase().includes(inputValue));

            showSuggestions(filteredSuggestions);
        });

        inputField.addEventListener('focus', function () {
            if (inputField.value.trim() !== '') {
                showSuggestions(suggestions);
            }
        });

        function showSuggestions(suggestionsList) {
            if (suggestionsList.length > 0) {
                const suggestionHTML = suggestionsList.map(suggestion => `<div>${suggestion}</div>`).join('');
                suggestionsContainer.innerHTML = suggestionHTML;
                suggestionsContainer.style.display = 'block';
            } else {
                suggestionsContainer.style.display = 'none';
            }
        }

        document.addEventListener('click', function (event) {
            if (!event.target.matches(`#${inputId}`) && !event.target.matches(`#${suggestionsContainerId} div`)) {
                suggestionsContainer.style.display = 'none';
            }
        });

        suggestionsContainer.addEventListener('click', function (event) {
            if (event.target.matches('div')) {
                inputField.value = event.target.textContent;
                suggestionsContainer.style.display = 'none';
            }
        });
    });
}

// Set up for the first input field
setupSuggestions('state', 'suggestions', 'states');
setupSuggestions('institution', 'suggestions2', 'institution');
setupSuggestions('course', 'suggestions3', 'department');
setupSuggestions('LGA', 'suggestions1', 'LGA');