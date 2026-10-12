Enquiry-to-Action AI Agent
----------------------------
What I created is a small web application that turns messy customer enquiries into structured data and decides what to do next. The demo is built around a made-up Melbourne home services company (HVAC/plumbing/electrical).

When someone types something like "My aircon stopped cooling, I am in werribee, call me on 0123 456 789, I'm free this weekend", the app pulls out details, figures out missing elements, and picks what to do next; either create a job, ask for more info, or flag this enquiry for human review if it comes across as too ambiguous. 

The problem
------------
Service businesses get enquiries through forms, email, chat, and phone notes. A person has to read each one and work out who the customer is, what's the problem, where they are and how to reach them, this application handles this step automatically, without forging or ignoring any information.

Why did I build an agent, and not a chatbot?
------------------------------------------------
A chatbot simply replies with text, although what i built picks from a set of three actions:
1) CREATE_JOB_REQUEST =  If there is enough information to progress the enquiry, it makes a job request.
2) ASK_FOR_MISSING_INFORMATION =  If there's something missing from the given enquiry, it asks for what is missing.
3) HUMAN_REVIEW =  if an enquiry is out of scope, too vague, it will flag this enquiry as one that needs to be reviewed manually.

The core concept: AI PROPOSES what to do, but python DECIDES what to do
-----------------------------------------------------------------------
AI figures out the messy part. Reading the message, pulling out the fields, suggesting an action. Python does the strict counterpart: checking the required fields, makes the final decision, runs the action, and handles the database.

The AI's choice is solely just a suggestion. Python rechecks the suggestion against the rules and overrides it when needed. if the AI suggests creating a job but theres no contact number, Python ignores that, and asks for the number instead to complete the enquiry. The AI cannot push through anything that breaks the rules.

How an enquiry moves
--------------------
Customer submits a message
the message/enquiry is saved to the database so its never lost
AI extracts the fields and suggests an action (in ai_service.py)
Python checks the rules and makes the decision (business_rules.py)
The chosen action runs (actions.py)
Result is then saved, and the response is shown to the customer.

What the AI handles vs. what Python handles
-------------------------------------------
The AI(ai_service.py) reads the messy/informal/typo-filled messages. It pulls out customers name, contact, suburb, issue, service type, urgency and preferred time. It also judges whether an enquiry is out of scope or too vague, and suggests a next action.
Python (business_rules.py, actions.py, database.py) checks which fields are actually present, makes the final decision on what happens, runs the action, and reads/writes to the database. The AI never gets direct access to the database.

Required fields
---------------
To create a job, an enquiry must consist of three things: a description of the problem, a suburb, and a way to contact the customer. Preferred time is optional since businesses usually arrange that on a callback. These rules are set in 'business_rules.py', they are easy to find and change

Human review
-------------
The AI is not trusted blindly. If a customer enquiry is out of scope (an example could be if the enquiry is not a home services job), it goes to a person instead of being guessed at. Also, I've added safety nets such that if the AI service fails (API down, quota hit), the app does not crash. Rather, that customer enquiry is still saved into the database and left for human review (one of the 3 actions).

Testing
--------
'test_enquiries.py' sends fake enquiries through the real pipeline and checks the decision it makes, which actions it picks, and which fields it marks as missing, rather than the AI's exact wording. The wording changes between runs, but the decisions shouldn't.
It covers complete enquiries, missing contact, missing suburb, missing both, out of scope requests, vague messages, typos, urgent wording and long/short messages.

Tech used
---------
Python + Flask
SQLite
Google Gemini called only from 'ai_service.py', I designed it such that if a developer decides to change the LLM model, he/she could do so by only changing one file.

HOW TO RUN THIS WEB APP
-----------------------
1) set up a virtual environment and install dependencies:
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt

2) create a .env file (not committed):
   GEMINI_API_KEY=your_key_here
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=your_admin_password
   FLASK_DEBUG=true

3) Run it: 
in the terminal, type: python app.py

4) Open http://127.0.0.1:5000


Known limitations of the demo
-----------------------------
The contact field checks if only something was entered, but it doesn’t validate if the phone number/email is in the correct format
the admin login uses basic auth, not a full login system
SQLite is fine for a demo but would not hold up for real scale


AI assistance
-------------
For this web app I used AI tools for debugging, code suggestions, and some research while building this. I reviewed and tested the code, and I can explain the architecture and decisions behind it.


