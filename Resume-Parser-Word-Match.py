import fitz as pydf
import os
import shutil
import openai
import os

# OpenAI Key for API
client = openai.OpenAI(api_key='OPENAI_API_KEY')


# Skills you want to match
skills_needed = ['Python','Flask','Docker','Django', 'Canva', 'HTML', 'Python']


# Create folders if they don't exist
folders = ['accepted','rejected','undecided']

for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Match the skills in the resume
def get_match(input) -> int:
    match_count = 0
    for skill in skills_needed:
        if skill in all_text:
            match_count += 1

    return match_count/len(skills_needed)

undecided_resumes = os.listdir('undecided')
if len(undecided_resumes) == 0:
    print('No resumes to process/ Folder was just Created')
    exit()

# Get Resumes from undecided folder
for resume in undecided_resumes:

    doc = pydf.open(f'undecided/{resume}')

    all_text = ''
    for page in doc:
        all_text += page.get_text()

    name = all_text.split('\n')[0].capitalize()

    doc.close()

    all_text.lower()

    # If the match is greater than 70% move to accepted folder
    if get_match(all_text) > 0.7:
        shutil.move(src=f"undecided/{resume}",dst="accepted")
        print(f'{name} with {get_match(all_text)} was sent to accepted dir')
        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        #max_tokens= 300,
        messages=[
            {"role": "user", "content": f"Give me a brief summary of {name}, considering the resume: {resume}, matched {get_match(all_text)}% of the skills needed {skills_needed}"},
        ]
        )
        print(completion.choices[0].message.content)
    else:
        shutil.move(src=f"undecided/{resume}",dst="rejected")
        print(f'{name} with {get_match(all_text)} was sent to rejected dir')
