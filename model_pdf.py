import subprocess
import os

import re
import streamlit as st
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Load templates from JSON file
def load_templates():
    try:
        with open("templates.json", "r") as f:
            templates = json.load(f)
    except FileNotFoundError:
        templates = {}
    return templates

# Save templates to JSON file
def save_templates(templates):
    with open("templates.json", "w") as f:
        json.dump(templates, f)

def generate_question_paper(question_types, num_mcq, num_3_marks, num_5_marks, total_marks, selected_option):
    # Generate question paper using Generative AI
    # Placeholder function, actual implementation would depend on the AI model
    
    # Dummy implementation
    
    question_paper = "Question Paper\n\n"
    for question_type in question_types.items():
        question_paper += f"Type: {question_type}\n"
        question_paper += f"Number of Questions: {num_mcq+num_3_marks + num_5_marks}\n"
    question_paper += f"Total Marks: {total_marks}\n"
    question_paper += f"Difficulty: {selected_option}"
    return question_paper

def download_pdf(question_paper):
    # Generate PDF and initiate download
    c = canvas.Canvas("Question_Paper.pdf", pagesize=letter)
    c.drawString(100, 750, question_paper)
    c.save()
    st.success("Question Paper PDF generated and downloaded!")

def main():
    st.title("Question Paper Generator")

    # Load templates
    templates = load_templates()
    selected_template = st.selectbox("Select Template", ["Custom"] + list(templates.keys()), index=0)
    select_difficulty = ["Easy", "Medium", "Hard"]

    if selected_template == "Custom":
        # Sidebar options for custom template
        st.header("Question Type")  # Making the title smaller

        question_types = {
            "MCQ": st.checkbox("MCQ"),
            "Descriptive": st.checkbox("Descriptive")}
        if question_types["MCQ"]:
                num_mcq = st.slider("Number of MCQ", min_value=0, max_value=20, value=1)
        else:   
                num_mcq = 0
        num_3_marks = st.slider("Number of 3-marks Questions", min_value=0, max_value=20, value=1)
        num_5_marks = st.slider("Number of 5-marks Questions", min_value=0, max_value=20, value=1)
        total_marks = num_mcq+(num_3_marks*3)+(num_5_marks*5)
        st.text(f"Total Marks {num_mcq+(num_3_marks*3)+(num_5_marks*5)}")
        selected_option = st.selectbox('Difficulty level', select_difficulty)

        # Validate if at least one checkbox is checked for question type
        if not any(question_types.values()):
            st.error("Please select at least one question type.")
            return
      

        # # Save current configuration as template
        # customize_template = st.text_input("Customize Template Name")
        # if customize_template:
        #     templates[customize_template] = {
        #         "question_types": question_types,
        #         "num_mcq": num_mcq,
        #         "num_3_marks": num_3_marks,
        #         "num_5_marks": num_5_marks,
        #         "total_marks": total_marks,
        #         "selected_option": selected_option
        #     }
        #     save_templates(templates)
        #     st.success("Template saved successfully!")
    else:
        # Load selected template
        template = templates[selected_template]
        question_types = template["question_types"]
        num_mcq = template["num_mcq"]
        num_3_marks = template["num_3_marks"]
        num_5_marks = template["num_5_marks"]
        total_marks = template["total_marks"]
        selected_option = template["selected_option"]
    
    # Generate question paper on button click
    if st.button("Generate Question Paper"):
        selected_question_types = {key: value for key, value in question_types.items() if value}
        question_paper = generate_question_paper(selected_question_types, num_mcq, num_3_marks, num_5_marks, total_marks, selected_option)
        with open("request.json", "r") as json_file:
            data = json.load(json_file)
        question = f"generate {total_marks} marks question paper in which {num_mcq} mcq questions with weightage of 1 mark, {num_3_marks} questions with weightage of 3 marks and {num_5_marks} questions with weightage of 5 marks."
        data["contents"]["parts"][1]["text"] = question
        with open("request.json", "w") as json_file:
            json.dump(data,json_file)
        st.text(question_paper)



        # if st.button("Download as pdf"):

        file = "response.txt"
        if os.path.exists(file):
            os.remove(file)
            print("File delete")
        command = r'''
        curl -X POST     -H "Authorization: Bearer $(gcloud auth print-access-token)"     -H "Content-Type: application/json; charset=utf-8"     -d @request.json     "https://us-central1-aiplatform.googleapis.com/v1/projects/team-synthify/locations/us-central1/publishers/google/models/gemini-1.0-pro:streamGenerateContent?alt=sse" -o response.txt
        '''
        subprocess.run(command,shell=True)

        
        with open("response.txt", "r") as file:
            content = file.read()

            # Split the content by "data: " to separate each JSON object
            json_strings = content.split("data: ")[1:]

        # Initialize an empty list to store the "text" fields
        texts = []
        # Iterate over each JSON object string
        for json_string in json_strings:
                # Load the JSON object
                data = json.loads(json_string)
                # Extract the "text" field from each "parts" list
                for candidate in data["candidates"]:
                        for part in candidate["content"]["parts"]:
                            texts.append(part["text"].strip())

        # Concatenate the "text" fields into a single string
        result_string = " ".join(texts)

        st.text(result_string)
        # with open("response.txt", "r") as txt_file:
        #     for line in txt_file.readlines():
        #         if len(line) == 0:
        #             continue
        #         result += line[71:].split('"}]},"')[0]
        # #print("result ",result.replace("\n"," "))
        # writefile(result)
        # printstr()
        # st.text(resu lt)
        
        
