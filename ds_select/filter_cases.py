import pandas as pd

# Login using `hf auth login` to access this dataset
dataset = pd.read_parquet("hf://datasets/SAVSNET/PetEVAL/data/test-00000-of-00001.parquet")

filtered = dataset[
        (dataset["icd_label"].str.contains("Diseases of the ear or mastoid process", na=False)) &
        (dataset["disease"].str.contains("otitis|OE|ear", na=False, case=False))
    ].drop(columns=["id", "annonymisation"])

filtered.to_excel("result.xlsx", index=False)

final_reslut = filtered[filtered["sentence"].str.contains("cytology|infection|bacteria|cocci|yeast", case=False)]
final_reslut.to_excel("final.xlsx", index=False)

print(f"total count: {len(final_reslut)}")
print(final_reslut.head(10)) # first 10 rows
print("Done export to excel file!")
