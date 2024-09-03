from crewai import Task
from textwrap import dedent

class EmailFilterTasks:
	def filter_emails_task(self, agent, emails):
		return Task(
			description=dedent(f"""\
				Analyze a batch of emails and filter out non-essential ones such as promotional content and 
				irrelevant notifications.
				
				Relevant emails are:
				- E-mails that require immediate attention from the user
					- Needs to be answered
					- Invites to meetings
					- User must take a specific action
					- Alerts
					  - Paid subscriptions
					  - Payments and finances in general
					  - Shopify and Printify
					  	- Orders
					  	- Payments
					  	- Refunds
					  	- New customers
					  	- New orders
					  - Potentially important alerts
				- Relevant Content
					- Newsletters and posts related to
					  - LangChain, LangGraph
					  - CrewAI, AutoGen
					  - AI Agents
					  - DeepLearningAI / Andrew Ng / The Batch
					  - Gen AI Coding tutorials
					  - AI Research Papers
					  - LLMs, Agents, and Autonomous AI
					- Product updates
					  - OpenAI API
					  - LangChain (the ecosystem)
					  - Cursor (IDE)
					  - Image Generation Models
					  - Video Generation Models
					  - New and interesting AI tools

			  	Use your expertise in email content analysis to distinguish
				relevant emails from the rest, pay attention to the sender and avoid invalid emails.

				Make sure to filter for the messages actually directed at the user and avoid notifications.

				EMAILS
				-------
				{emails}

				Your final answer MUST be a the relevant thread_ids and the sender, use bullet points.
				"""),
			agent=agent
		)

	def classify_emails_task(self, agent):
		return Task(
			description=dedent("""\
				For each email thread, pull and analyze the complete threads using only the actual Thread ID.
				understand the context, key points, and the overall sentiment of the conversation.

				Classify the emails into the following labels:
				- requires_action
				- quality_content
				- potentially_useful
				- alerts
				- ignore

				Your final answer MUST be a list for all emails with:
				- the thread_id
				- a summary of the email thread
				- a highlighting with the main points
				- identify the user and who he will be answering to
				- communication style in the thread
				- the sender's email address
				- the classification label of the email
				"""),
			agent=agent
		)

	def compile_emails_task(self, agent):
		return Task(
			description=dedent(f"""\
				Based on the relevant emails identified, generate a CSV list containing the following information for each email:
				- Email data (including sender, subject, and message body)
				- Labels, according to the previous step in the process
				- A dense summary of the email thread
				- A suggested action for each email. Possible actions are:
					- Reply
					- Study
					- Ignore
					- Other (please specify)
				Ensure that the CSV is well-formatted and includes all necessary details for further processing.

				Your final answer MUST be a confirmation that the CSV file has been created and saved successfully.
				"""),
			agent=agent
		)