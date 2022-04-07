import uvicorn

def start(event=None):
    uvicorn.run("utils.dash_app:server", host="0.0.0.0", port=8000, reload=True)
    

if __name__ == "__main__":
    uvicorn.run("dash_app:server", host="0.0.0.0", port=8000, reload=True)