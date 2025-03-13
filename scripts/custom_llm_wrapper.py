import time

from langchain_openai import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback
from langchain.schema   import SystemMessage, HumanMessage

class ChatCustom:
  def __init__(self, model, temperature, top_p, max_tokens):
    openai_api_key = "EMPTY"
    openai_api_base = "http://localhost:8000/v1"
    self.llm = ChatOpenAI(
      model       = model,
      temperature = temperature,
      top_p       = top_p,
      max_tokens  = max_tokens,
      api_key=openai_api_key,
      base_url=openai_api_base,
    )

#     full_prompt = full_prompt.replace("""\
# Only output the code snippet
# and do NOT output anything else.""", "")

  def chat(self, system_msg, full_prompt):
    msgs = [ SystemMessage(system_msg), HumanMessage(full_prompt) ]
    for _ in range(10):
      try:
        with get_openai_callback() as cb:
          resp = self.llm.invoke(msgs)
          break
      except Exception as e:
        print("")
        print("ERROR: LLM query failed, retrying in 20 seconds")
        print(f"{type(e)}")
        print(f"{e}")
        print("")
        time.sleep(20)

    resp.content = resp.content.replace("[END]", "[DONE]")
    return resp, cb
