import streamlit as st
import ollama

st.title("The Recommender")

# Layout first and last name inputs into side-by-side columns
name_col1, name_col2 = st.columns(2)
with name_col1:
    student_firstname = st.text_input("First name:", placeholder="First name")
with name_col2:
    student_lastname = st.text_input("Last name:", placeholder="Last name")

# Layout applying for and to do inputs into side-by-side columns
applying_col1, applying_col2 = st.columns(2)
with applying_col1:
    applying_for = st.text_input("Applying for:", placeholder="Example: grad school")
with applying_col2:
    do_what = st.text_input("To do:", placeholder="Example: to study Technology and Media")

# Mapping of class IDs to names and descriptions
class_descriptions = {
    'DES117': "Interaction Design 1 - Students design and create basic static websites in HTML and CSS from scratch",
    'DES157A': "Interaction Design 2 - Students design and build dynamic web projects in HTML, CSS and JavaScript",
    'DES157B': "Interaction Design 3 - Students complete a full UI/UX development process and create a capstone interactive project that demonstrates the skill learned in interaction design classes",
    'DES112': "User Interface / User Experience - Students study UI/UX processes and design interfaces for the web and create interactive prototypes for apps"
}

# Multiselect for "Classes taken:"
classes_taken = st.multiselect(
    'Classes taken:',
    options=list(class_descriptions.keys()),  # Display class IDs
    format_func=lambda x: x  # Display only class IDs in the dropdown
)

# Text area for pasting in paragraphs of text
additional_info = st.text_area("Additional information:", placeholder="Provide any additional information here.")

# Function to send information to Ollama and get a response
def get_llm_response(first_name, last_name, class_ids, additional_info):
    # Prepare class information without IDs
    classes_info = [f"{class_descriptions[class_id].split(' - ')[0]}: {class_descriptions[class_id].split(' - ')[1]}" for class_id in class_ids]
    
    prompt = (f"Please write a recommendation letter for {first_name} {last_name}, "
              f"applying for {applying_for} to {do_what}. "
              f"The student has completed the following coursework: {'; '.join(classes_info)}. "
              "The recommendation should be concise, focusing on the student's achievements and abilities as demonstrated through their coursework. "
              "Use the course names and descriptions as reference. Keep the recommendation letter to a maximum of 4 paragraphs. Do not include a letter header or footer. Do not include Dear or Sincerely. Just provide the body of the letter. "
              f"Additional context: {additional_info}")

    stream = ollama.chat(
        model='openchat',
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )
    
    recommendation = ""
    try:
        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                recommendation += chunk['message']['content']
            if 'end' in chunk:
                break
    except StopIteration:
        pass

    return recommendation

# Button to trigger the recommendation process
if st.button("Get Recommendation"):
    if not classes_taken:
        st.error("Please select at least one class.")
    elif not student_firstname or not student_lastname:
        st.error("Please enter both first and last names.")
    else:
        recommendation = get_llm_response(student_firstname, student_lastname, classes_taken, additional_info)
        st.text_area("Recommendation:", value=recommendation, height=600)
