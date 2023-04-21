
#Question 36. openai 12번 문제에서 만든 chatgpt api를 연동하여
# textarea1에 prompt를 넣고 button을 
#누르면 response가 textarea2에 출력되도록 하시오. (3점)
from tqdm.auto import tqdm 
from dotenv import load_dotenv
import backoff 
import openai
import tiktoken
import os


from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State

encoding = tiktoken.get_encoding("cl100k_base")
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def estimate_token(text):
  return len(encoding.encode(text))

MODEL = "gpt-3.5-turbo"
P_PENALTY = -2.0
TEMPERATURE = 0
PROMPT_MAXLEN = 2000

load_dotenv() 
import glob  
import os 

openai.api_key = os.getenv("OPENAI_API_KEY") #.env파일에서 api key 가져오기


def completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)



def run_api(q):
    answer = ""
    token_count = estimate_token(q)
    try:
        completion = completions_with_backoff(model=MODEL, messages=[{'role':'user', 'content': q}], presence_penalty=P_PENALTY, temperature=TEMPERATURE)

        result = completion.choices[0]
        answer = {"prompt": q,"gpt_answer": result['message']['content'],}
            
    except openai.error.RateLimitError as e:
        print(f"OpenAI API returned an API Error: {e}")
    pass

    return answer

app = Dash(__name__)

app.layout = html.Div([
    dcc.Textarea(id='textbox1',value='',style={'width': '100%', 'height': 200},), #input id = textbox1
    html.Div(id='textbox2', style={'whiteSpace': 'pre-line'}), #ouput id= textbox2
    html.Button('버튼', id='buttonbox', n_clicks=0) #button id = buttonbox
], id='wrapper')

@app.callback(
    Output('textbox2', 'children'),
    Input('buttonbox', 'n_clicks'),
    State('textbox1', 'value')
)
def update_output(n_clicks, value):
    try:
        answer = {}
        if n_clicks > 0:
            answer = run_api(value)
        return answer['gpt_answer']
    except:
        pass
        
    

if __name__ == '__main__':
    app.run_server(debug=True)
