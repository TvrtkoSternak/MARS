from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render(None,request))

def upload(request):
    id = request.POST['id']
    path = '/var/www/pictures/%s' % id
    f = request.FILES['picture']
    destination = open(path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    # return HttpResponse(open(path).read())
