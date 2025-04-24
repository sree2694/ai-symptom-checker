# utils/openai_helper.py
import openai
import os
import json

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
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=500
        )
        message = response['choices'][0]['message']['content']
        
        # Parse the JSON from GPT response
        data = json.loads(message.strip())
        return data
    except json.JSONDecodeError as je:
        return {"error": "Failed to parse GPT response. Check formatting.", "raw": message}
    except openai.error.OpenAIError as oe:
        return {"error": f"OpenAI API error: {str(oe)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
