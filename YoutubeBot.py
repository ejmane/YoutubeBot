import openai
import wikipedia
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# pass the api key
openai.api_key = os.environ.get('OPENAI_API_KEY')

# get user input
Video_URL = input("Input video URL: ") # Take the video URL
Video_ID = Video_URL.split("=")[1] # Take the Video ID from the URL
txt_formatted = TextFormatter().format_transcript(YouTubeTranscriptApi.get_transcript(Video_ID)) # Get the transcript

# define prompt
prompt = 'Write a in depth summary of the following text that summarizes the entire passage: ' + txt_formatted[:4097]
messages = []
messages.append({'role': 'system', 'content': 'You are a helpful person that wants to ensure the person you are talking to gains a thorough understanding'})
messages.append({'role': 'user', 'content': prompt})

def add_to_txt(input):
    # Open the file in append & read mode ('a+')
    with open("YoutubeBot_Response.txt", "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0 :
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(input)

try:
    # make an api call
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=messages)

    # print the response
    print(response.choices[0].message.content)
    add_to_txt("Message =" + str(response.choices[0].message.content))
    add_to_txt("==================")
    add_to_txt("Token usage =" + str(response.usage.total_tokens))
    add_to_txt("==================")
    add_to_txt("Sent message =" + str(messages))
    add_to_txt("Response =" + str(response))
    add_to_txt("====================================")

# authentication issue
except openai.error.AuthenticationError:
    print('no valid token / authentication error')

except openai.error.InvalidRequestError as e:
    print('invalid request, read the manual')
    print(e)



