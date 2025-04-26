import openai
import os
import json
import logging
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_conditions(age: int, gender: str, symptoms: list[str]):
    prompt = (
        f"You are a medical assistant.\n"
        f"User is a {age}-year-old {gender} experiencing: {', '.join(symptoms)}.\n"
        "Provide 2-3 possible conditions and care suggestions in strict JSON format like:\n\n"
        '''{
            "conditions": [
                {
                    "name": "Condition Name",
                    "probability": "High/Medium/Low",
                    "suggestion": "Recommended care or next steps"
                }
            ]
        }'''
    )

    try:
        logging.info(f"Sending request to OpenAI with prompt: {prompt[:100]}...")  # Log part of the prompt for debugging
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  # or other models
            prompt=prompt,
            temperature=0.5,
            max_tokens=500
        )
        message = response['choices'][0]['text']
        
        # Parse the JSON from GPT response
        logging.info(f"OpenAI response: {message[:100]}...")  # Log part of the response for debugging
        data = json.loads(message.strip())
        return data
    except json.JSONDecodeError as je:
        logging.error(f"JSON decode error: {je}")
        return {"error": "Failed to parse GPT response. Check formatting.", "raw": message}
    except openai.OpenAIError as oe:
        logging.error(f"OpenAI API error: {str(oe)}")
        return {"error": f"OpenAI API error: {str(oe)}"}
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return {"error": f"Unexpected error: {str(e)}"}
