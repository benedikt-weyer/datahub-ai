import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

def data_description(request):
    
    inactive_table_names_request = requests.get('http://datahub-ai:8001/api/data-description/inactive-table-names', params=request.GET)

    context = {
        'inactive_table_names': inactive_table_names_request.json().get('inactive-table-names')
    }


    return render(request, 'app/data_description.html', context)


def ai_chat(request):
    #TODO: update this function to make a POST call to localhost:8001/query
    #q = request.GET.get('q')
    
    
    
    
    #return JsonResponse({'response': f'{q}'})

    return render(request, 'app/ai_chat.html')