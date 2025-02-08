from openai import OpenAI

client = OpenAI(api_key="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")

def generate_ad_script(influencer, product):
    prompt = f"Generate a 30-second advertisement script where {influencer} promotes {product}. The tone should be casual, friendly, and engaging."
    response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
    script_content = response.choices[0].message.content  # ✅ Corrected line
    
    # ✅ Save the script to a file
    with open("ad_script.txt", "w") as file:
        file.write(script_content)
    
    return script_content

# Generate ad script and save it
script = generate_ad_script("Ed Sheeran", "Nike Air Force sneakers")
print("Ad script saved to 'ad_script.txt'")

