from django.shortcuts import render,redirect, HttpResponse

def index(request):
    return render(request,'first_app/index.html')

def result(request):
    if request.method == 'POST':
        print (request.POST)
        request.session['name'] = request.POST['name']
        request.session['city'] = request.POST['city']
        request.session['language'] = request.POST['language']
        request.session['comment'] = request.POST['comment']
        return redirect('/result')

    context = {
        'name':request.session['name'],
        'city':request.session['city'],
        'language':request.session['language'],
        'comment':request.session['comment']
    }

    return render(request,'first_app/result.html', context)
