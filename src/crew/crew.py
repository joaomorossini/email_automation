from crewai import Crew

from .agents import EmailFilterAgents
from .tasks import EmailFilterTasks

class EmailFilterCrew():
	def __init__(self):
		agents = EmailFilterAgents()
		self.filter_agent = agents.email_filter_agent()
		self.classification_agent = agents.email_classification_agent()
		self.compiler_agent = agents.email_compiler_agent()

	def kickoff(self, state):
		print("### Filtering emails")
		tasks = EmailFilterTasks()
		crew = Crew(
			agents=[self.filter_agent, self.classification_agent, self.compiler_agent],
			tasks=[
				tasks.filter_emails_task(self.filter_agent, self._format_emails(state['emails'])),
				tasks.classify_emails_task(self.classification_agent),
				tasks.compile_emails_task(self.compiler_agent)
			],
			verbose=True
		)
		result = crew.kickoff()
		return {**state, "action_required_emails": result}

	def _format_emails(self, emails):
		emails_string = []
		for email in emails:
			print(email)
			arr = [
				f"ID: {email['id']}",
				f"- Thread ID: {email['threadId']}",
				f"- Snippet: {email['snippet']}",
				f"- From: {email['sender']}",
				f"--------"
			]
			emails_string.append("\n".join(arr))
		return "\n".join(emails_string)