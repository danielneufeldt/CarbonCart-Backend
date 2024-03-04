import openai
import os
import json
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
import requests
from bs4 import BeautifulSoup

openai.api_key = "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"

app = FastAPI()

@app.get("/scrape")
async def scrape(url: str):
    try:
        # Send HTTP request to the URL
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Use BeautifulSoup to parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract the text from the webpage
            # Note: You can modify this to return structured data as needed
            page_text = soup.get_text()


            emissions_response = calculate_emissions(page_text)
            return JSONResponse(content={"content": page_text})
        else:
            return HTTPException(status_code=404, detail="Web page not found")
    except Exception as e:
        # Handle unexpected errors
        return HTTPException(status_code=500, detail=str(e))


def calculate_emissions(page_text):

  asked = "What is the carbon emissions (shipping and manufacturing combined) of the following product in json format produce given the delivering location:"
  delivered = "Los Angeles, CA"
  text = str(page_text)
  # json_string = json.dumps(json_file, indent = 4)
  condition = "I want the answer to be an estimate of the Carbon emissions where we have a singlular number, not a range or anything like that If you MUST give a range, then just give me the middle point of the two bounds."
  answer = 'Give final output in the form of "Total Emissions for this product is: X kg" X represents the amount of carbon emissions in Kilograms. Do not have the answer in this format: Total Emissions for this product is: x (The specific carbon emissions for shipping and manufacturing would need to be provided by the manufacturer or supplier)'
  content = str(asked + " " + delivered + " " + text + " " + condition + " " + answer)

  completion = openai.ChatCompletion.create(
      model = 'gpt-3.5-turbo',
      messages = [
          {"role":"user", "content":content}
      ]
  )

  print(completion.choices[0].message.content)
  return completion.choices[0].message.content
  # print(content)
  # create an API

  # let computers get my data from this API