# Combined app.py with Streamlit UI and scraping logic
import streamlit as st
import requests
from bs4 import BeautifulSoup
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import HumanMessage, SystemMessage
from openai import OpenAI

if 'current_report' not in st.session_state:
    st.session_state.current_report = ""

if 'previous_report' not in st.session_state:
    st.session_state.previous_report = ""

# Define the scraping function
def scrape_site(url):
    try:
        # Fetch the content from the URL
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract the text of the body of the page
            body = soup.find('body')
            if body:  # Check if the body tag was found
                return ' '.join(body.stripped_strings)  # Return the text content of the body
            else:
                return "Body tag not found in the HTML content."
        else:
            return f"Failed to retrieve the webpage. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"


# Streamlit UI for app navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose the app mode",
                                ["Materiality Report Generator", "SustainabilityGPT"])

if app_mode == "Materiality Report Generator":
    # Streamlit UI elements
    st.title('Materiality Report Generator')
    url_input = st.text_input('Enter the URL to scrape')

    chat = ChatOpenAI(temperature=0, openai_api_key=st.secrets["apiKey"])

    if st.button('Scrape'):
        # Call the scrape_site function and display the result
        data = scrape_site(url_input)

        messages = [
        SystemMessage(
            content= "Given the body text of a website, you are an expert in understanding what the company does and who are the potential stakeholders"
        ),
        HumanMessage(
            content= "Given the following body text of a website:\n" + data + "\nExtract what the company does and who are the potential stakeholders in the following format:\n\nDescription: detailed description of the company\nStakeholders: list of potential stakeholders for the company"
        ),
        ]
        print(chat(messages).content)
        st.success('Information Sucessfully Gathered!')
        company_info = chat(messages).content

        messages = [
            SystemMessage(
            content= "You are a sustainability expert. Given the description of a company and the list of stakeholders, you use your vast experience to create a materiality report to advice the senior management on potential business strategies. You create reports in markdown"
            ),
            HumanMessage(
            content= "Generate a materiality assessment report (markdown format) for the following company:\n" + company_info + "\n\nUse the following format for the report: \n\n"

    + "1. Executive Summary\n"
    + "Provide a brief overview of the materiality assessment process and its objectives. Summarize the key findings and material topics identified, including objectives like identifying key environmental, social, and governance risks, refining sustainability strategy, informing wider business strategy, engaging with internal or external stakeholders, and identifying areas for target setting to improve business and sustainability performance. Reflect on the audience for the materiality process and define what ‘materiality’ means for the organization.\n\n"

    + "2. Introduction\n"
    + "Explain the purpose of the materiality assessment and define what 'materiality' means for the organization, considering the importance of topics to stakeholders, the impact of topics in the value chain, and their strategic relevance. Outline the organizational scope, considering regions, business units, and the entire value chain. Discuss how the outcome will feed into reporting.\n\n"

    + "3. Methodology\n"
    + "Detail the approach taken for the materiality assessment, including creating a long list of potential material topics from sources such as media reporting, internal data, external peer review, and sector-specific regulations. Discuss the involvement of different teams beyond the sustainability team for a more in-depth understanding, the inclusion of areas of opportunity in addition to risks, and the focus on impactful external stakeholder engagement.\n\n"

    + "4. Material Topics Identified\n"
    + "List all the material topics identified during the assessment. Explain the source of each material topic and why it is considered material for the organization, focusing on a comprehensive review of media reports, internal data, and insights from peer reviews and sector-specific standards.\n\n"

    + "5. Categorization of Material Topics\n"
    + "Outline the process of clustering topics into a limited number of higher-level categories appropriate to the unit of assessment. Ensure that the categories are consistent and align with existing terminology, strategy, and policies used by the company. Describe the specific risk or opportunity for each material topic clearly.\n\n"

    + "6. Prioritization of Material Topics\n"
    + "Explain the criteria and process used for prioritizing topics, including identifying relevant business functions and stakeholders involved in the prioritization, using a developed methodology to score each topic, assessing stakeholder views, and setting a threshold for defining material topics. Focus on assessing the economic, social, and environmental impact of each topic on the company’s value.\n\n"

    + "7. Business Strategies\n"
    + "Interpret the materiality assessment results in the context of the organization's current strategy. Propose detailed business strategies based on the insights from the report, including risk management strategies, opportunity exploration, innovation and development suggestions, stakeholder engagement strategies, and performance targets. Reflect on how the prioritized material topics can inform business strategies and contribute to sustainability performance.\n\n"

    + "8. Proposed Innovation Project\n"
    + "Outline a comprehensive corporate entrepreneurship project aimed at bolstering the company's sustainability initiatives. This project should integrate innovative solutions, sustainable practices, and strategic partnerships to enhance the company's environmental, social, and governance (ESG) performance.\n\n"

        + "8.1 Project Overview [3-4 lines]\n"
        + "Provide a brief summary of the project, including its name, objectives, and the primary sustainability challenge it aims to address. Highlight the project's alignment with the company's overall sustainability goals and corporate strategy.\n\n"

        + "8.2 Problem Statement [3-4 lines]\n"
        + "Define the specific environmental or social issue the project targets. Detail the current impact of this issue on the company and its stakeholders, supported by relevant data and insights derived from the materiality assessment.\n\n"

        + "8.3 Innovation and Technology [6-7 lines]\n"
        + "Describe the innovative technologies or practices the project will employ to tackle the identified problem. Explain how these technologies are sustainable, their potential impact on the environment, and any technological partnerships or collaborations.\n\n"

        + "8.4 Sustainability Goals [6-7 lines]\n"
        + "Outline the sustainability goals of the project, including measurable targets related to waste reduction, energy efficiency, carbon footprint reduction, resource conservation, or social welfare improvements. Explain how these goals contribute to the company's long-term sustainability vision.\n\n"

        + "8.5 Stakeholder Engagement [6-7 lines]\n"
        + "Detail the plan for engaging key stakeholders, including employees, customers, suppliers, local communities, and regulators, throughout the project's lifecycle. Discuss how stakeholder feedback will be incorporated into the project development and implementation phases.\n\n"

        + "8.6 Impact Assessment [10-12 lines]\n"
        + "Describe the methodology for assessing the project's impact on the company's sustainability performance and stakeholder value. Include both qualitative and quantitative metrics for evaluating success, and how the project's outcomes will be reported and communicated.\n\n"

        + "8.7 Challenges and Solutions [6-7 lines]\n"
        + "Identify potential challenges and obstacles that might arise during the project's implementation, along with proposed solutions or mitigation strategies. Consider aspects such as regulatory compliance, technological limitations, market acceptance, and internal capacity building.\n\n"

        + "8.8 Future Opportunities [3-4 lines]\n"
        + "Explore future opportunities for scaling up the project or leveraging its outcomes for broader sustainability initiatives within the company. Discuss how the project could serve as a model for innovation and sustainability in the industry.\n\n"

    + "9. Sustainability Score\n"
    + "Based on your assessment, give the company a sustainability score out of 10. Explain your reasoning for the score."

    + "10. Conclusion\n"
    + "Summarize the materiality assessment process, its outcomes, and the importance of the identified material topics and proposed strategies. Reflect on the impact of the identified material topics on the organization's future strategy and operations.\n\n"

            ),
        ]
        # Display the report in Streamlit instead of printing
        report_content = chat(messages).content  # Get the report content from the chat model
        st.session_state.current_report = report_content
        st.markdown("## Materiality Assessment Report")  # Header for the report
        st.markdown(report_content)  # Display the report using markdown for formatting
        st.text_area("Scraped Text", data, height=300)  # Using text_area to display large amount of text

elif app_mode == "SustainabilityGPT":

    print("hello")

    st.title("SustainabilityGPT")

    client = OpenAI(api_key=st.secrets["apiKey"])

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4-0125-preview"

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "You are a sustainability expert. Based on your expertise you answer user's questions and assign sustainability scores to companies based on their materiality sustainability reports. You always provide your reasons for the scores you assign to companies."}]

    if st.session_state.current_report != "" and st.session_state.current_report != st.session_state.previous_report:
        st.session_state.messages.append({"role": "user", "content": "Answer questions based on this report:\n" + st.session_state.current_report})
        st.session_state.previous_report = st.session_state.current_report

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Say Something"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
