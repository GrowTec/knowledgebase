from datetime import datetime
from typing import Dict, List

from fastapi import APIRouter
from elasticsearch_dsl import Q, Search
from elasticsearch_dsl.query import MultiMatch

from models.elasticModels import KnowledgeEntry, KnowledgeEntryPydantic
from models.responseModels import AddKnowledgeEntryResponse


router = APIRouter(tags=["search"])


# search for entries
@router.get('/api/search')
async def search_knowledge(query_string: str):
    response_data: List[Dict[str, str]] = []

    query = Q('multi_match', query=query_string, fields=['title', 'description', 'resolution'])
    search = Search(index='knowledge-index').query(query)
    search_response = search.execute()
    for hit in search_response:
        if 'automation_link' in hit:
            response_data.append(
                {
                    'id': hit.meta.id,
                    'title': hit.title,
                    'description': hit.description,
                    'resolution': hit.resolution,
                    'automation_link': hit.automation_link
                }
            )
        else:
            response_data.append(
                {
                    'id': hit.meta.id,
                    'title': hit.title,
                    'description': hit.description,
                    'resolution': hit.resolution,
                    'automation_link': ""
                }
            )

    return {
        "Your query": query_string,
        "results": response_data
    }


# get a specific document by it's ID
@router.get('/api/search/{id}')
async def search_knowledge_by_id(id: str):
    response_data: Dict[str, str] = {}

    search = Search(index='knowledge-index').query('match', _id=id)
    search_response = search.execute()

    for hit in search_response:
        if 'automation_link' in hit:
            response_data = {
                'id': hit.meta.id,
                'title': hit.title,
                'description': hit.description,
                'resolution': hit.resolution,
                'automation_link': hit.automation_link
            }
        else:
            response_data = {
                'id': hit.meta.id,
                'title': hit.title,
                'description': hit.description,
                'resolution': hit.resolution,
                'automation_link': ""
            }
    return response_data


# Add new entry
@router.post('/api/search', status_code=201, response_model=AddKnowledgeEntryResponse)
async def add_knowledge_entry(new_entry: KnowledgeEntryPydantic):
    if new_entry.automation_link:  # if the 'automation_link' key exists
        new_doc = KnowledgeEntry(
            updated_at = datetime.utcnow(),
            title = new_entry.title,
            description = new_entry.description,
            resolution = new_entry.resolution,
            automation_link = new_entry.automation_link
        )
    else:
        new_doc = KnowledgeEntry(
            updated_at = datetime.utcnow(),
            title = new_entry.title,
            description = new_entry.description,
            resolution = new_entry.resolution
        )
    new_doc_create_response = new_doc.save(return_doc_meta=True)

    return AddKnowledgeEntryResponse(
        result = new_doc_create_response['result'],  # the result of the .save() method
        id = new_doc_create_response['_id']  # the document's ID within Elasticsearch
    )


# update an existing entry
@router.patch('/api/search/{id}')
async def update_knowledge_entry(id: str, document: KnowledgeEntryPydantic):
    # find the current document
    current_doc = KnowledgeEntry.get(id=id)

    # update the document
    update_response = current_doc.update(
        updated_at = datetime.utcnow(),
        title = document.title,
        description = document.description,
        resolution = document.resolution
    )
    return {'result': update_response}


