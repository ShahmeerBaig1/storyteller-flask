from flask import Flask, request, jsonify
import os
from together import Together
import json
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)

CORS(app)

def generate_story(prompt, retry_count=1):
    try:
        client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

        response = client.completions.create(
            model="meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
            prompt=f"Write one small story for kids with this setup: [{prompt}] output format: {{'title': story title, 'story': story}}), dont return anything other than the plain json ",
            max_tokens=500,
            temperature=0.7,
        )

        story_text = response.choices[0].text.strip().split('}')[0] + "}"
        json_story = json.loads(story_text)
        return json_story

    except Exception as e:
        if retry_count > 0:
            return generate_story(prompt, retry_count - 1)
        else:
            return {'error': 'An error occurred, Please try again'}

@app.route('/api/generate', methods=['POST'])
def generate():
    prompt = request.json.get('prompt', '')
    story = generate_story(prompt)
    return jsonify(story)

if __name__ == '__main__':
    app.run()
