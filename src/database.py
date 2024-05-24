from typing import Any
import requests
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    Column,
    CursorResult,
    DateTime,
    ForeignKey,
    Identity,
    Insert,
    Integer,
    LargeBinary,
    MetaData,
    Select,
    String,
    Table,
    Update,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings
from src.constants import DB_NAMING_CONVENTION

DATABASE_URL = str(settings.DATABASE_URL)

engine = create_async_engine(DATABASE_URL)
metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)



async def fetch_one(select_query: Select | Insert | Update) -> dict[str, Any] | None:
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(select_query)
        return cursor.first()._asdict() if cursor.rowcount > 0 else None


async def fetch_all(select_query: Select | Insert | Update) -> list[dict[str, Any]]:
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(select_query)
        return [r._asdict() for r in cursor.all()]


async def execute(select_query: Insert | Update) -> None:
    async with engine.begin() as conn:
        await conn.execute(select_query)


class MeiliSearchParameters:
    def __init__(self,
                 q: str = "",
                 offset: int = 0,
                 limit: int = 20,
                 hits_per_page: int = 1,
                 page: int = 1,
                 filter: Optional[str] = None,
                 facets: Optional[List[str]] = None,
                 attributes_to_retrieve: List[str] = ["*"],
                 attributes_to_crop: Optional[List[str]] = None,
                 crop_length: int = 10,
                 crop_marker: str = "…",
                 attributes_to_highlight: Optional[List[str]] = None,
                 highlight_pre_tag: str = "<em>",
                 highlight_post_tag: str = "</em>",
                 show_matches_position: bool = False,
                 sort: Optional[List[str]] = None,
                 matching_strategy: str = "last",
                 show_ranking_score: bool = False,
                 attributes_to_search_on: List[str] = ["*"]):
        self.q = q
        self.offset = offset
        self.limit = limit
        self.hits_per_page = hits_per_page
        self.page = page
        self.filter = filter
        self.facets = facets
        self.attributes_to_retrieve = attributes_to_retrieve
        self.attributes_to_crop = attributes_to_crop
        self.crop_length = crop_length
        self.crop_marker = crop_marker
        self.attributes_to_highlight = attributes_to_highlight
        self.highlight_pre_tag = highlight_pre_tag
        self.highlight_post_tag = highlight_post_tag
        self.show_matches_position = show_matches_position
        self.sort = sort
        self.matching_strategy = matching_strategy
        self.show_ranking_score = show_ranking_score
        self.attributes_to_search_on = attributes_to_search_on

    def to_dict(self):
        return {
            "q": self.q,
            "offset": self.offset,
            "limit": self.limit,
            "hitsPerPage": self.hits_per_page,
            "page": self.page,
            "filter": self.filter,
            "facets": self.facets,
            "attributesToRetrieve": self.attributes_to_retrieve,
            "attributesToCrop": self.attributes_to_crop,
            "cropLength": self.crop_length,
            "cropMarker": self.crop_marker,
            "attributesToHighlight": self.attributes_to_highlight,
            "highlightPreTag": self.highlight_pre_tag,
            "highlightPostTag": self.highlight_post_tag,
            "showMatchesPosition": self.show_matches_position,
            "sort": self.sort,
            "matchingStrategy": self.matching_strategy,
            "showRankingScore": self.show_ranking_score,
            "attributesToSearchOn": self.attributes_to_search_on
        }

class MeiliSearch:
    def __init__(self, index_name, url=settings.MEILIDB_URL, api_key=settings.MEILIDB_KEY):
        self.url = url
        self.api_key = api_key
        self.index_name = index_name
        self.headers = {'Content-Type': 'application/json'}
        if api_key:
            self.headers['X-Meili-Api-Key'] = api_key
    @staticmethod
    def create_index(index_name):
        url=settings.MEILIDB_URL
        headers = {'Content-Type': 'application/json','X-Meili-Api-Key':settings.MEILIDB_KEY}
        endpoint = f"{url}/indexes"
        data = {'name': index_name}
        response = requests.post(endpoint, json=data, headers=headers)
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create index: {response.text}")

    def add_document(self, document):
        endpoint = f"{self.url}/indexes/{self.index_name}/documents"
        response = requests.post(endpoint, json=document, headers=self.headers)
        if response.status_code == 202:
            return response.json()
        else:
            raise Exception(f"Failed to add document: {response.text}")

    def delete_document(self, document_id):
        endpoint = f"{self.url}/indexes/{self.index_name}/documents/{document_id}"
        response = requests.delete(endpoint, headers=self.headers)
        if response.status_code == 204:
            return "Document deleted successfully."
        elif response.status_code == 404:
            return "Document not found."
        else:
            raise Exception(f"Failed to delete document: {response.text}")

    def search(self, query):
        endpoint = f"{self.url}/indexes/{self.index_name}/search"
        params = {'q': query}
        response = requests.get(endpoint, params=params, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to search: {response.text}")
    def adnvance_search(self, search_object:MeiliSearchParameters):
        endpoint = f"{self.url}/indexes/{self.index_name}/search"
        response = requests.get(endpoint, params=search_object.to_dict(), headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to search: {response.text}")