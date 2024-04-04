
# from django import forms
# from django.template.loader import get_template

# class SuggestionsWidget(forms.TextInput):
#     def __init__(self, suggestions_template, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.suggestions_template = suggestions_template

#     def render(self, name, value, attrs=None, renderer=None):
#         rendered = super().render(name, value, attrs, renderer)
#         suggestions_template = get_template(self.suggestions_template)
#         suggestions = suggestions_template.render()
#         return rendered + f'<datalist id="{name}_datalist">{suggestions}</datalist>'

# widgets.py
from django import forms

class SuggestionsWidget(forms.TextInput):
    def __init__(self, suggestions_file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open(suggestions_file, 'r') as f:
            self.suggestions = [line.strip() for line in f]

    def render(self, name, value, attrs=None, renderer=None):
        rendered = super().render(name, value, attrs, renderer)
        options = '\n'.join(f'<option value="{s}">{s}</option>' for s in self.suggestions)
        return rendered + f'<datalist id="{name}_datalist">{options}</datalist>'








# widgets.py
from django.forms import TextInput
from django.utils.safestring import mark_safe

class SuggestionInput(TextInput):
    class Media:
        js = ['suggestion_widgets.js']


    def render(self, name, value, attrs=None, renderer=None):
        rendered = super().render(name, value, attrs, renderer)
        script = """
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const inputElement = document.querySelector('#id_%s');
                const suggestionList = document.createElement('datalist');
                suggestionList.id = '%s-suggestions'; // Generate unique ID for suggestions
                inputElement.setAttribute('list', suggestionList.id);
               
                inputElement.addEventListener('input', function() {
                    const inputText = inputElement.value.trim().toLowerCase();
                    const suggestions = document.querySelector('#%s');
                    suggestions.innerHTML = ''; // Clear previous suggestions

                    // Fetch suggestions from text file
                    fetch('/get_suggestions')
                        .then(response => response.text())
                        .then(data => {
                            const suggestionOptions = data.split('\\n');
                            suggestionOptions.forEach(option => {
                                if (option.toLowerCase().includes(inputText)) {
                                    const suggestion = document.createElement('option');
                                    suggestion.value = option;
                                    suggestionList.appendChild(suggestion);
                                }
                            });
                        })
                        .catch(error => console.error('Error fetching suggestions:', error));
                });
            });
        </script>
        """ % (attrs['id'], attrs['id'], attrs['id'])  # Use attribute ID to generate unique IDs

        return mark_safe(rendered + script)

