import streamlit as st
from model import lcpp_llm, newsletters, N_CTX
import datetime 
import pandas as pd
from utils import chunks

def make_template(text1):
    return f"""
              Write a concise summary of the following text delimited by triple backquotes.
              Return your response in bullet points which covers the key points of the text.
              ```{text1}```
              BULLET POINT SUMMARY:
           """
def get_response(radio_select):
    if radio_select =="All":
        text1 = newsletters.copy()
    else:
        text1 = newsletters[newsletters['from']==radio_select]

    # check if nb_tokens >= nb_ctx :
    if text1['n_tokens'].sum() < N_CTX : #nb_ctx:
        template = make_template(str(text1['text'].to_list()))
        response = lcpp_llm(prompt=template,  max_tokens=256,temperature=0,top_p=0.95,repeat_penalty=1.2,top_k=50,stop = ['USER:'], # Dynamic stopping when such token is detected.
        echo=False # return the prompt
        )
        return response["choices"][0]["text"].split("\n")
    else:
        text1 = chunks(text1,N_CTX-100)
        responses = ""
        for text_i in text1:
            template = make_template(text_i)
            response = lcpp_llm(prompt=template,  max_tokens=256,temperature=0,top_p=0.95,repeat_penalty=1.2,top_k=50,stop = ['USER:'], # Dynamic stopping when such token is detected.
            echo=False # return the prompt
            )
            responses = responses + response["choices"][0]["text"]

        return responses.split("\n")


def main():
    st.title("Newsletter summary")
    query = st.radio("What's your newsletter of interest",["AlphaSignal", "TLDR", "Towards AI Newsletter","All"],horizontal=True)

    if st.button('Get newsletters summaries'):
        if query == '':
            st.write('Searchable query missing. Please try again.')
        else:
            responses = get_response(query)
            for resp in responses: 
                st.markdown(resp.replace("•",""))


if __name__ == '__main__':
	main()