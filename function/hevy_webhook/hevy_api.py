"""Helper module for interacting with Hevy API."""

import logging
import os
import requests
from typing import Optional, Dict, Any
from datetime import datetime


def get_workout_details(workout_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch workout details from Hevy API.
    
    Args:
        workout_id: UUID of the workout to fetch
        
    Returns:
        Dictionary containing workout details, or None if error
    """
    hevy_api_key = os.environ.get("HEVY_API_KEY")
    
    if not hevy_api_key:
        logging.error("HEVY_API_KEY not configured")
        return None
    
    headers = {
        "api-key": hevy_api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"https://api.hevyapp.com/v1/workouts/{workout_id}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code != 200:
            logging.error(f"Hevy API error: {response.status_code} - {response.text}")
            return None
        
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch workout from Hevy API: {str(e)}")
        return None


def get_routine_details(routine_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch routine details from Hevy API.
    
    Args:
        routine_id: UUID of the routine to fetch
        
    Returns:
        Dictionary containing routine details, or None if error
    """
    hevy_api_key = os.environ.get("HEVY_API_KEY")
    
    if not hevy_api_key:
        logging.error("HEVY_API_KEY not configured")
        return None
    
    headers = {
        "api-key": hevy_api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"https://api.hevyapp.com/v1/routines/{routine_id}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code != 200:
            logging.error(f"Hevy API error for routine: {response.status_code} - {response.text}")
            return None
        
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch routine from Hevy API: {str(e)}")
        return None


def calculate_workout_duration(workout_data: Dict[str, Any]) -> Optional[float]:
    """
    Calculate workout duration in minutes from workout data.
    
    Args:
        workout_data: Workout data from Hevy API
        
    Returns:
        Duration in minutes, or None if cannot be calculated
    """
    try:
        # Try to get duration_seconds if available
        if 'duration_seconds' in workout_data:
            return workout_data['duration_seconds'] / 60.0
        
        # Try to calculate from start_time and end_time
        start_time_str = workout_data.get('start_time')
        end_time_str = workout_data.get('end_time')
        
        if start_time_str and end_time_str:
            start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
            duration_seconds = (end_time - start_time).total_seconds()
            return round(duration_seconds / 60.0, 0)
        
        logging.warning("Could not calculate workout duration from available data")
        return None
    except (ValueError, TypeError, KeyError) as e:
        logging.error(f"Error calculating workout duration: {str(e)}")
        return None
