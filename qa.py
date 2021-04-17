import streamlit as st
from boilerpy3 import extractors
from transformers import pipeline
import requests
import pandas as pd
from pprint import pprint
from IPython.display import display, HTML

# Initilizing the QA model
qa = pipeline("question-answering")



def if_403_error(url, extractor):
      
  headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko)'
                  'Chrome/50.0.2661.102 Safari/537.36'}

  resp = requests.get(url, headers=headers)
  if resp.ok:
      doc = extractor.get_doc(resp.text)
      return doc

  else:
      raise Exception(f'Failed to get URL: {resp.status_code}')


def get_text_from_url(url):
  response = {}
  try:   
    extractor = extractors.ArticleExtractor()
    doc = extractor.get_doc_from_url(url)
    response = {'title': doc.title, 'content':doc.content, 'success':True, 'error': None}

  except Exception as e:
    if e.code == 403:
      doc = if_403_error(url, extractor)
      response = {'title': doc.title, 'content':doc.content, 'success':True, 'error': None}
   
  return response


def get_question_answers(article_text, questions):
  result = []
  article_text = r"""{}""".format(article_text)
  answers = qa(question=questions, context=article_text)

  for idx, _ in enumerate(questions, start=0):
    result.append({'question':questions[idx], 'answer':answers[idx]['answer']})
  print("Answers Extracted Sucessfully...")
  return result

def display_qa_response(qa_object):
  display(HTML(pd.DataFrame(qa_object).to_html()))




tech_blog = 'https://aws.amazon.com/blogs/machine-learning/announcing-aws-media-intelligence-solutions/'
news_article = 'https://arynews.tv/en/lahore-coronavirus-positivity-rate/'
story = 'https://americanliterature.com/childrens-stories/little-red-riding-hood'

questions = ['What did Little Red Riding Hood give to her grandmother?', 
             'How far away from the village did the grandmother live?', 
             'Where did the wolf meet the little red riding hood?']

response = get_text_from_url(story)

if response['success']:
  article = response['content']
  qa_result = get_question_answers(article, questions)
  display_qa_response(qa_result)


pprint(qa_result, width=200)  
