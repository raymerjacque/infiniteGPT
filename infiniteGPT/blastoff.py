import openai
from concurrent.futures import ThreadPoolExecutor

# Add your own OpenAI API key

openai.api_key = "sk-XXXXXXXXXXXXXXXXXXXXX"

def load_text(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def save_to_file(responses, output_file):
    with open(output_file, 'w') as file:
        for response in responses:
            file.write(response + '\n')

# Change your OpenAI chat model accordingly

def call_openai_api(chunk, chat_history=None):
    messages = [
        {"role": "system", "content": "PASS IN ANY ARBITRARY SYSTEM VALUE TO GIVE THE AI AN IDENITY"}
    ]
    
    if chat_history:
        messages.extend(chat_history)

    messages.append({"role": "user", "content": f"OPTIONAL PREPROMPTING FOLLOWING BY YOUR DATA TO PASS IN: {chunk}."})
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1750,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0]['message']['content'].strip()

def split_into_chunks(text, tokens=1500):
    words = text.split()
    chunks = [' '.join(words[i:i + tokens]) for i in range(0, len(words), tokens)]
    return chunks

def process_chunks(input_file, output_file):
    text = load_text(input_file)
    chunks = split_into_chunks(text)

    chat_history = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you! How can I help you today?"}
    ]
    
    # Processes chunks in parallel
    with ThreadPoolExecutor() as executor:
        # Use a lambda function to pass chat_history to call_openai_api
        responses = list(executor.map(lambda chunk: call_openai_api(chunk, chat_history), chunks))

    save_to_file(responses, output_file)

# Specify your input and output files

if __name__ == "__main__":
    input_file = "your_input_here.txt"
    output_file = "your_output_here.txt"
    process_chunks(input_file, output_file)

# Can take up to a few minutes to run depending on the size of your data input
