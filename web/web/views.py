from django.shortcuts import render

from .mars import Mars

mars = Mars()


def index(request):
    return render(request, 'index.html', {})


def analyse_code(request):
    source_code = request.POST.get("source_code", None)
    recommendations = mars.analysis(source_code)
    source_code_lines_list = list()
    recommendations_list = list()
    for line in source_code.split('\n'):
        source_code_lines_list.append(line)
    for line in recommendations.strip(' \t\n\r').split('\n'):
        recommendations_list.append(line+'\n')
    return render(request, 'index.html', {"source_code": source_code_lines_list, "recommendations": recommendations_list})


def upload_file(request):
    source_code_file = request.FILES["source_code"]
    source_code_lines_list = list()
    for line in source_code_file.read().decode("utf-8").split('\n'):
        source_code_lines_list.append(line)
    return render(request, 'index.html', {"source_code": source_code_lines_list})
