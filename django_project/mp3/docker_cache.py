import json
import os
from pathlib import Path

from dotenv import load_dotenv

from common import initialize_model_tokenizer_SENT

if __name__ == "__main__":

    load_dotenv('.env')

    SENT_MODEL = os.getenv('SENT_MODEL')
    SENT_TKNZR = os.getenv('SENT_TKNZR')

    (sent_model, sent_tokenizer) = initialize_model_tokenizer_SENT(model_name=SENT_MODEL,
                                                                   tokenizer_name=SENT_TKNZR)

    print('finished downloading model')
