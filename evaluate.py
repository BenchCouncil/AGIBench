import json
import argparse
import openai
import time
import requests

def extract_problem(json_data, prompt):
    problem_parts = [json_data['Question']]
    
    options = ['A', 'B', 'C', 'D']
    for option in options:
        problem_parts.append(f"{option}. {json_data[f'Option_{option}']}")
    # problem = f"{json_data['Question']}\nA. {json_data['Option_A']}\nB. {json_data['Option_B']}\nC. {json_data['Option_C']}D. \n{json_data['Option_D']}\n"
    problem = '\n'.join(problem_parts)
    if prompt:
        problem = f"{problem}\n{prompt}"
    return problem


def ask_chatgpt(prompt, model='gpt-3.5-turbo-0301', max_tokens=512, temperature=1, n=1, **noused_args):
    while True:
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
                n=n,
            )
            return response.choices[0].message["content"].strip()
        except Exception as e:
            print(f"Error occurred: {e}")
            print("Retrying in 3 seconds...")
            time.sleep(3)


def ask_gpt(prompt, model='text-davinci-003', max_tokens=512, temperature=1, n=1, **noused_args):
    while True:
        try:
            response = openai.Completion.create(
                engine=model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                n=n,
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Error occurred: {e}")
            print("Retrying in 3 seconds...")
            time.sleep(3)


def ask_glm(endpoint, prompt, temperature, **noused_args):
    while True:
        try:
            url = endpoint
            headers = {"Content-Type": "application/json"}
            data = {
                "prompt": f"{prompt}",
                "history": [],
                "temperature": temperature
            }
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response_json = response.json()
            message = response_json.get('response', 'Message field not found')
            return message
        except Exception as e:
            print(f"Error occurred: {e}")
            print("Retrying in 30 seconds...")
            time.sleep(30)


def ask_fastchat(endpoint, prompt, model_name, max_tokens, temperature, *noused_args):
    prompt_begining = "A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions.###Human: What are the key differences between renewable and non-renewable energy sources?###Assistant: Renewable energy sources are those that can be replenished naturally in a relatively short amount of time, such as solar, wind, hydro, geothermal, and biomass. Non-renewable energy sources, on the other hand, are finite and will eventually be depleted, such as coal, oil, and natural gas. Here are some key differences between renewable and non-renewable energy sources:\n1. Availability: Renewable energy sources are virtually inexhaustible, while non-renewable energy sources are finite and will eventually run out.\n2. Environmental impact: Renewable energy sources have a much lower environmental impact than non-renewable sources, which can lead to air and water pollution, greenhouse gas emissions, and other negative effects.\n3. Cost: Renewable energy sources can be more expensive to initially set up, but they typically have lower operational costs than non-renewable sources.\n4. Reliability: Renewable energy sources are often more reliable and can be used in more remote locations than non-renewable sources.\n5. Flexibility: Renewable energy sources are often more flexible and can be adapted to different situations and needs, while non-renewable sources are more rigid and inflexible.\n6. Sustainability: Renewable energy sources are more sustainable over the long term, while non-renewable sources are not, and their depletion can lead to economic and social instability.\n###Human:"
    prompt_ending = "###Assistant:"

    prompt = prompt_begining + prompt + prompt_ending

    payload = {
        "model": model_name,
        "prompt": prompt,
        "temperature": float(temperature),
        "max_new_tokens": int(max_tokens),
        'stop': "###"
    }

    while True:
        try:
            response = requests.post(endpoint + "/worker_generate_stream",
                                     json=payload, stream=True, timeout=20)
            output = ''
            for chunk in response.iter_lines(decode_unicode=False, delimiter=b"\0"):
                if chunk:
                    data = json.loads(chunk.decode())
                    if data["error_code"] == 0:
                        output = data["text"].strip()
                    else:
                        output = data["text"] + f" (error_code: {data['error_code']})"
                        print(output)
                        return
                    time.sleep(0.02)
            return output.split(prompt_ending)[2]
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            print("Retrying in 3 seconds...")
            time.sleep(3)


def ask_llm(problem, model='text-davinci-003', **kwargs):
    llms = {
        'text-davinci-003': ask_gpt,
        'gpt-3.5-turbo-0301': ask_chatgpt,
        'gpt-4': ask_chatgpt,
        'llama-13b': ask_fastchat,
        'chatglm': ask_glm,
        'chatglm2': ask_glm
    }
    kwargs['model'] = model
    kwargs['prompt'] = problem

    return llms.get(model)(**kwargs)


def main(input_file, output_file, endpoint, model, prompt, max_tokens, temperature, n):
    with open(input_file, 'r') as f:
        json_data = json.load(f)

    results = []

    for question_data in json_data:
        problem = extract_problem(question_data, prompt)
        response = ask_llm(problem, model=model, endpoint=endpoint, max_tokens=max_tokens, temperature=temperature, n=n)
        question_data["LLM_Prompt"] = problem
        question_data["LLM_Response"] = response
        print(f'{"-" * 16}')
        print(problem, response)
        results.append(question_data)


    with open(output_file, 'w') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send problems from JSON file to LLM and save output to a file.")
    parser.add_argument("-i", "--input", required=True, help="Input JSON file.")
    parser.add_argument("-o", "--output", required=True, help="Output file to save LLM responses.")
    parser.add_argument("--model", default="text-davinci-003", help="LLM model to use.")
    parser.add_argument('--endpoint', help="Endpoint to call LLM")
    parser.add_argument("--prompt", required=True, help="Prompt type.")
    # parser.add_argument("--use_chat_api", action="store_true", help="Use Chat API instead of Completion API.")
    parser.add_argument("--max_tokens", type=int, default=150, help="Maximum tokens for LLM response.")
    parser.add_argument("--temperature", type=float, default=0.8, help="Sampling temperature for LLM response.")
    parser.add_argument("--n", type=int, default=1, help="Number of completions to generate.")
    args = parser.parse_args()

    main(args.input, args.output, args.endpoint, args.model, args.prompt, args.max_tokens, args.temperature, args.n)
