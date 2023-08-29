# AGIBench

AGIBench stands for a multi-granularity, multimodal, human-referenced, auto-scoring benchmark tailored for large language models. This repository hosts the dataset utilized by AGIBench.

The `datasets.json` file comprises 927 instances. Each instance features a question, its associated options, the correct answer, human-referenced accuracy, reason, difficulty level, ability branch, knowledge domain, modality information, and more.

## Extract Data

To extract data tailored to your benchmarking requirements, you can employ [`jq`](https://github.com/jqlang/jq), a versatile command-line JSON processor. 

For instance, if you wish to extract entries where `Knowledge (EN)` is set to "Humanities", the `Ability Branch` is "Common Sense", the `difficulty level` is set to 2, and there's no associated image context, you can execute the following:

```bash
jq '[.[] | select(.["Knowledge (EN)"] == "Humanities" and .["Ability Branch"] == "Common Sense" and .Level == 2 and .["Image Context"] == false)]' datasets.json > filtered_data.json
```