def writefile(result):
    with open("result.txt", "w") as file:
    # Write the text into the file
        file.write(result)
        # print()
            # st.text()
            # download_pdf(question_paper)
def printstr():
    with open("result.txt", "r") as file:
        content = file.read()
        print(content)

# Remove newline characters using regular expression
    #content_without_newline = re.sub(r'\n', '', content)

# Print or write the modified content back to the file
   # print(content_without_newline)



if __name__ == "__main__":
    # res = "**Multiple Choice Questions (1 mark each)**\n\n1. Which of the following is not a tetrahedral hybrid orbital?\n    (a) sp3\n    (b) sp2\n    (c) sp\n    (d) sp3d\n\n2. Which of the following molecules has a π bond?\n    (a) CH4\n    (b) C2H4\n    (c) C2H6\n    (d) C6H6\n\n3. What is the IUPAC name of the compound CH3CH(CH3)-CH2-COOH?\n    (a) 2-Methylbutanoic acid\n    (b) 3-Methylbutanoic acid\n    (c) 2-Methylpentanoic acid\n    (d) 3-Methylpentanoic acid\n\n4. Which of the following is an electrophile?\n    (a) CH3NH2\n    (b) AlCl3\n    (c) Na+\n    (d) CH3OH\n\n5. Which of the following reactions is an elimination reaction?\n    (a) CH3CH2Br + NaOH → CH3CH2OH + NaBr\n    (b) CH3COOH + NaOH → CH3COONa + H2O\n    (c) CH3CH2CH2Cl + KOH(aq) → CH3CH=CH2 + KCl + H2O\n    (d) CH3CHO + HCN → CH3CH(OH)CN\n\n6. Which of the following techniques is used to separate a mixture of volatile liquids?\n    (a) Crystallisation\n    (b) Distillation\n    (c) Chromatography\n    (d) Sublimation\n\n7. Which of the following is a secondary alcohol?\n    (a) CH3CH2OH\n    (b) (CH3)2CHOH\n    (c) (CH3)3COH\n    (d) CH3CH2CHO\n\n8. Which of the following elements is detected by Lassaigne's test?\n    (a) Nitrogen\n    (b) Phosphorus\n    (c) Chlorine\n    (d) Oxygen\n\n9. Which of the following organic compounds contains a basic group?\n    (a) Ethanol\n    (b) Acetic acid\n    (c) Methylamine\n    (d) Glycerol\n\n10. Which of the following organic compounds is an isomer of the compound CH3CH2CHO?\n    (a) CH3COCH3\n    (b) CH3CH(OH)CH3\n    (c) CH3OCH3\n    (d) CH3CH2CH2OH\n\n**Short Answer Questions (3 marks each)**\n\n1. Describe the hybridisation of carbon atoms in the compound ethene.\n2. Draw the structural formula of the compound 2,3-dimethylbutanal.\n3. What is the difference between an electrophile and a nucleophile?\n4. Explain the mechanism of an SN2 reaction.\n5. Describe the principle of paper chromatography.\n6. How can you estimate the percentage of nitrogen in an organic compound using Kjeldahl's method?\n7. What is resonance? Explain with the help of a suitable example.\n8. Describe the electromeric effect.\n9. Explain why alcohols have higher boiling points than alkanes.\n10. What is the role of a catalyst in an organic reaction?\n11. Describe the mechanism of an electrophilic aromatic substitution reaction.\n12. What is the difference between a sigma bond and a pi bond?\n\n**Long Answer Questions (5 marks each)**\n\n1. Draw the complete structural formula of the compound 2-chloro-3-methylhexane. Identify the functional group present in this compound.\n2. Describe the three main types of structural isomers with the help of suitable examples.\n3. Explain the inductive effect and show how it influences the acidity of organic acids.\n4. Describe the mechanism of a free radical substitution reaction.\n5. Explain the principles of distillation and discuss its applications.\n6. Describe the qualitative analysis of an organic compound containing nitrogen, sulphur, and chlorine using Lassaigne's test.\n7. What is the principle of quantitative analysis? Explain the estimation of carbon and hydrogen in an organic compound using Dumas' method.\n8. Describe the mechanisms of the following reactions:\n    (a) CH3CH2Br + KOH(aq) → CH3CH2OH + KI\n    (b) CH3COOH + CH3CH2OH → CH3COOCH2CH3 + H2O\n    (c) CH3CH=CH2 + HBr → CH3CHBrCH3\n9. Discuss the various methods used for the purification of organic compounds.\n10. Explain the concept of isomerism in organic chemistry. Give suitable examples to illustrate different types of isomers."
    # print(res)
    # exit()
    # file = "response.json"
    # if os.path.exists(file):
    #     os.remove(file)
    #     print("File delete")
    # command = r'''
    # curl -X POST     -H "Authorization: Bearer $(gcloud auth print-access-token)"     -H "Content-Type: application/json; charset=utf-8"     -d @request.json     "https://us-central1-aiplatform.googleapis.com/v1/projects/team-synthify/locations/us-central1/publishers/google/models/gemini-1.0-pro:streamGenerateContent?alt=sse" -o response.json
    # '''
    # subprocess.run(command,shell=True)
    # question = f"generate 50 marks organic chemistry question paper in which 10 mcq questions with weightage of 1 mark, 10 questions with weightage of 3 marks and 5 questions with weightage of 5 marks"

    # with open("request.json", "r") as json_file:
    #     data = json.load(json_file)
    # data["contents"]["parts"][1]["text"] = question
    # with open("request.json", "w") as json_file:
    #     json.dump(data,json_file)
    # print(tmp)
    main()
    
