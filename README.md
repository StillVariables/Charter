# Charter
Hackathon Project: ChatBot

Goal
---
The aim of this application is to demonstrate ChatBot using open banking API's for customer queries related to branch, ATM, account details and balances with interative communication channel using open source libraries and tools.

### Prerequisites:-
The prerequisites for developing and understanding a chatbot
1. Python should be installed. You can download from [here](https://www.python.org/downloads/)
2. Microsoft Build tools with Visual C++ 14.0 should be installed. [Download Link](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
3. Pycharm (Python Editor) to edit the scripts, can be downloaded from [here](https://www.jetbrains.com/pycharm/download/#section=windows)
4. Node.js runtime Framwork should be installed for executing API calls. Can be installed from [here](https://nodejs.org/en/download/)
5. Install Anaconda from [here](https://www.anaconda.com/products/individual)

### Modules
##### Bot Modules
Rasa is an open source machine learning framework for building contextual AI assistants and chatbots.
Rasa has two main modules:
1. NLU for understanding user messages.
2. Core for holding conversations and deciding what to do next.
##### API Modules
Node.js is an open-source, JavaScript runtime environment that executes JavaScript code. It provides web server to execute and call the open banking API's.


###  Implementation:
#### API
1. Create a folder which will contain scripts.
2. Open the code in IDE and run the commands in Terminal. Alternatively (if IDE is not available), go to command prompt and traverse to the folder using ```cd``` command. Post the below commands Node server will be up and running to access the API's.
```nowrap
npm install
npm run start
```
#### BOT
1. Create a new folder for your chatbot project.
2. Open that folder using Pycharm
3. Create a new environment for your chatbot project from pycharm or from anaconda prompt.
4. Run the command ```pip install rasa``` for installing all the rasa dependencies.
5. Run the command ```pip install spacy``` for installing spacy library.
6. Then enter the following commands:
     ```nowrap
     python -m spacy download en
     python -m spacy download en_core_web_md
     python -m spacy link en_core_web_mden
     ```
7.   After all this command run successfully, enter the command ```rasa init``` and for all the subsequent actions choose Y (for training the model etc).
8.   You’ll then end up with all the predefined structures which RASA would have built.
9.   Open the ‘nlu.md’ file from the data folder and enter desired intents: This file is used to create all the intents and their sample utterances for conversation.
10.  Open the ‘domain.yml’ and register the newy added intet (This file is used to configure  the bot responses).
11.  Open the ‘stories.md’ file from the data folder (This file is used to create the conversation flows).
12.  After all this, you can just enter the command ```rasa train``` to train the model with new conversation elements.
13.  Charter(bot) is ready.

### Communication channel Integration:-
1.  Download ngrok from https://ngrok.com/download
2.  After extracting the zip file, open the ngrok file and run it.
3.  In ngrok, enter the command ```ngrok http 5005```: ngrok provide tunnel IP, copy the URL: ```https://<<ngrokurl>>.io```
4.  Then go to telegram and create your own bot using Botfather:
     1.	Open the telegram app and search for botfather (it is an inbuilt bot used to create other bots).
     2.	Start a conversation with botfather and enter ```/newbot``` to create a newbot.
     3.	Give a name to your bot.
     4.	Give a username to your bot, which must end with ```_bot```.This generates an access token.
5.  Open ‘credentials.yml’ inside bot  and enter:
    ```nowrap
    telegram:
    access_token:"obtained from telegram"
    verify:"your bot username"
    webhook_url:"https://<ngrokurl>/webhooks/telegram/webhook" 
	(ngrok url should be same URL which is coming once we have ngrok http 5005)
	```
6.  Go to Pycharm terminal and enter the command.
	```nowrap
	rasa run 
	```
7.  Open one more terminal and run the command.
	```nowrap
	rasa run actions
	```
8.  Now, you can chat with your bot from Telegram.
