from django.shortcuts import HttpResponse, redirect
from django.http import HttpRequest
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
        <li>
            <form action="/delete/" method="post">
                <input type="hidden" name="id" value={id}></input>
                <input type="submit" value="delete"></input>
            </form>
        </li>
        <li><a href="/update/{id}">update</a></li>
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

@csrf_exempt
def update(request:HttpRequest,id):
    global topics
    if request.method == "GET":
        for topic in topics:
            if topic["id"] == int(id):
                selectedTopic = {"title":topic["title"],"body":topic["body"]}
        article = f'''
         <form action="/update/{id}/" method="post">
            <p><input type="text" name="title" placeholder="title" value={selectedTopic["title"]}></p>
            <p><textarea type="textarea" name="body" placeholder="body">{selectedTopic["body"]}</textarea></p>
            <p><input type="submit"></p>  
        </form>
        '''
        return HttpResponse(HTMLTemplate(article,id))
    elif request.method == "POST":
        title = request.POST["title"]
        body = request.POST["body"]
        for topic in topics:
            if topic["id"] ==int(id):
                topic["title"] = title
                topic["body"] = body
        return redirect(f'/read/{id}')
    