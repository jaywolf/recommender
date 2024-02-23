# Prompt template for the model
# <|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n
#
def format_prompt_with_template(user_prompt):
  return f"[INST]{user_prompt}[/INST]Assistant</s>"
