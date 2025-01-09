import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

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
    #TODO: update this function to make a POST call to localhost:8001/query
    #q = request.GET.get('q')
    
    
    
    
    #return JsonResponse({'response': f'{q}'})

    return render(request, 'app/ai_chat.html')