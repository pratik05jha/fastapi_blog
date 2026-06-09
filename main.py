from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
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


#Since we have added post.html template, we can now create API endpoints to serve the data for our posts. We will create two endpoints, one to get all the posts and another to get a specific post by its ID.
@app.get("/posts/{post_id}", include_in_schema = False)
def post_page(request: Request, post_id: int):
     for post in posts:
          if post.get("id") == post_id:
               return templates.TemplateResponse(
                    request, "post.html", {"post" : post, "title" : post["title"]},
               )
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.get("/api/posts")
def get_posts():
    return posts

@app.get("/api/posts/{post_id}")
def get_post(post_id: int):  #this is a path parameter, it allows us to capture a value from the URL and pass it to the function as an argument
    for post in posts:
        if post["id"] == post_id:
                return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")



@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )