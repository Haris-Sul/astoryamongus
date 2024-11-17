import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import GenerationConfig

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

def generate_intro(keywords, max_intro_length=200):
    intro_prompt = "write the opening paragraph for a story that uses the following words:"
    for keyword in keywords:
        intro_prompt += f" {keyword}"

    generation_config = GenerationConfig(
        max_output_tokens=max_intro_length,
        temperature=0.5,
        top_p=0.9,
        frequency_penalty=0.5,
        presence_penalty=0.5
    )

    model = genai.GenerativeModel("gemini-1.5-flash-8b")
    response = model.generate_content(
        contents=intro_prompt,
        generation_config=generation_config
    )

    return response.text


def generate_sentence(story_so_far, max_sentence_length=100):
    sentence_prompt = f"write the next sentence in the story. The story so far is: {story_so_far}"

    generation_config = GenerationConfig(
        max_output_tokens=max_sentence_length,
        temperature=0.5,
        top_p=0.9,
        frequency_penalty=0.5,
        presence_penalty=0.5
    )

    model = genai.GenerativeModel("gemini-1.5-flash-8b")
    response = model.generate_content(
        contents=sentence_prompt,
        generation_config=generation_config
    )

    return response.text


# Example usage:

# keywords = ["penguins", "space", "adventure", "mystery"]
# intro = generate_intro(keywords)
# print("Generated Intro:")
# print(intro)


# story_so_far = "The wind howled a mournful song across the icy plains..."
# next_sentence = generate_sentence(story_so_far)
# print("Generated Next Sentence:") 
# print(next_sentence)