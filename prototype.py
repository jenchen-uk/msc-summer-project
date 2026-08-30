import streamlit as st
import json
# import related files
import pipeline
import style
import terms

# load css style
style.custom_style()

st.set_page_config(layout="wide", page_title="Owners Portal")

NAV_TAGS = [":material/home: Home", ":material/pets: My Pet", ":material/article: Records", ":material/book_4: Guidance", ":material/logout: Logout"]
CARD_LABEL = ["How the medicine is given?", "Which medicine was used?", "When treatment starts?", "How often it's given?"]
SAMPLE_CASE = ["case_1", "case_2"]
EXPLANATION_TYPE = ["causal", "contrastive"]
FAKE_PETS_NAME = ["Oscar", "Sophia"]

def load_case(case_id):
    note_text = pipeline.read_file(f"demo/{case_id}.txt")
    with open(f"demo/{case_id}.json", encoding="utf-8") as file:
        pipeline_result = json.load(file)

    return note_text, pipeline_result

def render_terms(result):
    st.write(":orange[**:material/manage_search: What These Words Mean?**]")
    st.caption("// Simple explanations of the medical terms //")

    foil_list = result["explanations"]
    output = {}
    for foil in foil_list:
        term_list = terms.filter_terms(foil[switch_type])
        output.update(term_list)
    with st.container(border=True, key="term_container", height="stretch"):
        for term, explanation in output.items():
            st.write(f"**{term}** - {explanation}")

def render_note(text):
    with st.container(horizontal=True):
        st.write(":material/keep: **What the Vet Wrote?**")
        st.space("stretch")
        st.write(":grey[Uploaded date: 2026/7/18]")
    
    st.caption("// The clinic's original note for your pet, exactly as written //")
        
    with st.container(border=True, key="note_container"):
        st.write(text)
    
    st.text_area("Owner's self-notes:", height="stretch")
    with st.container(horizontal_alignment="right"):
        st.button("Save")

def render_explanation(result, type):
    if switch_case == "case_1":
        name = FAKE_PETS_NAME[0]
    else:
        name = FAKE_PETS_NAME[1]
    
    st.badge(f":material/search: Quick overview of {name}'s condition")
    st.info(result["summary"])
    st.write("Some things you might be wondering about this treatment:")

    cols = st.columns(3)
    foil_list = zip(CARD_LABEL, result["explanations"])
    index = 0
    for label, foil in foil_list:
        if foil["node"] != "Step2":
            with cols[index]:
                with st.container(height="stretch", border=True, key=f"col_{index}"):
                    st.write(f":blue-background[**{label}**]")
                    st.write(foil[type])
            index += 1

def render_case(case_id):
    note_text, pipeline_result = load_case(case_id)
    if switch_type:
        render_explanation(pipeline_result, switch_type)

    st.divider()

    col1, col2 = st.columns([2, 3])
    with col1:
        render_terms(pipeline_result)
    with col2:
        render_note(note_text)
  
# sidebar
switch_case = st.sidebar.radio("sample case", SAMPLE_CASE)
st.sidebar.divider()
switch_type = st.sidebar.radio("explanation type", EXPLANATION_TYPE)

# page content
cols = st.columns(6, vertical_alignment="bottom")

logo_col, *nav_cols = cols
with logo_col:
    st.image("pic/logo.png", width="stretch")

nav_list = zip(nav_cols, NAV_TAGS)
for col, tag in nav_list:
    with col:
        st.button(tag, width="stretch", key=f"btn_{tag}")

st.divider()
with st.container(horizontal=True):
    if switch_case == "case_1":
        name = FAKE_PETS_NAME[0]
    else:
        name = FAKE_PETS_NAME[1]

    st.markdown(f"> Records > {name} > **2026/7/18**")
    st.space("stretch")
    st.button(":material/settings: settings", type="tertiary")

if switch_case:
    render_case(switch_case)

st.divider()

flex_box = st.container(horizontal=True, horizontal_alignment="left")
with flex_box:
    st.button("Print report")
    st.button("Share Content :material/share:")
    st.button("Arrange recheck :material/calendar_month:", key="styled")
    st.button("Email to vet :material/forward_to_inbox:", type="primary")
    st.space("stretch")
    st.button("support@ownersportal.co.uk", type="tertiary", key="mail")
    st.button(":material/help: Help", type="tertiary")

st.write("")
st.write(":grey[:material/copyright: 2026 Paws Veterinary Clinic]")
