DICTIONARY = {
    "topical": "medicines used locally on the outside of the body",
    "systemic": "medicines reaches and has an effect on the whole of a body",
    "cytology": "the exam of a single cell type, often used to diagnose or screen for disease",
    "malassezia": "a naturally occurring fungus (organisms) that lives on the skin",
    "yeast": "a type of fungus (organisms)",
    "cocci": "a spherical-shaped bacterium",
    "combination medication": "an ear drop that contains two or more active medications",
    "smear": "a diagnostic test from a sample of ear discharge",
    "swab": "a procedure uses a small cotton bud to take a sample of fluid or discharge from ear canal",
    "bacteria": "tiny organisms (living things) that have only one cell",
    "antibiotic": "medicines used to treat or prevent bacterial infections",
    "antifungal": "medicines used to kill funguses or prevent them from growing",
    "steroid": "medicines used to reduce redness and swelling and stop the body's immune system attacking itself",
    "inflammation": "a red, painful, and often swollen area in or on a part of the body",
    "long-acting": "medications designed to release slowly into the bloodstream",
    "daily dosing": "medications on a strict once or multi-dose for a day"
}

def filter_terms(text):
    text_lower = text.lower()
    result = {}
    
    for term, explanation in DICTIONARY.items():
        term_lower = term.lower()
        if term_lower in text_lower:
            result[term] = explanation
            
    return result