import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# API and model used
load_dotenv()
client = OpenAI()
MODEL = "gpt-5.4-mini"

# prompt, schema, tree, principle and note files
FILEBASE = Path(__file__).parent

def read_file(file_name) -> dict:
    return (FILEBASE / file_name).read_text(encoding="utf-8")

def read_json(file_name) -> dict:
    return json.loads(read_file(file_name))
                     
PHASE1_PROMPT = read_file("prompt1.txt")
PHASE2_PROMPT = read_file("prompt2.txt")
PHASE3_PROMPT = read_file("prompt3.txt")

SAMPLE_CASE = read_file("demo/case_2.txt")
FOIL_TREE = read_file("tree.md")
PRINCIPLE_TABLE = read_json("principle.json")

SCHEMA1 = read_json("schema1.json")
SCHEMA2 = read_json("schema2.json")
SCHEMA3 = read_json("schema3.json")

# phase 1 - extract features from vet notes
def feature_extraction(text_note) -> dict:
    return api_response(text_note, PHASE1_PROMPT, SCHEMA1)

# phase 2 - select foil types
def foil_selection(p1_result) -> dict:
    prompt = PHASE2_PROMPT.replace("{{tree}}", FOIL_TREE)
    return api_response(p1_result, prompt, SCHEMA2)

# phase 3 - output two types of explanations
def explanation_generation(p2_result) -> dict:
    for foil in p2_result["foils"]:
        branch = foil["branch_taken"]
        principle = PRINCIPLE_TABLE[branch]
        # insert principle texts for both explanations
        foil["causal_text"] = principle["causal_text"]
        foil["contrast_text"] = principle["contrast_text"]
        # remove "traversal_trace" label (content for decision verification)
        foil.pop("traversal_trace", None)

    return api_response(p2_result, PHASE3_PROMPT, SCHEMA3)

# helper functions
def save_to_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def api_response(data, prompt, schema):
    if isinstance(data, dict):
        data = json.dumps(data, ensure_ascii=False)

    response = client.responses.create(
        model = MODEL,
        reasoning = { "effort": "low" },
        input = [
            { "role": "developer", "content": prompt },
            { "role": "user", "content": data }
        ],
        text = {
            "format": {
                "type": "json_schema",
                "name": schema["name"],
                "schema": schema["schema"],
                "strict": schema["strict"],
            }
        },
    )
    return json.loads(response.output_text)

# pipeline
def run_pipeline(note, case_id, output_dir):
    phase1 = feature_extraction(note)
    save_to_json(phase1, output_dir / f"{case_id}_p1.json")
    phase2 = foil_selection(phase1)
    save_to_json(phase2, output_dir / f"{case_id}_p2.json")
    phase3 = explanation_generation(phase2)
    save_to_json(phase3, output_dir / f"{case_id}_p3.json")

    return "Prompt pipeline completed"

# main
if __name__ == "__main__":
    final_result = run_pipeline(SAMPLE_CASE, "case_2", (FILEBASE / "outputs"))
    print(final_result)
