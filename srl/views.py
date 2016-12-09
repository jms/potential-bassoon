from r andom import randrange
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.models import User
from srl.models import ShortURL
from srl.forms import SrlForm
from srl.services.parse import encode


# Create your views here.

def index(request):
    if request.method == 'POST':
        form = SrlForm(request.POST)
        if form.is_valid():
            random_user = get_random_user()
            url = form.cleaned_data['url']
            surl, created = ShortURL.objects.get_or_create(url=url)
            if created:
                code = encode(surl.id)
                surl.submitter = random_user
                surl.code = code
                surl.save()
            else:
                code = surl.code

            return HttpResponseRedirect('/!{}'.format(code))
    else:
        form = SrlForm()

    return render(request, 'srl/index.html', {'form': form})


def resolve(request, code):
    query_set = ShortURL.objects.filter(code=code)
    if query_set:
        srl_record = query_set[0]
        return redirect(srl_record.url)
    else:
        return HttpResponseNotFound('URL not found')


def details(request, detail):
    code = detail.replace('!', '')
    query_set = ShortURL.objects.filter(code=code)
    if query_set:
        srl_record = query_set[0]
        return render(
            request,
            'srl/details.html',
            {
                'data': srl_record,
                'host': request.get_host()
            }
        )
    else:
        return HttpResponseNotFound('URL Not Found')


def get_random_user():
    users = User.objects.values('id').all()
    ids = []
    for item in users:
        ids.append(item.get('id'))
    count = len(ids)
    pos = randrange(0, count, 1)
    random_id = ids[pos]
    random_user = User.objects.filter(id=random_id)[0]
    return random_user
