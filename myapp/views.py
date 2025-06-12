from django.shortcuts import HttpResponse, redirect
from django.http import HttpRequest
import random
from django.views.decorators.csrf import csrf_exempt
next_Id = 4
topics = [
    {'id':1,'title':'routing','body':'Routing is ...'},
    {'id':2,'title':'view','body':'View is ...'},
    {'id':3,'title':'Model','body':'Model is ...'}
]

def HTMLTemplate(article:str,id=None):
    global topics
    contextUI = ''
    if id !=None:
        contextUI = f'''
            <form action="/delete/" method="post">
                <input type="hidden" name="id" value={id}></input>
                <input type="submit" value="delete"></input>
            </form>
        
        '''
    ol = ''
    for topic in topics:
        ol+= f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'    
    return f'''
<html>
    <body>
        <h1>Django</h1>
            <ol>
               {ol}
            </ol>
            {article}
        <ul>
            <a href="/create/">create</a>
        {contextUI}
        </ul>    
        
    </body>
</html>
'''

def index(request):
    article ='''
    <h2>welcome</h2>
    hello django
    '''
    return HttpResponse(HTMLTemplate(article))

@csrf_exempt
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        body = request.POST["body"]
        global next_Id
        newTopic = {"id":next_Id,"title":title,"body":body}
        topics.append(newTopic)
        url = '/read/'+str(next_Id)
        next_Id +=1
        return redirect(url)
    return HttpResponse(HTMLTemplate('''
    <form action="/create/" method="post">
        <p><input type="text" name="title" placeholder="title"></p>
        <p><textarea type="textarea" name="body" placeholder="body"></textarea></p>
        <p><input type="submit"></p>  
    </form>
    '''))
    
def read(request ,id):
    global topics
    article =''
    for topic in topics:
        if topic['id'] == int(id):
            article = f'''<h2>{topic["title"]}</h2>
            <h3>{topic["body"]}</h3>'''
        
    return HttpResponse(HTMLTemplate(article,id))

@csrf_exempt
def delete(request:HttpRequest):
    global topics
    if request.method == 'POST':
        newTopics = []
        id = request.POST["id"]
        for topic in topics:
            if topic["id"] != int(id):
                newTopics.append(topic)
        topics = newTopics
        return redirect("/")