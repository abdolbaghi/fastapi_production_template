
from src.database import MeiliSearch ,MeiliSearchParameters
from typing import List
from src.foodlist.schemas import Food
# Initialize MeiliSearch client
index = MeiliSearch('food_index')

def create_food(food:Food):
    index.add_document(food.serializable_dict())
    
def search_by_ingredient_in_meilisearch(ingredient: str) -> List[List[str]]:
    """
    Search for foods with a specific ingredient in MeiliSearch and retrieve only the ingredient names.

    Args:
        ingredient (str): Ingredient to search for.

    Returns:
        List[List[str]]: List of ingredient lists that match the given ingredient.
    """
    search_result = index.adnvance_search(MeiliSearchParameters(filter=f'ingredients = "{ingredient}"',attributes_to_retrieve=['ingredients']))
    matching_set = set()
    for hit in search_result['hits']:
        for ingredient in hit['ingredients']:
            matching_set.add(ingredient)
    return matching_set
def search_by_tag_in_meilisearch(tag: str) -> List[str]:
    """
    Search for foods with a specific tag in MeiliSearch and retrieve only the tag names.

    Args:
        tag (str): Tag to search for.

    Returns:
        List[str]: List of tags that match the given tag.
    """
    search_result = index.adnvance_search(MeiliSearchParameters(filter=f'tags = "{tag}"',attributes_to_retrieve=['tags']))
    matching_set = set()
    for hit in search_result['hits']:
        for tag in hit['tags']:
            matching_set.add(tag)
    return matching_set