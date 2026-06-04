from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory = "Static"), name = "static") #this is how we serve static files in FastAPI, we mount the StaticFiles class to a specific path and specify the directory where our static files are located

templates = Jinja2Templates(directory = "templates")

posts: list[dict] = [
    {
        "id": 1,
        "author": "Pratik Kumar Jha",
        "title": "Learning FastAPI is fun",
        "content": "FastAPI is a great choice for machine learning enginners.",
        "date_posted": "April 19, 2025",
    },
    {
        "id": 2,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 3,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]

# @app.get("/" , response_class = HTMLResponse ,include_in_schema = False)    #this is stacking decorators in FastAPI, it allows us to have multiple routes for the same function
# @app.get("/posts" , response_class = HTMLResponse, include_in_schema = False)    #this is stacking decorators in FastAPI, it allows us to have multiple routes for the same function 
@app.get("/", include_in_schema = False, name = "home")    
@app.get("/posts", include_in_schema = False, name = "posts")
def home(request: Request):
    return templates.TemplateResponse(
        request, "home.html", {"posts" : posts, "title" : "Home"},
        ) #this is how we render a template in FastAPI, we pass the request object, the name of the template and a dictionary of variables to the TemplateResponse function

@app.get("/api/posts")
def get_posts():
    return posts