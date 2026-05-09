from app.llm import generate_response

prompt = "Explain Java programming in one sentence."

response = generate_response(prompt)

print("\nLLM RESPONSE:\n")
print(response)