from huggingface_hub import hf_hub_download
import pandas as pd
from llama_cpp import Llama
import datetime

N_CTX = 4096
end = datetime.datetime.today()
start = datetime.datetime.today() + datetime.timedelta(days=-7)



model_name_or_path = "TheBloke/Llama-2-7B-chat-GGML"
model_basename = "llama-2-7b-chat.ggmlv3.q4_0.bin" # the model is in bin format
model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)

# GPU
lcpp_llm = Llama(
    model_path=model_path,
    n_threads=2, # CPU cores
    n_batch=512, # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
    n_gpu_layers=43, # Change this value based on your model and your GPU VRAM pool.
    n_ctx=N_CTX, # Context window
)

text = pd.read_csv("corpus.csv")
text['received_at'] = pd.to_datetime(text['received_at'])
text = text[(text['received_at']>=start) & (text['received_at']<=end)]
text['n_tokens'] = text["text"].apply(lambda x :len(lcpp_llm.tokenizer().encode(x)))