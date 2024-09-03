import os
from datetime import datetime
from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.create_draft import GmailCreateDraft
from langchain.tools import tool


class CreateCsvTool():
  @tool("Create CSV")
  def create_csv(data):
    """
    	Useful to create and save CSV files.
    	The input to this tool should be a string formatted as CSV.
    	"""
    # Create the output directory if it doesn't exist
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate the filename based on the current date and time
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M_email_analysis.csv")
    file_path = os.path.join(output_dir, filename)
    
    # Write the CSV data to the file
    with open(file_path, 'w') as file:
      file.write(data)
    
    return f"\nCSV created: {file_path}\n"
  

# class CreateDraftTool():
#   @tool("Create Draft")
#   def create_draft(data):
#     """
#     	Useful to create an email draft.
#       The input to this tool should be a pipe (|) separated text
#       of length 3 (three), representing who to send the email to,
#       the subject of the email and the actual message.
#       For example, `lorem@ipsum.com|Nice To Meet You|Hey it was great to meet you.`.
#     """
#     email, subject, message = data.split('|')
#     gmail = GmailToolkit()
#     draft = GmailCreateDraft(api_resource=gmail.api_resource)
#     result = draft({
# 				'to': [email],
# 				'subject': subject,
# 				'message': message
# 		})
#     return f"\nDraft created: {result}\n"




