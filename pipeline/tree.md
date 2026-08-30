# DECISION TREE
| node | input field | branches | dependency |
| ----- | ----- | ----- | ----- |
| Gate1 | disease_type | externa(continue) / media(exit) / interna(exit) | none |
| Gate2 | duration_evidence | acute <7d(continue) / subacute 7-30d(continue) / chronic >30d(exit) | Gate1 = externa |
| Step0 | disease_type, ear_condition, treatment_mentioned | topical(Foil0) / systemic(continue, no foil) | Gate2 = acute or subacute |
| Step1 | cytology_result | no_infection(Foil1) / malassezia(Foil2) / cocci(Foil2b) / rods(exit) | Step0 finished |
| Step2 | pain_evidence, ear_condition, treatment_mentioned | relieve_first(Foil3, then exit) / direct_treatment(Foil3, continue) | Step1 finished |
| Step3 | treatment_mentioned, final_delivery | daily(Foil4) / long_acting(Foil4) | Step2 finished |

# FOIL OPPONENTS (rejected_alternative for each foil is DEFINED here, not inferred)
| foil_type | branch_taken | rejected_alternative | foil_contrasts |
| ----- | ----- | ----- | ----- |
| Foil0 | topical | systemic | topical vs systemic |
| Foil1 | no_infection | antimicrobial | steroid-only vs antimicrobial |
| Foil2 | malassezia | antibiotic_only | combination product vs antibiotic-only |
| Foil2b | cocci | antibiotic_only | combination product vs antibiotic-only |
| Foil3 | relieve_first | direct_treatment | relieve first vs direct treatment |
| Foil3 | direct_treatment | relieve_first | direct treatment vs relieve-first |
| Foil4 | daily | long_acting | daily-dosing vs long-acting |
| Foil4 | long_acting | daily | long-acting vs daily-dosing |

# FOIL QUESTIONS
- Foil0: "Why treat the infection with topical medication instead of systemic (oral/injectable) antibiotics?"
- Foil1: "Why steroid only, no antimicrobial medication?"
- Foil2/Foil2b: "Why combination product, not antibiotic medication?"
- Foil3: phrase by what the vet did FIRST - "Why relieve first instead of direct treatment?" or the opposite
- Foil4: phrase by what was FINALLY chosen - "Why daily dose instead of long-acting medicine?" or the opposite

# DISAMBIGUATION RULES (apply exactly)
1. Foil0: Foil0 is mandatory, do NOT skip it
    [CRITERIA] Was the primary treatment delivered LOCALLY (topical application directly into the ear)?
    - Yes: (Topical) If the clinical note never explains why systemic medication was avoided, set evidence_status = "not_in_note" and note_evidence = "insufficient_info"
    - No: (Systemic only) The systemic branch produces NO foil
2. Foil3: This is based on a checkable fact, NOT on severity level.
    [CRITERIA_1] Was a SYSTEMIC anti-inflammatory drug (e.g., oral prednisolone or methylprednisolone) administered BEFORE any affected-site treatment?
    [CRITERIA_2] What was the actual SEQUENCE of actions taken by the vet?
    - Decision = "relieve_first": ONLY when [CRITERIA_1] is true AND the note shows the systemic anti-inflammatory was administered FIRST
    - Decision = "direct_treatment": When no such prior systemic anti-inflammatory step exists (the vet treated the ear site directly)
    [EXCLUSIONS] (Force to "direct_treatment", do NOT count as "relieve_first"):
    - Ear flushing/clean-out/cytology: These are routine clinical steps, NOT "relieve_first"
3. Foil4:
    - When Step2 = relieve_first, the Step3 decision (daily vs long_acting) belongs to a FUTURE visit. Do NOT produce Foil4 for a relieve_first case, stop after Foil3.
    - When MULTIPLE delivery options are discussed, do NOT mark ambiguous. Decide by what was FINALLY administered, prescribed, or set as the explicit follow-up plan.
