import os
from dotenv import load_dotenv
import openai

def get_openai_response(prompt, model="gpt-4o-mini"):
    load_dotenv()
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Replace with your OpenAI API key
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

def create_prompt(user_input):
    prompt = "What is the likelihood that the following email is a phishing attempt on a scale from 0-100:\n" + user_input
    prompt += "Provide one number from 0-100 on the first line and the explanation in the next line."
    print(prompt)
    return prompt

if __name__ == "__main__":
    user_prompt = input("Enter your email: ")

    
    response = get_openai_response(create_prompt(user_prompt))
    print("Response:", response)