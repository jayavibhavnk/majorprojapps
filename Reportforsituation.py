import streamlit as st
import openai
openai.api_key="abcdd"
def generate_report(type_report, input_code):
    # OpenAI API key

    # Prompt for OpenAI
    prompt = f"Generate a {type_report} report of the following code:\n\n{input_code}\n\n"

    # Call OpenAI API to generate report
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.4
    )

    # Extract and return the generated report
    report = response['choices'][0]['text']
    return report

def main():
    st.title('Code Report Generator')

    # Text area for users to input their code
    code_input = st.text_area('Enter your code here:', height=400)

    # Text area for users to input the type of report they want
    type_report = st.text_input('Enter the type of report:', 'README')

    if st.button('Generate Report'):
        if code_input.strip() == '':
            st.warning('Please enter some code.')
        else:
            generated_report = generate_report(type_report, code_input)
            st.write(f'### {type_report.capitalize()} Report:')
            st.write(generated_report)

if __name__ == "__main__":
    main()
