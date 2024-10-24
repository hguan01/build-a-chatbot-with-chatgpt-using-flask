from flask import Blueprint, render_template
from flask import request
from .models import Result
from openai import OpenAI

routes = Blueprint('routes', __name__)

client = OpenAI(
    api_key='YOUR_API_KEY',
)

@routes.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        query = request.args.get('query')

        if query == "" or query is None:
            return render_template('response_view.html')

        response = ask(query)

        dataList = []
        queryMessage = Result(time="This Time", messagetype="other-message float-right", message=query)
        responseMessage = Result(time="This Time", messagetype="my-message", message=response)
        dataList.append(queryMessage)
        dataList.append(responseMessage)

        return render_template('response_view.html', results=dataList)


def ask(question, chat_log=None):
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": question,
            }
                ],
            model="gpt-3.5-turbo",
        )

    response = completion.choices[0].message.content
    return response