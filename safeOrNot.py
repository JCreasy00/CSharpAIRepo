# here I grab a bunch of url's to stack exchange articles and their titles and send them through the /predict endpoint of fastAPI which=
# predicts whether or not the article and or other parts of it are safe for work. My goal here was to understand how to send a post request
# to an API through python as well as understand how to parse the json information that is sent back.

# TO DO:
#     output NSFW words, if there are any, as a list that is easy to read instaed of json

# import libraries
import requests
import json

# grabbing a bunch of articles and their titles
url = 'https://api.stackexchange.com/2.3/articles?order=desc&sort=activity&site=stackoverflow'
response = requests.get(url)

# create a list of lists, inner lists has title and url, the 2 params for /predict
url_and_title = []

#  parse response and append the url and title of each article to url_and_title
for data in response.json()['items']:
    temp = [data['link'], data['title']] 
    url_and_title.append(temp)

# create a function that takes in a url and text, and passes it to /predict
# then either include or make in another function the pulling of data from /predicts response
def postPredict(urlIN: str, text: str):
    # API endpoint 
    url = 'http://tfs.mcnsolutions.net:8040/predict'

    #create payload
    payload = {
        "url": urlIN,
        "text": text
    }

    # convert payload from python dictionary to json
    jsonload = json.dumps(payload, indent = 4)

    # send post request
    response = requests.post(url, data = jsonload)

    # get the response data
    response_data = response.json() 

    # Display input
    print("Input URL: " + urlIN)
    print("Input Text: " + text + "\n")

    # print out the data that we want to see
    # dont inclue the list of NSFW words, yet, or the description
    for i in response_data:
      if i != "NSFW words" and i != "Description":
        print (i + ": " + str(response_data[str(i)]))

    # load the words that are declared NSFW as json
    # from here on in the function is not working
    NSFWjson = response_data.get("NSFW words")

    if NSFWjson:  
      # parse the json string
      NSFWlist = json.loads(NSFWjson)
      
      # extract the words from the list of word objects
      words = [word_obj['Word'] for word_obj in NSFWlist]
      
      print (words)

# url only instance
def postPredict(urlIN: str):
   
  url = 'http://tfs.mcnsolutions.net:8040/predict'

  payload = {
     "url" : urlIN
  }

  jsonload = json.dumps(payload, indent = 4)
  response = requests.post(url, data = jsonload)
  response_data = response.json()
  print("Input URL: " + urlIN + "\n")
  dontInclude = ['NSFW words', 'Description', 'predicted_label_text', 'confidence_score_text']

  for i in response_data:
     if i not in dontInclude:
        print (i + ': ' + str(response_data[str(i)]))

# text only instance
def postPredict(text: str):
   
  url = 'http://tfs.mcnsolutions.net:8040/predict'

  payload = {
     "text" : text
  }

  jsonload = json.dumps(payload, indent = 4)
  response = requests.post(url, data = jsonload)
  response_data = response.json()
  print("Input Text: " + text + "\n")
  include = ['predicted_label_text', 'confidence_score_text']

  for i in response_data:
     if i in include:
        print (i + ': ' + str(response_data[str(i)]))

for i in url_and_title:
   postPredict(str(i[0]), str(i[1]))
   print("\n---------------------------------------------------------------------------------------\n")
    

