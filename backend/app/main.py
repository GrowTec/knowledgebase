from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import secure
from elasticsearch_dsl import connections

from models.elasticModels import KnowledgeEntry

from routes.search import router as searchRouter


app = FastAPI(
    title='Knowledge Search Backend',
    description='API to search an Elasticsearch database for issues and their resolutions',
    version='0.0.1'
)
secure_headers = secure.Secure()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.middleware('http')
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response


@app.on_event('startup')
async def startup_events():
    """
    Create a connection to Elasticsearch running on localhost:9200 (the default).
    Using the create_connection() method allows all other operations to use that connection automatically.
    """
    connections.create_connection(hosts=['knowledgebase-database'])
    KnowledgeEntry.init()  # initialize the Elasticsearch class before we use it.


@app.get("/", status_code=200, tags=["test"])
async def index(welcome_message: str = "Hello World!"):
    return {"message:": welcome_message}


# include the imported routers
app.include_router(searchRouter)
