from typing import List, Tuple

import torch
import torchaudio
from scipy.special import softmax
from transformers import (AutoModelForSequenceClassification, AutoTokenizer,
                          Speech2TextForConditionalGeneration,
                          Speech2TextProcessor)


def initialize_model_processor_S2T(model_name: str,
                                   processor_name: str) -> Tuple[Speech2TextForConditionalGeneration, Speech2TextProcessor]:
    model = Speech2TextForConditionalGeneration.from_pretrained(model_name)
    processor = Speech2TextProcessor.from_pretrained(processor_name)
    return (model, processor)


def initialize_model_tokenizer_SENT(model_name: str,
                                    tokenizer_name: str) -> Tuple[AutoModelForSequenceClassification, AutoTokenizer]:
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    return (model, tokenizer)


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


def analyze_sentiment(sentence: str,
                      model: AutoModelForSequenceClassification,
                      tokenizer: AutoTokenizer) -> dict:
    '''
    Labels: 0 -> Negative; 1 -> Neutral; 2 -> Positive
    '''
    encoded_input = tokenizer(sentence, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    return scores


def load_audio_file(file_path: str) -> torch.Tensor:
    return torchaudio.load(file_path)


def split_words(words: str) -> str:
    return [item.strip().lower() for item in words.split(',') if len(item.strip()) > 0]


def get_word_freq(word_list: list, sentence: str) -> dict:

    word_freq = {}

    for word in sentence.strip().split(' '):
        if word not in word_freq.keys() and word in word_list:
            word_freq[word] = 1
        elif word in word_list:
            word_freq[word] += 1
        else:
            pass

    return word_freq
