# Multi-Modal Chatbot

# This is a terminal based multi-modal chatbot that leverages OpenAI APIs and Langchain to provide 
# a versatile interaction experience. Users can upload images and documents in various formats 
# such as PDF, Word, Excel, and text, and ask questions about the content of these images/documents.

# Author: Abhimanyu Bhatnagar

import textract
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv
import base64
import cv2
# import httpx


#Number of previous conversations to remember. User prompt and the following output together count for 2 conversations
CONTEXT_LENGTH = 12
#Loading of evironment variables
load_dotenv()
#Getting OPEN_API_KEY env variable
OPEN_API_KEY = os.getenv('OPEN_API_KEY')

def document_processor():
	#Taking path of file from user
	path = input("Give the path of the file you want to upload\n")
	text = textract.process(path)
	#list to store previous interactions
	previous_conversations = []

	#Temperature: Parameter to control how creative the model is with range from 0 to 1 with 1 being most creative.
	llm = ChatOpenAI(temperature=0.5,model_name='gpt-4o',max_tokens=4096,openai_api_key=OPEN_API_KEY)
	conversation = ConversationChain(llm=llm)
	#Initially this prompt and the document is sent to the llm
	initial_prompt = """ Read the text following thoroughly. Answer the questions that follow taking
					     this information into account. The text is:"""
	prompt = "{} {}".format(initial_prompt,text)
	answer = conversation.predict(input=prompt)
	#Store the prompt sent and the response receieved from the llm
	previous_conversations.append(prompt)
	previous_conversations.append(answer)
	while True:
		#First two being stored as document/image is there. Limiting the previous conversations that are sent to the llm.
	    conv_history = None
	    if len(previous_conversations) > CONTEXT_LENGTH:
	    	  conv_history = previous_conversations[0:2] + previous_conversations[-CONTEXT_LENGTH:]
	    else:
	    	conv_history = previous_conversations.copy()
	    #Storing the previous conversations in memory variable
	    memory_size = len(conv_history)
	    memory = ConversationBufferWindowMemory(k= memory_size)
	    for i in range(0, len(conv_history) - 1, 2):
	        memory.save_context({"input": conv_history[i]}, {"output": conv_history[i + 1]})
	    memory.load_memory_variables({})
	    #Starting a conversation with memory of previous conversations
	    conversation = ConversationChain(llm=llm,memory=memory)
	    user_question = input("Enter your question or enter 'exit' to terminate the program\n")
	    if user_question == "exit":
	        break	    
	    answer = conversation.predict(input=user_question)
	    print(f'\n{answer}')
	    previous_conversations.append(user_question)
	    previous_conversations.append(answer)

def image_processor():
	previous_conversations = []
	model = ChatOpenAI(model="gpt-4o",api_key=OPEN_API_KEY)

	#Taking an image and converting it into the required data format. 
	path = input("Give the path of the image you want to upload\n")
	#Reading the image
	image = cv2.imread(path) 
	jpg_img = cv2.imencode('.jpg', image)
	imageconv_history = base64.b64encode(jpg_img[1]).decode('utf-8')
	content = [
		{
		    "type": "image_url",
			"image_url": {"url": f"data:image/jpeg;base64,{imageconv_history}"},
		},
		{"type": "text", "text": "Human: Answer questions based on the image"},
	] 
	message = HumanMessage(content=content)
	#Initial instruction to llm to analyze the image data and answer following questions
	response = model.invoke([message])
	#Converting the response to a string object
	response_string = response.pretty_repr()
	#Appending the first interaction to the conversation history.
	previous_conversations = content.copy()
	previous_conversations.append({"type": "text", "text": f'AI: {response_string}'})
	while True:
		user_question = input("Enter your question or enter 'exit' to terminate the program\n")
		if user_question == "exit":
			break
		#limiting the previous conversation size. 3 to include the ai response as well to the intiial 2 instructions.
		if(len(previous_conversations) > CONTEXT_LENGTH):
			trimmed_content = previous_conversations[:3] + previous_conversations[-CONTEXT_LENGTH:]
		else:
			trimmed_content = previous_conversations.copy()
		user_text =  {"type": "text", "text": 'Human: {}'.format(user_question)}
		trimmed_content.append(user_text)
		message = HumanMessage(content = trimmed_content)
		
		response = model.invoke([message])
		response_string = response.pretty_repr()
		print(response_string)

		previous_conversations.append(user_question)
		previous_conversations.append({"type": "text", "text": f'AI: {response_string}'})

def menu():
	choice= int(input("Enter 1 if you want to upload a document, enter 2 if you want to upload an image\n"))
	# Get the context data for the conversion from the database
	if(choice == 1):
		document_processor()

	if(choice == 2):
		image_processor()

if __name__ == '__main__':
	menu()

