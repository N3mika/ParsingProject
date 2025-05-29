import os
import ast
import json
import time
import pandas as pd
from tqdm import tqdm
from openai import OpenAI

# === SETUP ===
os.environ['OPENAI_API_KEY'] = "your-api-key-here"  # Replace securely with your api_key before running
client = OpenAI()

# === CONFIGURATION ===
INPUT_CSV_PATH = "path_to_input_file.csvv"
OUTPUT_CSV_PATH = "path_to_output_file.csv"
PROMPT_FILE = "prompt_instructions_guarani.txt"

# === SYSTEM PROMPT ===
sys_text = "You're a Spanish-Guarani linguistic tagger. Your job is to correctly tag various linguistic components of a Spanish-Guarani code-switch sentence. Make use of the instructions provided to you in the use prompt."

# === LOAD PROMPT ===
with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    base_prompt_text = f.read()

# === GPT CALL FUNCTION ===
def call_gpt(sentence):
    prompt_text = base_prompt_text + f"\nSentence: {sentence}\nOutput:"
    response = client.chat.completions.create(
        model="gpt-4.1-2025-04-14",
        messages=[
            {"role": "system", "content": sys_text},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0,
        max_tokens=3000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content

# === MAIN ===
def main():
    df = pd.read_csv(INPUT_CSV_PATH)
    df['tokens_info'] = df['tokens_info'].apply(ast.literal_eval)

    gptresponse = []

    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing Sentences"):
        sentence_id = row['sentence_id']
        sentence = row['sentence']
        tokens_info = row['tokens_info']
        has_emoji = row['has_emoji']

        try:
            gpt_response = call_gpt(sentence)
            start_idx = gpt_response.find('[')
            end_idx = gpt_response.rfind(']') + 1

            if start_idx == -1 or end_idx == -1:
                print(f"Cannot find valid JSON brackets for sentence_id {sentence_id}")
                continue

            cleaned_response = gpt_response[start_idx:end_idx]

            try:
                gpt_response_list = json.loads(cleaned_response.strip())
            except Exception as e:
                print(f"JSON parsing error for sentence_id {sentence_id}: {e}")
                continue

            gpt_by_id = {}
            for token in gpt_response_list:
                tid = token.get("ID")
                gpt_by_id.setdefault(tid, []).append(token)

            for token_info in tokens_info:
                token_id, token_text, lang_tag = token_info
                gpt_tokens_for_id = gpt_by_id.get(token_id, [])

                if not gpt_tokens_for_id:
                    print(f"No GPT token matched for token_id {token_id} in sentence_id {sentence_id}")
                    continue

                for gpt_token in gpt_tokens_for_id:
                    gptresponse.append({
                        "sentence_id": sentence_id,
                        "has_emoji": has_emoji,
                        "sentence": sentence,
                        "gpt_response": gpt_response,
                        "token_id": token_id,
                        "token": token_text,
                        "lang_tag": lang_tag,
                        "ID": gpt_token.get("ID"),
                        "FORM": gpt_token.get("FORM"),
                        "LEMMA": gpt_token.get("LEMMA"),
                        "UPOS": gpt_token.get("UPOS"),
                        "HEAD ID": gpt_token.get("HEAD ID"),
                        "HEAD": gpt_token.get("HEAD"),
                        "DEPREL": gpt_token.get("DEPREL")
                    })

            pd.DataFrame(gptresponse).to_csv(OUTPUT_CSV_PATH, index=False)
            time.sleep(1)

        except Exception as e:
            print(f"Error processing sentence_id {sentence_id}: {e}")
            continue

if __name__ == "__main__":
    main()
