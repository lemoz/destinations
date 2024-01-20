from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Load context data from file
with open('context.json', 'r') as file:
    context_data = json.load(file)

# Cache dictionary to store generated pages
cache = {}

def generate_custom_content(source_context):
    # This function would contain the logic to generate custom content based on the context.
    # It returns a string of HTML content.
    # For demonstration purposes, let's just return a sample string that would be replaced
    # with the actual dynamic content generation logic.
    print("Generation Step")
    return "<h1>{}</h1>".format(source_context['sourceProperties']['Ad_Copy']['Headline'])

@app.route('/')
def index():
    # Get source ID from URL parameter
    source_id = request.args.get('sourceId', 'default')
    print("source_id:" + source_id)

    # Check if the page for this sourceId is already in cache
    if source_id in cache:
        print("Fetching Cached Version")
        return cache[source_id]

    # Find the context for the given source ID
    source_context = next((item for item in context_data if item['sourceId'] == source_id), None)

    if source_context:
        # Generate custom content based on the source context
        custom_content = generate_custom_content(source_context)
        # Replace the placeholder in the HTML template with custom content
        # This assumes that the placeholder is denoted by a specific HTML comment
        # such as <!--CUSTOM_CONTENT--> in your index.html template
        rendered_page = render_template('index.html').replace('<!--CUSTOM_CONTENT-->', custom_content)
    else:
        # If no context is found, render the default page
        rendered_page = render_template('index.html')

    # Cache the generated page
    cache[source_id] = rendered_page

    return rendered_page

if __name__ == '__main__':
    app.run(debug=True)