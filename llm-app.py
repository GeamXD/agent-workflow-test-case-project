from crewai import Agent, Task, Process, Crew
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.llms import Ollama
import streamlit as st

##### TITLE ############################
col1, col2, col3 = st.columns(3)
with col1:
    st.write('')
with col2:
    st.title('Crew App')
with col3:
    st.write('')

# Topic that will be used in the crew run
try:
    topic = st.text_input('', placeholder='Enter interested topic')
except Exception as e:
    st.write(e)

# TOOL for searching
search_tool = DuckDuckGoSearchRun()

# Assuming you have Ollama installed and downloaded the openhermes model
ollama_openhermes = Ollama(model="openhermes")
ollama_mistral = Ollama(model='mistral')

# Button
button = st.button('Submit')

#########
if button: # Check if button was clicked
    # Define agents with roles and goals
    researcher = Agent(
        role='Senior Educational Reseacher',
        goal=f'Develop currated ideas for teaching and engaging new learners in {topic}',
        backstory="""You are an expert educational researcher with 15 years experience in developing
        ideas and strategies ofr teaching and engaging new learners. You also have a keen eye for details and make
        complex ideas simple and teachable""",
        verbose=True,
        allow_delegation=False,
        max_iter=5,
        max_rpm=5,
        llm=ollama_openhermes,
    )

    writer = Agent(
        role='Senior Education Writer',
        goal=f'craft compelling articles for new learners in {topic}',
        backstory="""You are a renowned writer in the education system, known for your
        insightul and engaging articles. With a deep understanding of the
        education system. You can transfrom complex ideas into compelling articles""",
        verbose=True,
        max_iter=5,
        max_rpm=5,
        allow_delegation=True,
        llm=ollama_openhermes,
    )

    examiner = Agent(
        role='Chief Examiner',
        goal=f'craft questions using articles from writer, to evaluate understanding of content in {topic}',
        backstory="""You are a seasoned examiner with years of experience in setting
        test questions to evaluate learners
        knowledge in various concept""",
        verbose=True,
        max_iter=5,
        max_rpm=5,
        allow_delegation=False,
        llm=ollama_openhermes,
    )

    ################ TASKS ###############################

    # Research task
    research_task = Task(
        description=f"""Identiy best ideas for teaching and engaging student in {topic}.
      Focus on identifying the easiest manner of teaching.
      """,
        tools=[search_tool],
        agent=researcher
    )

    # Writing task based on research findings
    write_task = Task(
        description=f"""Compose an explanatory article on {topic}.
        This article should be easy to understand, engaging and positive.
      """,
        expected_output=f"""A well structured article on {topic} with 
        at least 3 paragraphs""",
        tools=[search_tool],
        agent=writer
    )

    # Examiner task for setting questions
    examiner_task = Task(
        description=f"""Compose standard multi-choice questions on {topic}.
      """,
        expected_output=f"""3 Multi-choice questions on {topic}.
        Place each question on a new line.
        Answers presented in a clear and nice format under each question""",
        tools=[search_tool],
        agent=examiner
    )

    ### Process ###

    # Forming the edu-focused crew
    crew = Crew(
      agents=[researcher, writer, examiner],
      tasks=[research_task, write_task, examiner_task],
      process=Process.sequential  # Sequential task execution
    )

    # # Starting the task execution process
    with st.spinner(text="In progress"):
        result = crew.kickoff()
        st.success('Model has finished Task')


    # Returns a TaskOutput object with the description and results of the task
    st.title('Article')
    st.markdown(f"""{write_task.output.result}
    """)
    st.title('Questions')
    st.markdown(f"""{examiner_task.output.result}
    """)
else:
    pass
