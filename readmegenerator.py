import streamlit as st
import openai
openai.api_key = "abcdddd"

def generate_readme(input_code):
    prompt = f"Generate a README file for the following code:\n\n{input_code}\n\n"
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=400,
        n=1,
        stop=None,
        temperature=0.7
    )

    readme_description = response['choices'][0]['text']
    return readme_description

def main():
    st.title('Code to README Generator')
    code_input = st.text_area('Enter your code here:', height=400)

    if st.button('Generate README'):
        if code_input.strip() == '':
            st.warning('Please enter some code.')
        else:
            readme_content = generate_readme(code_input)
            st.write('### README:')
            st.write(readme_content)

if __name__ == "__main__":
    main()
