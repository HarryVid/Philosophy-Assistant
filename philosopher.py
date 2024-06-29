from streamlit import title
from streamlit import subheader
from streamlit import markdown
from streamlit import text_input
from streamlit import columns
from streamlit import write
from streamlit import button
from streamlit import warning

from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from ollama import chat


title("Welcome to LLamalosophy!")

markdown("### What can I help you with today my dear friend?")

user_query = text_input(" ", label_visibility="collapsed")

embedding_function = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)

prompt_template_1 = PromptTemplate.from_template(
	"Answer the user's queries in a short, strightforward and concise manner."
	)

prompt_template_2 = PromptTemplate.from_template(
	"You are a calm, kind, caring and helpful philosophy assistant " \
	"who will take on the persona and role of a wise old gentleman " \
	"and answer the user in a short, sweet, strightforward and concise " \
	"yet motivating manner based on your existing knowledge base."
	)

prompt_template_3 = PromptTemplate.from_template(
	"You are a calm, kind, caring and helpful philosophy assistant " \
	"who will take on the persona and role of a wise old gentleman " \
	"and answer the user in a short, sweet, strightforward and concise " \
	"yet motivating manner based on your existing knowledge base " \
	"and use additional information and context from the following philosophy texts: \n \n {context}"
	)


if button("Submit"):
	if user_query:
		docs = db.similarity_search(user_query, k=3)
		context = "\n\n---\n\n".join(doc.page_content for doc in docs)
		prompt_1 = prompt_template_1.format()
		prompt_2 = prompt_template_2.format()
		prompt_3 = prompt_template_3.format(context=context)

		response1 = chat(model='llama3:latest', messages=[
			{
				'role': 'system',
				'content': prompt_1,
				},
			{
				'role': 'user',
				'content': user_query,
				}
			])

		response2 = chat(model='llama3:latest', messages=[
			{
				'role': 'system',
				'content': prompt_2,
				},
			{
				'role': 'user',
				'content': user_query,
				}
			])

		response3 = chat(model='llama3:latest', messages=[
			{
				'role': 'system',
				'content': prompt_3,
				},
			{
				'role': 'user',
				'content': user_query,
				}
			])

		markdown("### Responses")
		col4, col5, col6 = columns(3)
		with col4:
			subheader("Basic Response")
			write(response1['message']['content'])

		with col5:
			subheader("Prompt Engineering Response")
			write(response2['message']['content'])

		with col6:
			subheader("RAG Response")
			write(response3['message']['content'])

		markdown("### Prompts")
		col1, col2, col3 = columns(3)
		with col1:
			subheader("Basic Prompt")
			write(f"{prompt_1} \n \n {user_query}")

		with col2:
			subheader("Engineered Prompt")
			write(f"{prompt_2} \n \n {user_query}")

		with col3:
			subheader("Engineered Prompt with RAG")
			write(f"{prompt_3} \n \n {user_query}")

	else:
		warning("Please type your questions into the text box and I will do my best to help!")
