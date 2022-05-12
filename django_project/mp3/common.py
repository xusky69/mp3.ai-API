import io
import json
import wave
from typing import List, Tuple

import torch
import torchaudio
from pydub import AudioSegment
from scipy.special import softmax
from transformers import (AutoModelForSequenceClassification, AutoTokenizer,
                          Speech2TextForConditionalGeneration,
                          Speech2TextProcessor)
from vosk import KaldiRecognizer, Model, SetLogLevel

SetLogLevel(-1)


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


def transcript_file_vosk(path: str,
                         model: Model,
                         ) -> dict:

    wf = mp3_to_wav(path, skip=0, cut_at=60)
    wf = wave.open(wf, "rb")

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    rec.SetPartialWords(True)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            pass
        else:
            pass

    return json.loads(rec.FinalResult())


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


def load_audio_file(file_path: str, max_duration=60, sample_rate=16000) -> torch.Tensor:
    audio, og_sample_rate = torchaudio.load(file_path)
    audio = audio[:, 0:max_duration*og_sample_rate]
    audio = torchaudio.transforms.Resample(og_sample_rate, 16000)(audio)
    return (audio, sample_rate)


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


def initialize_model_VOSK(model_path: str) -> Model:
    model = Model(model_path)
    return model


def mp3_to_wav(source: str, skip: int = 0, cut_at: int = 30, sound_rate=16000):
    '''
    based from 
    towardsdatascience.com/transcribe-large-audio-files-offline-with-vosk-a77ee8f7aa28
    '''

    if skip >= cut_at:
        assert False, "'cut_at' vakue must be greater thank 'skip' value"

    sound = AudioSegment.from_mp3(source)
    sound = sound.set_channels(1)
    sound = sound.set_frame_rate(sound_rate)

    sound = sound[skip*1000:cut_at*1000]
    # output_path = os.path.splitext(source)[0]+".wav"

    audio = io.BytesIO()
    sound.export(audio, format="wav")

    return audio
