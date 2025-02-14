import json
from typing import Generator, Union

from llama_cpp import Llama

llama = Llama.from_pretrained(
    repo_id="bartowski/NuExtract-1.5-smol-GGUF",
    version="main",
    filename="NuExtract-1.5-smol-Q8_0.gguf",
    n_ctx=16384,
    verbose=False,
)


def predict(text: str, template: str, max_new_tokens: int = 4_000) -> str:
    template = json.dumps(json.loads(template), indent=4)
    prompt = (
        f"""<|input|>\n### Template:\n{template}\n### Text:\n{text}\n\n<|output|>"""
    )
    output = llama(prompt, max_tokens=max_new_tokens)
    return json.loads(output["choices"][0]["text"])


def extract(text: Union[str, list[str]]) -> Generator[dict, None, None]:
    if isinstance(text, str):
        text = [text]
    for t in text:
        yield predict(t, template)


if __name__ == "__main__":
    text = """We introduce Mistral 7B, a 7–billion-parameter language model engineered for
    superior performance and efficiency. Mistral 7B outperforms the best open 13B
    model (Llama 2) across all evaluated benchmarks, and the best released 34B
    model (Llama 1) in reasoning, mathematics, and code generation. Our model
    leverages grouped-query attention (GQA) for faster inference, coupled with sliding
    window attention (SWA) to effectively handle sequences of arbitrary length with a
    reduced inference cost. We also provide a model fine-tuned to follow instructions,
    Mistral 7B – Instruct, that surpasses Llama 2 13B – chat model both on human and
    automated benchmarks. Our models are released under the Apache 2.0 license.
    Code: <https://github.com/mistralai/mistral-src>
    Webpage: <https://mistral.ai/news/announcing-mistral-7b/>"""

    template = """{
        "Model": {
            "Name": "",
            "Number of parameters": "",
            "Number of max token": "",
            "Architecture": []
        },
        "Usage": {
            "Use case": [],
            "Licence": ""
        }
    }"""
    for i in extract(text):
        print(i)
