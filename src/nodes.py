import os
import time
from typing import Any, Dict, List, Optional, Type
from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.search import GmailSearch
from langchain_community.tools.gmail.utils import clean_email_body
import base64
import email


# Create a custom GmailSearch class to better handle decoding
class CustomGmailSearch(GmailSearch):
    def _parse_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for message in messages:
            message_id = message["id"]
            message_data = (
                self.api_resource.users()
                .messages()
                .get(userId="me", format="raw", id=message_id)
                .execute()
            )

            raw_message = base64.urlsafe_b64decode(message_data["raw"])

            email_msg = email.message_from_bytes(raw_message)

            subject = email_msg["Subject"]
            sender = email_msg["From"]

            message_body = ""
            if email_msg.is_multipart():
                for part in email_msg.walk():
                    ctype = part.get_content_type()
                    cdispo = str(part.get("Content-Disposition"))
                    if ctype == "text/plain" and "attachment" not in cdispo:
                        try:
                            message_body = part.get_payload(decode=True).decode("utf-8")
                        except UnicodeDecodeError:
                            message_body = part.get_payload(decode=True).decode("latin-1")
                        break
            else:
                try:
                    message_body = email_msg.get_payload(decode=True).decode("utf-8")
                except UnicodeDecodeError:
                    message_body = email_msg.get_payload(decode=True).decode("latin-1")

            body = clean_email_body(message_body)

            results.append(
                {
                    "id": message["id"],
                    "threadId": message_data["threadId"],
                    "snippet": message_data["snippet"],
                    "body": body,
                    "subject": subject,
                    "sender": sender,
                }
            )
        return results


class Nodes():
	def __init__(self):
		self.gmail = GmailToolkit()

	def check_email(self, state):
		print("# Checking for new emails")
		search = CustomGmailSearch(api_resource=self.gmail.api_resource)
		emails = search._run(query='is:unread', max_results=5)
		checked_emails = state['checked_emails_ids'] if state['checked_emails_ids'] else []
		thread = []
		new_emails = []
		for email in emails:
			if (email['id'] not in checked_emails) and (email['threadId'] not in thread) and ( os.environ['MY_EMAIL'] not in email['sender']):
				thread.append(email['threadId'])
				new_emails.append(
					{
						"id": email['id'],
						"threadId": email['threadId'],
						"snippet": email['snippet'],
						"sender": email["sender"]
					}
				)
		checked_emails.extend([email['id'] for email in emails])
		return {
			**state,
			"emails": new_emails,
			"checked_emails_ids": checked_emails
		}

	def wait_next_run(self, state):
		print("## Waiting for 180 seconds")
		time.sleep(180)
		return state

	def new_emails(self, state):
		if len(state['emails']) == 0:
			print("\n## No new emails")
			return "end"
		else:
			print("\n## New emails")
			return "continue"

