"""Notion database integration for Hevy workout entries."""

import logging
import os
import requests
from typing import Dict, Any, Optional


def add_workout_to_notion(workout_data: Dict[str, Any], routine_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Add a Hevy workout entry to the Notion Workouts database.
    
    Args:
        workout_data: Workout data from Hevy API
        routine_name: Name of the routine (e.g., "Upper Body 💪")
        
    Returns:
        Response from Notion API
        
    Raises:
        ValueError: If required environment variables are not set
        requests.HTTPError: If Notion API request fails
    """
    notion_api_key = os.environ.get("NOTION_API_KEY")
    notion_workouts_db_id = os.environ.get("NOTION_WORKOUTS_DATABASE_ID")
    
    if not notion_api_key or not notion_workouts_db_id:
        raise ValueError("NOTION_API_KEY and NOTION_WORKOUTS_DATABASE_ID environment variables must be set")
    
    # Prepare Notion API headers
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Extract workout ID
    workout_id = workout_data.get("id", "")
    
    # Extract and format workout date
    workout_date = None
    start_time = workout_data.get("start_time")
    if start_time:
        # Hevy uses ISO 8601 format
        workout_date = start_time.split('T')[0]  # Extract just the date part
    
    # Calculate duration in minutes
    duration_minutes = None
    if "duration_seconds" in workout_data:
        duration_minutes = workout_data["duration_seconds"] / 60.0
    
    # Build properties according to Notion database schema
    properties = {
        "Hevy ID": {
            "title": [
                {
                    "text": {
                        "content": workout_id
                    }
                }
            ]
        }
    }
    
    # Add workout date if available
    if workout_date:
        properties["Workout Date"] = {
            "date": {
                "start": workout_date
            }
        }
    
    # Add duration if available
    if duration_minutes is not None:
        properties["Duration"] = {
            "number": round(duration_minutes, 2)
        }
    
    # Add routine as select option if provided
    if routine_name:
        properties["Routine"] = {
            "select": {
                "name": routine_name
            }
        }
    
    # Prepare the request payload
    payload = {
        "parent": {
            "database_id": notion_workouts_db_id
        },
        "properties": properties
    }
    
    # Make the API request to create a page in the database
    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers=headers,
        json=payload,
        timeout=10
    )
    
    if response.status_code != 200:
        logging.error(f"Notion API error: {response.status_code} - {response.text}")
        response.raise_for_status()
    
    return response.json()


def ensure_routine_option_exists(routine_name: str) -> bool:
    """
    Check if a routine name exists as a select option in the Notion database.
    If not, the option will be automatically created by Notion when adding the workout.
    
    Args:
        routine_name: Name of the routine to check
        
    Returns:
        True (option will be created automatically if it doesn't exist)
        
    Note:
        Notion automatically creates new select options when you reference them
        in a page creation request, so this function is mainly for logging purposes.
    """
    if routine_name:
        logging.info(f"Routine '{routine_name}' will be added as select option if it doesn't exist")
    return True
