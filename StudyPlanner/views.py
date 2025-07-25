from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
import json
import csv
import os
import google.generativeai as genai
import logging
import json
from datetime import datetime, timedelta
from collections import defaultdict


logger = logging.getLogger(__name__)


def initialize_gemini():
    try:
        # Use Django setting for API key (which gets it from environment variable)
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("Gemini API key not found in environment variables")

        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        logger.error(f"Failed to initialize Gemini: {e}")
        raise

def index(request):
    return render(request, "index.html")


def generate_study_plan(request):
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            tasks = data.get('tasks', [])

            if not tasks:
                return JsonResponse({'error': 'No tasks provided'}, status=400)

            # Build prompt
            prompt = "Create a study plan/calendar based on these tasks:\n\n"
            for task in tasks:
                status = task.get('status', 'pending')
                prompt += f"- Task: {task['name']}, Date: {task['date']}, Type: {task['type']}, Status: {status}\n"

            prompt += """\nPlease organize these tasks into a well-structured study plan with time allocations and breaks. Give the output in a JSON format with the following structure:{
  "study_plan": {
    "title": "...",
    "tasks": [
      {
        "date": "YYYY-MM-DD",
        "time_start": "HH:MM",
        "time_end": "HH:MM",
        "activity": "...",
        "type": "...",
        "notes": "..."
      }
    ]
  }
}
"""

            # Initialize and call Gemini
            try:
                model = initialize_gemini()
                response = model.generate_content(prompt)

                if not response or not response.text:
                    return JsonResponse({'error': 'Empty response from Gemini API'}, status=500)

            except Exception as gemini_error:
                logger.error(f"Gemini API error: {gemini_error}")
                return JsonResponse({'error': 'Failed to connect to AI service'}, status=500)

            # Parse JSON response
            try:
                # Clean the response text - remove markdown formatting if present
                response_text = response.text.strip()
                if response_text.startswith('```json'):
                    response_text = response_text[7:]  # Remove ```json
                if response_text.endswith('```'):
                    response_text = response_text[:-3]  # Remove ```

                study_plan = json.loads(response_text)
            except json.JSONDecodeError as json_error:
                logger.error(f"JSON decode error: {json_error}, Raw response: {response.text}")
                # Return a fallback response structure
                fallback_plan = {
                    "study_plan": {
                        "title": "Generated Study Plan",
                        "tasks": [{"name": task['name'], "date": task['date'], "type": task['type']} for task in tasks]
                    }
                }
                return JsonResponse(
                    {'study_plan': fallback_plan, 'warning': 'AI response was malformed, showing fallback plan'})

            study_plan = json.loads(response_text)
            request.session['latest_study_plan'] = study_plan
            return JsonResponse({'study_plan': study_plan})


        except json.JSONDecodeError as json_error:
            logger.error(f"Request JSON decode error: {json_error}")
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)

        except Exception as e:
            logger.error(f"Unexpected error in generate_study_plan: {e}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


def study_plan_calendar(request):
    study_plan_data = request.session.get('latest_study_plan')

    if not study_plan_data:
        messages.error(request, "No study plan available. Please generate one first.")
        return redirect('index')

    tasks_by_date = defaultdict(list)
    for task in study_plan_data['study_plan'].get('tasks', []):
        tasks_by_date[task['date']].append(task)

    context = {
        'study_plan': study_plan_data['study_plan'],
        'tasks_by_date': dict(tasks_by_date),
    }

    return render(request, 'calendar.html', context)

