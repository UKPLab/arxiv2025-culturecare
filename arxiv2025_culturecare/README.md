<p align="center">
  <img src="../culturecare_logo.png" alt="Logo" height="200">
</p>
<div align="center">
    <h1 style="margin: 0">Tailored Emotional LLM-Supporter: Enhancing Cultural Sensitivity</h1>
</div>
<br clear="left"/>

## Disclaimer
This repository contains experimental software and is published for the sole purpose of giving additional background details on the respective publication.

**Important** 
This research was conducted using Reddit data.  Please make sure your read, understand and follow Reddit's policy, if you are interested in conducting research on the data:

1. https://support.reddithelp.com/hc/en-us/articles/26410290525844-Public-Content-Policy

2. https://redditinc.com/policies/data-api-terms

---

### Usage

There are two entry point scripts in this repository:

* `generation.py` for generation with an open-sourced model with different prompting strategies
* `evaluation.py` for evaluation with an open-sourced model

The experiment configuration is handled through Hydra with configuration files.
See `configs` folder for an example. The parameters are:
```
model_name: "aya-expanse-8b"
model_path: "/models--cohere-aya-expanse-8b"
data_path: "/data/{culture}_data.jsonl"
output_dir: "/outputs/responses/"
cache_dir: ""
culture: Chinese
strategy: profile
generate_cfg:
  temperature: 0.7
  max_new_tokens: 1000
```

In this configuration file, `{culture}` is one of {Arabic, Chinese, German, Jewish}, and will be filled automatically.
`strategy` is the prompting strategy, options are:

```
"redditor": The baseline prompting, role-playing a Redditor
"profile": Culture-informed role-playing by assuming a person from the same culture as the post author
"guided_without_profile": Using CCCI-R as the guideline
"annotation_without_profile": Using explicit annotation information
"guided_annotation": Combination of culture-informed role-playing, guideline and annotations, the cga strategy in our paper
```

The `data` folder contains annotations of CultureCare. 
Due to privacy and data policies, we cannot publicly release the posts.
However, *urls* are provided that you can download directly from Reddit, alternatively please contact the first authors.
The data inheres the policy of Reddit, is strictly for research purposes, and cannot be used for model training unless a separate arrangement between you and Reddit exists.

---
## Citation
If you find this repository useful, please cite the following paper:

```
@article{culturecare2025,
  author       = {Chen Cecilia Liu and
                  Hiba Arnaout and
                  Nils Kovačić and 
                  Dana Atzil-Slonim and
                  Iryna Gurevych},
  title        = {Tailored Emotional LLM-Supporter: Enhancing Cultural Sensitivity},
  note         = {Chen Cecilia Liu and Hiba Arnaout contributed equally to this work},
  journal      = {ArXiv preprint},
  volume       = { },
  year         = {2025},
  url          = { },
  doi          = { },
  eprinttype    = {arXiv},
  eprint       = { }
}
```

## Contact
https://www.ukp.tu-darmstadt.de/

https://www.tu-darmstadt.de/

Don't hesitate to send first authors an e-mail if something is broken (and it shouldn't be) or if you have further questions.
This repository contains experimental software and is published for the sole purpose of giving additional background details on the respective publication. 

## License
This repository is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for the full license text.
 