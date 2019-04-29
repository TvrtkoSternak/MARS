from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {})


def analyse_code(request):
    print("hello")
    source_code_file = request.FILES["source_code"]
    source_code_lines_list = list()
    for line in source_code_file.read().decode("utf-8").split('\n'):
        source_code_lines_list.append(line)
    return render(request, 'index.html', {"source_code": source_code_lines_list})
