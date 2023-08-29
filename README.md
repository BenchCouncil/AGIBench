# AGIBench

AGIBench stands for a multi-granularity, multimodal, human-referenced, auto-scoring benchmark tailored for large language models. This repository hosts the dataset utilized by AGIBench.

The `datasets.json` file comprises 927 instances. Each instance features a question, its associated options, the correct answer, human-referenced accuracy, reason, difficulty level, ability branch, knowledge domain, modality information, and more.

## Extract Data

To extract data tailored to your benchmarking requirements, you can employ [`jq`](https://github.com/jqlang/jq), a versatile command-line JSON processor. 

For instance, if you wish to extract entries where `Knowledge (EN)` is set to "Humanities", the `Ability Branch` is "Common Sense", the `difficulty level` is set to 2, and there's no associated image context, you can execute the following:

```bash
jq '[.[] | select(.["Knowledge (EN)"] == "Humanities" and .["Ability Branch"] == "Common Sense" and .Level == 2 and .["Image Context"] == false)]' datasets.json > filtered_data.json
```
## Evaluation Execution

The `evaluate.py` script is compatible with various LLM APIs, such as:
- OpenAI GPT series
- [Fastchat](https://github.com/lm-sys/FastChat)
- [ChatGLM](https://github.com/THUDM/ChatGLM2-6B)

It's designed for easy expansion to accommodate additional LLMs.

For instance, using ChatGLM, first set up the [ChatGLM API](https://github.com/THUDM/ChatGLM2-6B#api-%E9%83%A8%E7%BD%B2). Assuming your API endpoint is `http://10.118.0.26:8000`, execute the evaluation:

```bash
python evaluate.py -i datasets.json -o chatglm2_prompt_type_1_run_1.json --model chatglm2 --prompt "" --max_tokens 512 --temperature 1 --n 1 --endpoint http://10.118.0.26:8000
```

For a breakdown of argument specifics, use `python evaluate.py --help`. For models that don't require an endpoint, set the endpoint parameter to an empty string: `--endpoint ""`.
