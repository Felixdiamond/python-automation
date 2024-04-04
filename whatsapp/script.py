import pywhatkit
import pathlib
import textwrap

import google.generativeai as genai

from rich.console import Console
from rich.markdown import Markdown

GOOGLE_API_KEY= 'AIzaSyAfc74s_ARa5vHr4GVi0VEUHJjvk_R5F4E'

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')
console = Console()



def generate_text(prompt):
  master_prompt = """
    Your role is to act as an interpreter that translates user requests into executable PyWhatKit code. 
    Here are some examples of user requests and the corresponding PyWhatKit code:

    1. 'Generate code to send a WhatsApp message to +1234567890 saying "I love you."'
       Response: 'pywhatkit.sendwhatmsg("+1234567890", "I love you", 0, 0)'

    2. 'Generate code to send a WhatsApp message to +1234567890 saying "Meeting at 10 AM" at 9 AM.'
       Response: 'pywhatkit.sendwhatmsg("+1234567890", "Meeting at 10 AM", 9, 0)'

    3. 'Generate code to play a YouTube video "Despacito".'
       Response: 'pywhatkit.playonyt("Despacito")'

    4. 'Generate code to search "Python programming" on Google.'
       Response: 'pywhatkit.search("Python programming")'

    5. 'Generate code to find information about "Elon Musk".'
       Response: 'pywhatkit.info("Elon Musk")'

    6. 'Generate code to send a WhatsApp message to +1234567890 saying "Happy Birthday!"'
       Response: 'pywhatkit.sendwhatmsg("+1234567890", "Happy Birthday!", 0, 0)'

    7. 'Generate code to play a YouTube video "Python tutorial".'
       Response: 'pywhatkit.playonyt("Python tutorial")'

    8. 'Generate code to search "Machine learning" on Google.'
       Response: 'pywhatkit.search("Machine learning")'

    9. 'Generate code to find information about "Albert Einstein".'
       Response: 'pywhatkit.info("Albert Einstein")'

    10. 'Generate code to send a WhatsApp message to +1234567890 saying "See you at the party" at 8 PM.'
        Response: 'pywhatkit.sendwhatmsg("+1234567890", "See you at the party", 20, 0)'

    11. 'Generate code to play a YouTube video "Meditation music".'
        Response: 'pywhatkit.playonyt("Meditation music")'

    12. 'Generate code to search "Data science" on Google.'
        Response: 'pywhatkit.search("Data science")'

    13. 'Generate code to find information about "Isaac Newton".'
        Response: 'pywhatkit.info("Isaac Newton")'

    14. 'Generate code to send a WhatsApp message to +1234567890 saying "Good luck for the exam".'
        Response: 'pywhatkit.sendwhatmsg("+1234567890", "Good luck for the exam", 0, 0)'

    15. 'Generate code to play a YouTube video "Workout routine".'
        Response: 'pywhatkit.playonyt("Workout routine")'

    16. 'Generate code to search "Artificial intelligence" on Google.'
        Response: 'pywhatkit.search("Artificial intelligence")'

    17. 'Generate code to find information about "Ada Lovelace".'
        Response: 'pywhatkit.info("Ada Lovelace")'

    18. 'Generate code to send a WhatsApp message to +1234567890 saying "Let's catch up soon".'
        Response: 'pywhatkit.sendwhatmsg("+1234567890", "Let's catch up soon", 0, 0)'

    19. 'Generate code to play a YouTube video "Cooking recipe".'
        Response: 'pywhatkit.playonyt("Cooking recipe")'

    20. 'Generate code to search "Quantum computing" on Google.'
        Response: 'pywhatkit.search("Quantum computing")'

    For this task, the user request is 'Generate code to {}'. Generate the corresponding PyWhatKit code. Remember, no additional conversation or clarification is needed. Your response should be purely in code form.
""".format(prompt)
  response = model.generate_content(master_prompt)
  return response.text
#   md = Markdown(response.text)
#   return md

def cus_pr(text):
    md = Markdown(text)
    console.print(md)

def main():
    cus_pr("# Welcome to whatsapp automation, made by Felix.")
    cus_pr("## What do you want to do?")
    cus_pr("- Send a message (1)")
    cus_pr("- Set an automatic message (2)")
    cus_pr("- Exit (3)")
    text = int(input("Choose a number: "))
    if text == 1:
        prompt = input("Enter a prompt: ")
        command = generate_text(prompt)
        # print(command)
        exec(command)
    elif text == 2:
        print("Checking pending messages...")
        pywhatkit.sendwhatmsg_instantly("+4915735988371", "Hello, I am a bot. I am currently not available. I will get back to you as soon as possible.")
        print("Message sent!")
    elif text == 3:
        print("Exiting...")
        exit()