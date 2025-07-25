from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
import json
import csv
import pandas as pd
import os
from datetime import datetime

def index(request):
    return render(request, "index.html")

def list(request):
    # You might want to pass tasks data to the template
    # For now we'll just render the template
    return render(request, "list.html")

def settings(request):
    return render(request, "settings.html")

def import_tasks(request):
    if request.method == 'POST':
        try:
            # Get data from the request
            import_data = request.POST.get('importData', '')
            import_format = request.POST.get('importFormat', 'json')
            include_properties = request.POST.get('includeProperties') == 'on'
            include_dates = request.POST.get('includeDates') == 'on'
            overwrite_existing = request.POST.get('overwriteExisting') == 'on'

            if not import_data.strip():
                return JsonResponse({'status': 'error', 'message': 'No data provided'})

            # Process the input data based on format
            tasks = []

            if import_format == 'json':
                # Process JSON data
                try:
                    json_data = json.loads(import_data)
                    if isinstance(json_data, list):
                        tasks = json_data
                    else:
                        # Handle case where JSON might be an object with a tasks key
                        tasks = json_data.get('tasks', [json_data])
                except json.JSONDecodeError:
                    return JsonResponse({
                        'status': 'error', 
                        'message': 'Invalid JSON format. Please check your input.'
                    })

            elif import_format == 'csv':
                # Process CSV data
                try:
                    lines = import_data.strip().split('\n')
                    reader = csv.DictReader(lines)
                    for row in reader:
                        tasks.append(row)
                except Exception as e:
                    return JsonResponse({
                        'status': 'error', 
                        'message': f'Error parsing CSV: {str(e)}'
                    })

            elif import_format == 'text':
                # Process simple text - one task per line
                lines = import_data.strip().split('\n')
                for i, line in enumerate(lines):
                    if line.strip():
                        # Create a simple task object from text line
                        task = {
                            'name': line.strip(),
                            'id': f'task_{i}',
                            'created_at': datetime.now().isoformat()
                        }
                        tasks.append(task)

            # Process and return tasks
            task_count = len(tasks)

            if task_count > 0:
                # In a real application, you would save these tasks to a database
                # For now, just return them in the response
                return JsonResponse({
                    'status': 'success',
                    'message': f'Successfully processed {task_count} tasks',
                    'tasks': tasks
                })
            else:
                return JsonResponse({
                    'status': 'warning',
                    'message': 'No tasks found in the imported data'
                })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error importing tasks: {str(e)}'
            })

    # If not POST, return error
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})