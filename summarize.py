from pdf_txt import pdf_to_text, get_num_pages, pdf_to_text_miner
import os
import openai
from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig
import json
import requests
import traceback

input_file='sample.pdf'

def openai_summarize(input_file):
    openai.api_key= "API_KEY"

    num_count = get_num_pages(input_file)
    f = open('summarized.txt','a+')

    count=0
    while count<num_count:

        text= pdf_to_text(input_file,count)
        response = openai.Completion.create(
            engine="davinci", 
            prompt= text, 
            temperature=0.3,
            max_tokens=50,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
            )

        summarized_text = response['choices'][0]['text'] 
        print(summarized_text)
        f.write(summarized_text)
        
    f.close()

def bart_summarize(input_file):
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    
    num_count = get_num_pages(input_file)
    f = open('summarized_bart.txt','a+')

    count=0
    while count<num_count:
        text= pdf_to_text(input_file,count)
        ARTICLE_TO_SUMMARIZE = text
        inputs = tokenizer([ARTICLE_TO_SUMMARIZE], max_length=1024, return_tensors='pt')
        # Generate Summary
        summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=5, early_stopping=True)
        summarized_text = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]
        print(summarized_text)
        str1=''.join(summarized_text)
        print(str1)
        f.write(str1)
        count += 1
        
    f.close()

def bart_large(input_file):

    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

    def query(payload):
        data = json.dumps(payload)
        response = requests.request("POST", API_URL, data=data)
        return json.loads(response.content.decode("utf-8"))
    
    def splitter(n, s):
        pieces = s.split()
        out = (" ".join(pieces[i:i+n]) for i in range(0, len(pieces), n))
        return out
 
    f = open('summarized_bart_api.txt','a+')

    i = 0
    for paragraph in splitter(1000, text):
       
        i+= 1
        
        try:
            print('\n\n')
            print('on paragraph', i)
            print('paragraph length is:',len(paragraph))
            data=query(paragraph)
            
            output = data[0]['summary_text']
            
            print('summary length for paragraph is:', len(output))
            f.write(output)
            f.write('\n\n')
        except Exception as e:
            error = traceback.format_exc()
            print(error)
            print(data)
        
    f.close()


#Choose one of 3 methods, comment out the other two
if __name__=='__main__':
    #openai_summarize(input_file)
    #bart_summarize(input_file)
    bart_large(input_file)

