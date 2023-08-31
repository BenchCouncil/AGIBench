# AGIBench

AGIBench stands for a multi-granularity, multimodal, human-referenced, auto-scoring benchmark tailored for large language models. This repository hosts the dataset utilized by AGIBench.

The `datasets.json` file comprises 927 instances. Each instance features a question, its associated options, the correct answer, human-referenced accuracy, reason, difficulty level, ability branch, knowledge domain, modality information, and more. In details, the `datasets.json` contains three ability branches, including common sense, understanding, and reason. In terms of knowledge, it contains 20 primary knowledge domains, and 68 sub knowledge domans. We 

## Extract Data

To extract data tailored to your benchmarking requirements, you can employ [`jq`](https://github.com/jqlang/jq), a versatile command-line JSON processor. 

For instance, if you wish to extract entries where `Knowledge (EN)` is set to "Humanities", the `Ability Branch` is "Common Sense", the `difficulty level` is set to 2, and there's no associated image context, you can execute the following:

```bash
jq '[.[] | select(.["Knowledge (EN)"] == "Humanities" and .["Ability Branch"] == "Common Sense" and .Level == 2 and .["Image Context"] == false)]' datasets.json > filtered_data.json
```

The `Knowledge (EN)` can be selected from 20 knowledge domains. The `Ability Branch` can be chosen from "Common Sense", "Understanding", and "Reasoning". We divide questions into 5 different difficulty levels, so you can choose a level from 1 to 5. If you want questions with an image context, you can set "Image Context" to true. Of course, you can select multiple knowledge domains, ability branches, and difficulty levels according to your needs. For more advanced selections, you can refer to [`jq`](https://github.com/jqlang/jq).

## Evaluation Execution

The `evaluate.py` script is compatible with various LLM APIs, such as:

- **OpenAI GPT series**: Set your OpenAI API key in the system environment using the following command: ```export OPENAI_API_KEY=xxxxxxxx```. For different models, such as ChatGPT and GPT-4, pass the model argument to `evaluate.py` as shown in the example below. If you're using a different OpenAI API base, such as the Azure GPT service, specify a different endpoint at the beginning of `evaluate.py` and set the system environment similarly to the API Key.

- **[Fastchat](https://github.com/lm-sys/FastChat)**: This supports numerous open-source LLMs, including LLama 2, Vicuna, Alpaca, Baize, ChatGLM, Dolly, Falcon, FastChat-T5, GPT4ALL, Guanaco, MTP, OpenAssistant, RedPajama, StableLM, WizardLM, and more.

- **[ChatGLM](https://github.com/THUDM/ChatGLM2-6B)**: Deploy a local API following the provided documentation.

For instance, when using ChatGLM, set up the [ChatGLM API](https://github.com/THUDM/ChatGLM2-6B#api-%E9%83%A8%E7%BD%B2) first. If your API endpoint is `http://10.118.0.26:8000`, run the evaluation using:

```bash
python evaluate.py -i datasets.json -o chatglm2_prompt_type_1_run_1.json --model chatglm2 --prompt "" --max_tokens 512 --temperature 1 --n 1 --endpoint http://10.118.0.26:8000
```

For LLMs that only provide web browser access, such as Ernie, Claude, and Spark, you can deploy local APIs using the [chatgpt-mirai-qq-bot API](https://github.com/lss233/chatgpt-mirai-qq-bot#-http-api).

Furthermore, `evaluate.py` is designed for easy expansion to support additional LLMs.

For a breakdown of the available arguments, run `python evaluate.py --help`. For models that don't need an endpoint, set the endpoint parameter to an empty string using `--endpoint ""`.
