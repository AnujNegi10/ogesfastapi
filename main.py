from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    # return 'hello'
    return {"data":{
        "name": "anuj"
    }}

@app.get('/about')
def about():
    return "This is the about Page "