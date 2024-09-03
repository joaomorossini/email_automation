import os

from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.get_thread import GmailGetThread
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import AzureChatOpenAI, ChatOpenAI

from textwrap import dedent
from crewai import Agent
from .tools import CreateCsvTool

azure_llm = AzureChatOpenAI(
    model="gpt-4o",
	temperature=0
)

class EmailFilterAgents():
	def __init__(self):
		self.gmail = GmailToolkit()

	def email_filter_agent(self):
		return Agent(
			role='Senior Email Analyst',
			goal='Filter out non-essential emails like newsletters and promotional content',
			backstory=dedent("""\
				As a Senior Email Analyst, you have extensive experience in email content analysis.
				You are adept at distinguishing important emails from spam and other irrelevant 
				content. Your expertise lies in identifying key patterns and markers that
				signify the importance of an email."""),
			verbose=True,
			allow_delegation=False,
			llm=azure_llm,
		)

	def email_classification_agent(self):

		return Agent(
			role='Email Action Specialist',
			goal='Classify emails according to their content and context',
			backstory=dedent("""\
				With a keen eye for detail and a knack for understanding context, you specialize
				in identifying emails that require immediate action and emails that contain important 
				information or useful/relevant content for professional development and growth in the AI/Tech industry.
				Your skill set includes interpreting the urgency and importance of an email based on its content and context.
				You may use Tavily to gather relevant context from the internet to help you with this task.
			"""),
			tools=[
				GmailGetThread(api_resource=self.gmail.api_resource),
				TavilySearchResults()
			],
			verbose=True,
			allow_delegation=False,
			llm=azure_llm,
		)

	# def email_response_writer(self):
	# 	return Agent(
	# 		role='Email Response Writer',
	# 		goal='Draft responses to action-required emails',
	# 		backstory=dedent("""\
	# 			You are a skilled writer, adept at crafting clear, concise, and effective email responses.
	# 			Your strength lies in your ability to communicate effectively, ensuring that each response is
	# 			tailored to address the specific needs and context of the email."""),
	# 		tools=[
	# 			TavilySearchResults(),
	# 			GmailGetThread(api_resource=self.gmail.api_resource),
	# 			CreateDraftTool.create_draft
	# 		],
	# 		verbose=True,
	# 		allow_delegation=False,
	# 		llm=azure_llm,
	# 	)

	def email_compiler_agent(self):
		return Agent(
			role='Email Response Writer',
			goal='Draft responses to action-required emails',
			backstory=dedent("""\
				You are an expert in understanding emails, summarizing content, and suggesting appropriate actions.
				Your strength lies in your ability to analyze email content effectively, ensuring that each summary
				and suggested action is tailored to address the specific needs and context of the email."""),
			tools=[
				TavilySearchResults(),
				GmailGetThread(api_resource=self.gmail.api_resource),
				CreateCsvTool.create_csv
			],
			verbose=True,
			allow_delegation=False,
			llm=azure_llm,
		)