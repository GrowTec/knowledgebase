from typing import Optional

from elasticsearch_dsl import Document, Date
from pydantic import BaseModel


class KnowledgeEntry(Document):
    updated_at = Date(default_timezone='UTC')
    title: str  # title of the issue or error being seen
    description: str  # description of the issue and any helpful error messages
    resolution: str  # steps or commands to fix this issue
    automation_link: str or None  # link to any automation to fix the issue without manual steps


    class Index:  # name of the Elastic index to add these documents to
        name = 'knowledge-index'


class KnowledgeEntryPydantic(BaseModel):
    id: Optional[str] or None
    title: str
    description: str
    resolution: str
    automation_link: Optional[str] = None


    class Config:
        schema_extra = {
            "example": {
                "title": "My new entry's title",
                "description": "This should be a detailed description of the known issue. It should also include an error messages. This is mainly what Elasticsearch will search for any matches to a search query.",
                "resolution": "The step(s) to resolve this known issue.",
                "automation_link": "[OPTIONAL]. This would be a link to any scripts or automated tools that can resolve this issue for you without manual intervention."
            }
        }
