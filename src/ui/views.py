import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from datetime import datetime
import json

def data_description_download(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'export_descriptions':
            try:
                response = requests.get('http://datahub-ai:8001/api/data-description/active-tables')
                response.raise_for_status()
                active_tables = response.json().get('active-tables')
                formated_active_tables = [{'table_name': table.get('table_name'), 'table_description': table.get('table_description')} for table in active_tables]

                response_content = json.dumps({'active_tables': formated_active_tables}, indent=4)

                response = HttpResponse(response_content, content_type="application/json")
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
                response['Content-Disposition'] = f'attachment; filename=datahub_active_tables_export_{timestamp}.json'
                return response
            except requests.RequestException as e:
                return JsonResponse({'error': 'Failed to export table descriptions', 'details': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Invalid form type'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def data_description(request):
    # --form processing--
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'update_table':
            table_name = request.POST.get('table_name')
            table_description = request.POST.get('table_description')
            
            try:
                response = requests.put(
                    'http://datahub-ai:8001/api/data-description/active-tables',
                    json={
                        'table_name': table_name,
                        'table_description': table_description
                    }
                )
                response.raise_for_status()
            except requests.RequestException as e:
                return JsonResponse({'error': 'Failed to update table description', 'details': str(e)}, status=500)
        
        if form_type == 'add_table':
            table_name = request.POST.get('table_name')
            
            try:
                response = requests.post(
                    'http://datahub-ai:8001/api/data-description/active-tables',
                    json={
                        'table_name': table_name
                    }
                )
                response.raise_for_status()
            except requests.RequestException as e:
                return JsonResponse({'error': 'Failed to add table', 'details': str(e)}, status=500)
        
        if form_type == 'remove_table':
            table_name = request.POST.get('table_name')
            
            try:
                response = requests.delete(
                    'http://datahub-ai:8001/api/data-description/active-tables',
                    json={'table_name': table_name}
                )
                response.raise_for_status()
            except requests.RequestException as e:
                return JsonResponse({'error': 'Failed to remove table', 'details': str(e)}, status=500)
            
        
        if form_type == 'import_descriptions':
            try:
                file = request.FILES['file']
                file_content = file.read()
                file_data = json.loads(file_content)
                print(file_data, flush=True)
                print('file-data', flush=True)
                response = requests.post(
                    'http://datahub-ai:8001/api/data-description/active-tables/import',
                    json={'file_data': file_data}
                )
                response.raise_for_status()
            except requests.RequestException as e:
                return JsonResponse({'error': 'Failed to import table descriptions', 'details': str(e)}, status=500)
        
        
    # --fetch data--
    try:
        inactive_table_names_request = requests.get('http://datahub-ai:8001/api/data-description/inactive-table-names', params=request.GET)
        inactive_table_names_request.raise_for_status()
        inactive_table_names = inactive_table_names_request.json()
    except requests.RequestException as e:
        return JsonResponse({'error': 'Failed to fetch inactive table names', 'details': str(e)}, status=500)

    try:
        active_tables_request = requests.get('http://datahub-ai:8001/api/data-description/active-tables', params=request.GET)
        active_tables_request.raise_for_status()
        active_tables = active_tables_request.json()
    except requests.RequestException as e:
        return JsonResponse({'error': 'Failed to fetch active tables', 'details': str(e)}, status=500)

    context = {
        'inactive_table_names': inactive_table_names.get('inactive-table-names'),
        'active_tables': active_tables.get('active-tables')
    }

    return render(request, 'app/data_description.html', context)


def ai_chat(request):

    return render(request, 'app/ai_chat.html')