from pydantic import BaseModel


class AddKnowledgeEntryResponse(BaseModel):
    # Response model for the add_knowledge_entry function
    result: str
    id: str
