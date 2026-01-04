"""
Recipe tools for the cooking AI agent.
Provides functions for recipe search and ingredient extraction.
"""

from typing import Annotated
import json


def search_recipes(
    query: Annotated[str, "The search query (ingredients, cuisine, or recipe name)"],
    cuisine_type: Annotated[str, "The cuisine type (e.g., Italian, Asian, Mexican)", ""] = "",
) -> str:
    """
    Search for recipes based on query and optional cuisine type.
    
    Args:
        query: Search terms (ingredients or recipe name)
        cuisine_type: Optional cuisine type filter
        
    Returns:
        A JSON string containing recipe suggestions
    """
    # Sample recipe database
    recipes_db = {
        "pasta": [
            {
                "name": "Classic Carbonara",
                "cuisine": "Italian",
                "ingredients": ["pasta", "eggs", "bacon", "parmesan cheese", "black pepper"],
                "servings": 4,
                "prep_time": "15 minutes",
                "cook_time": "20 minutes"
            },
            {
                "name": "Pasta Aglio e Olio",
                "cuisine": "Italian",
                "ingredients": ["pasta", "garlic", "olive oil", "red pepper flakes", "parsley"],
                "servings": 2,
                "prep_time": "10 minutes",
                "cook_time": "15 minutes"
            }
        ],
        "chicken": [
            {
                "name": "Garlic Butter Chicken",
                "cuisine": "American",
                "ingredients": ["chicken breast", "garlic", "butter", "lemon", "thyme"],
                "servings": 4,
                "prep_time": "10 minutes",
                "cook_time": "25 minutes"
            },
            {
                "name": "Thai Red Curry Chicken",
                "cuisine": "Asian",
                "ingredients": ["chicken", "red curry paste", "coconut milk", "bell pepper", "basil"],
                "servings": 4,
                "prep_time": "15 minutes",
                "cook_time": "20 minutes"
            }
        ],
        "beef": [
            {
                "name": "Beef Stew",
                "cuisine": "European",
                "ingredients": ["beef", "potatoes", "carrots", "onion", "beef broth", "thyme"],
                "servings": 6,
                "prep_time": "20 minutes",
                "cook_time": "120 minutes"
            }
        ],
        "chocolate": [
            {
                "name": "Chocolate Cake",
                "cuisine": "American",
                "ingredients": ["flour", "chocolate", "eggs", "butter", "sugar", "cocoa powder"],
                "servings": 8,
                "prep_time": "15 minutes",
                "cook_time": "35 minutes"
            }
        ]
    }
    
    results = []
    query_lower = query.lower()
    
    # Search through recipes
    for key, recipes_list in recipes_db.items():
        if key in query_lower:
            for recipe in recipes_list:
                if cuisine_type and recipe["cuisine"].lower() != cuisine_type.lower():
                    continue
                results.append(recipe)
    
    # Also search by ingredients
    if not results:
        for key, recipes_list in recipes_db.items():
            for recipe in recipes_list:
                if any(ingredient in query_lower for ingredient in recipe["ingredients"]):
                    if cuisine_type and recipe["cuisine"].lower() != cuisine_type.lower():
                        continue
                    results.append(recipe)
    
    if results:
        return json.dumps({
            "status": "success",
            "count": len(results),
            "recipes": results
        }, indent=2)
    else:
        return json.dumps({
            "status": "no_results",
            "message": f"No recipes found for '{query}'" + (f" in {cuisine_type} cuisine" if cuisine_type else "")
        })


def extract_ingredients(
    recipe_description: Annotated[str, "The recipe description or ingredient list to extract from"],
) -> str:
    """
    Extract and format ingredients from a recipe description.
    
    Args:
        recipe_description: The recipe text to extract ingredients from
        
    Returns:
        A JSON string containing extracted ingredients
    """
    # Common ingredient patterns
    common_ingredients = [
        "flour", "sugar", "salt", "pepper", "butter", "oil", "egg", "eggs",
        "milk", "cream", "cheese", "garlic", "onion", "tomato", "potato",
        "carrot", "chicken", "beef", "fish", "pasta", "rice", "bread",
        "lemon", "lime", "orange", "apple", "banana", "berry", "berries",
        "chocolate", "vanilla", "cinnamon", "basil", "parsley", "thyme",
        "olive", "coconut", "soy", "vinegar", "sauce", "broth", "stock"
    ]
    
    description_lower = recipe_description.lower()
    found_ingredients = []
    
    for ingredient in common_ingredients:
        if ingredient in description_lower:
            found_ingredients.append(ingredient.title())
    
    if found_ingredients:
        return json.dumps({
            "status": "success",
            "extracted_ingredients": list(set(found_ingredients)),  # Remove duplicates
            "count": len(set(found_ingredients))
        }, indent=2)
    else:
        return json.dumps({
            "status": "no_ingredients_found",
            "message": "Could not extract clear ingredients from the provided description"
        })


def get_recipes_by_ingredients(
    available_ingredients: Annotated[str, "Comma-separated list of available ingredients"],
) -> str:
    """
    Find recipes that can be made with the available ingredients.
    
    Args:
        available_ingredients: Comma-separated list of ingredients
        
    Returns:
        A JSON string containing recipes that match the ingredients
    """
    ingredients_list = [ing.strip().lower() for ing in available_ingredients.split(",")]
    
    recipes_db = {
        "pasta": [
            {
                "name": "Simple Pasta with Oil and Garlic",
                "required_ingredients": ["pasta", "garlic", "oil"],
                "servings": 2,
                "cook_time": "15 minutes"
            }
        ],
        "chicken": [
            {
                "name": "Pan-seared Chicken",
                "required_ingredients": ["chicken", "salt", "pepper"],
                "servings": 4,
                "cook_time": "25 minutes"
            }
        ]
    }
    
    matching_recipes = []
    
    for category, recipes_list in recipes_db.items():
        for recipe in recipes_list:
            required = [req.lower() for req in recipe["required_ingredients"]]
            if all(any(req in ingredient for ingredient in ingredients_list) for req in required):
                matching_recipes.append(recipe)
    
    if matching_recipes:
        return json.dumps({
            "status": "success",
            "matching_recipes": matching_recipes,
            "count": len(matching_recipes)
        }, indent=2)
    else:
        return json.dumps({
            "status": "no_matches",
            "message": f"No recipes found that match your ingredients: {available_ingredients}"
        })
