import json
import os
from pathlib import Path

from dotenv import load_dotenv
from common import (analyze_sentiment, get_word_freq,
                            initialize_model_processor_S2T,
                            initialize_model_tokenizer_SENT, load_audio_file,
                            split_words, transcript_file)

if __name__ == "__main__":

    load_dotenv('.env')

    # SPEECH 2 TEXT MODEL
    S2T_MODEL = os.getenv('S2T_MODEL')
    S2T_PROCESSOR = os.getenv('S2T_PROCESSOR')

    # SENTIMENT ANALYSIS MODEL
    SENT_MODEL = os.getenv('SENT_MODEL')
    SENT_TKNZR = os.getenv('SENT_TKNZR')

    (s2t_model, s2t_processor) = initialize_model_processor_S2T(model_name=S2T_MODEL,
                                                                processor_name=S2T_PROCESSOR)

    (sent_model, sent_tokenizer) = initialize_model_tokenizer_SENT(model_name=SENT_MODEL,
                                                                   tokenizer_name=SENT_TKNZR)

    print('finished downloading models')
