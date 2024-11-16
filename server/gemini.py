from configparser import ConfigParser
import google.generativeai as genai
from google.generativeai import GenerationConfig

MAX_INTRO_LENGTH = 200
MAX_SENTENCE_LENGTH = 100

try:
    config = ConfigParser()
    config.read('credentials.ini')
    api_key = config['API_KEY']['google_api_key']

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-8b")

    keywords = ["penguins", "space", "adventure", "mystery"]

    intro_prompt = "write the opening paragraph for a story that uses the following words:"

    for keyword in keywords:
        intro_prompt += f" {keyword}"

    # print(intro_prompt)

    sentence_prompt = '''write the next sentence in the story. The story so far is: 
    The wind howled a mournful song across the icy plains, a symphony of frozen air that echoed the vastness of spac
e above.  A small band of penguins, their black and white coats gleaming under the pale lunar light, huddled tog
ether, their beady eyes reflecting the unsettling mystery that clung to the abandoned research station.  This wa
sn't just another freezing Antarctic night; this was the start of an extraordinary adventure.'''

    generation_config = GenerationConfig(
        max_output_tokens=MAX_SENTENCE_LENGTH,
        temperature=0.5,
        top_p=0.9,
        frequency_penalty=0.5,
        presence_penalty=0.5
    )

    response = model.generate_content(
        contents=sentence_prompt,
        generation_config=generation_config
    )

    print(response.text)

except KeyError as e:
    print(f"Key error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")