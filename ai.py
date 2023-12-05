from contextlib import redirect_stdout
import os
from os import PathLike
from typing import Any
import logging
import io
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoConfig,
    AutoTokenizer,
    BitsAndBytesConfig,
    TextStreamer,
)


CHAT_EOS_TOKEN_ID = 32002


class AI:
    def __init__(self) -> None:
        self.started = False
        self.model: Any = None
        self.tokenizer: Any = None

    def start(self, model_path: PathLike | str):
        logging.info(f"Starting the AI at '{model_path}'")
        if self.started:
            logging.warn("Stop the currently running AI before starting a new one.")
            return

        config = AutoConfig.from_pretrained(
            model_path,
            rope_scaling={
                "type": "dynamic",
                "factor": 2.0,
            },
            local_files_only=True,
        )
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            config=config,
            quantization_config=bnb_config,
            local_files_only=True,
            device_map="auto",
            load_in_4bit=True,
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.started = True

    def stop(self):
        self.started = False
        del self.model
        del self.tokenizer
        torch.cuda.empty_cache()

    def ask_ai(
        self, height: int, weight: int, sex: str, goals: str, activity: str
    ) -> str:
        if not self.started:
            logging.warn("AI have not been started yet")
            return "AI have not been started yet"

        prompt = f"I am a {sex}, my height are {height} ft, i weight {weight} pounds, my goal is to {goals} weight, and i want a {activity} activity level, please give me a personalized meal recommendations considering my profile to help me achieve my goals and support my activity. Ensure that the meals are well-balanced and aligned with my fitness objectives.\n"
        complete_prompt = (
            f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
        )

        input = self.tokenizer(complete_prompt, return_tensors="pt").to("cuda:0")
        output = self.model.generate(
            **input,
            max_new_tokens=2048,
            eos_token_id=CHAT_EOS_TOKEN_ID,
        )

        return self.tokenizer.batch_decode(output, skip_special_tokens=True)[0].replace(
            f"user\n{prompt} \n assistant\n", ""
        )


if __name__ == "__main__":
    ai = AI()
    ai.start(os.path.expanduser("~/TinyLlama"))
    print(ai.ask_ai(5, 128, "male", "maintain", "low"))
