import streamlit as st
import ollama
import json
from prompt_template import format_prompt_with_template

# Load descriptions from a JSON file
with open('descriptions.json', 'r') as file:
    descriptions = json.load(file)

st.title("The Recommender")

# Model to use for the recommendation
model = 'openchat'

# Input fields for user information
name_col1, name_col2 = st.columns(2)
with name_col1:
    firstname = st.text_input("First name:", placeholder="First name")
with name_col2:
    lastname = st.text_input("Last name:", placeholder="Last name")

applying_col1, applying_col2 = st.columns(2)
with applying_col1:
    applying_for = st.text_input("Applying for:", placeholder="Example: grad school")
with applying_col2:
    goal_purpose = st.text_input("Goal:", placeholder="Example: to study Technology and Media")

# Multiselect for qualifications
qualifications = st.multiselect(
    'Qualifications:',
    options=list(descriptions.keys()),
    format_func=lambda x: f"{x} - {descriptions[x].split(' - ')[0]}"
)

# Text area for additional information
additional_info = st.text_area("Additional information:", placeholder="Provide any additional information here.")

# Function to get the response from Ollama using the formatted prompt
def get_llm_response(firstname, lastname, applying_for, goal_purpose, qualifications, additional_info):
    user_prompt = (
        "You are a helpful assistant who writes concise recommendations. "
        "The recommendation must not exceed four paragraphs in length. "
        "Do not include header or footer. Do not address or sign the recommendation. "
        "Just write the body of the recommendation. "
        f"Write a recommendation for {firstname} {lastname}, "
        f"who is applying for {applying_for} to {goal_purpose}. "
        f"The person for whom the recommendation is being written has enhanced their skillset with the follows: {'; '.join([descriptions[q] for q in qualifications])}. "
        "Include the achievements and abilities demonstrated through their qualifications as context. "
        f"Use the following additional context for writing the recommendation: {additional_info}"
    )

    # Format the prompt with the template
    formatted_prompt = format_prompt_with_template(user_prompt)

    # Adjust options as needed
    options = {
        'seed': -1
    }

    # Get the response from Ollama
    stream = ollama.chat(
        model=model,
        messages=[{'role': 'user', 'content': formatted_prompt}],
        options=options,  # Include the options dictionary here
        stream=True
    )

    # Extract the recommendation from the stream
    recommendation = ""
    for chunk in stream:
        if 'message' in chunk and 'content' in chunk['message']:
            recommendation += chunk['message']['content']
        if 'end' in chunk:
            break
    return recommendation

# Button to trigger the recommendation generation
if st.button("Get recommendation"):
    if not qualifications:
        st.error("Please select at least one qualification.")
    elif not firstname or not lastname:
        st.error("Please enter both first and last names.")
    else:
        with st.spinner("Generating recommendation..."):
            recommendation = get_llm_response(firstname, lastname, applying_for, goal_purpose, qualifications, additional_info)
        st.markdown(f"**Recommendation:**\n\n{recommendation}")
