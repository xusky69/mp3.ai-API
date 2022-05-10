from typing import List, Tuple

import torch
from transformers import (Speech2TextForConditionalGeneration,
                          Speech2TextProcessor)


def initialize_model_processor(model_name: str,
                               processor_name: str) -> Tuple[Speech2TextForConditionalGeneration, Speech2TextProcessor]:
    model = Speech2TextForConditionalGeneration.from_pretrained(model_name)
    processor = Speech2TextProcessor.from_pretrained(processor_name)
    return (model, processor)


def transcript_file(data: torch.Tensor,
                    sampling_rate: int,
                    model: Speech2TextForConditionalGeneration,
                    processor: Speech2TextProcessor) -> List[str]:

    model_input = processor(data,
                            sampling_rate=sampling_rate,
                            return_tensors="pt")
    model_output = model.generate(model_input["input_features"],
                                  attention_mask=model_input["attention_mask"])
    transcription = processor.batch_decode(model_output)

    return transcription
