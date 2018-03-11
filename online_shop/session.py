

# def setSession(request):
#     request.session['counter'] = 0
#     return HttpResponse('Session activated')



@csrf_exempt
def addToSession(request):
    html = '''
            <form method="POST">
                <label>
                    Klucz:
                    <input type="text" name="key">
                </label>
                <label>
                    Wartość:
                    <input type="text" name="value">
                </label>
                <input type="submit" name="convertionType">
            </form>
           '''
    if request.method == 'GET':
        products = Product.objects.all()
        photos = []
        for product in products:
            for url in product.photo.all():
                photos.append(url.image_urls)
        p = 1
        if 'p' in request.session:
            request.session['p'] = request.session['p'] + 1
        else:
            request.session['p'] = 1

        ctx = {
            'photos': photos,
            'products': products,
            "p": p
        }

        return render(request, 'index.html', ctx)

    elif request.method == 'POST':
        key = request.POST.get('p')
        value = request.POST.get('p')
        request.session[key] = value
        return HttpResponse('<p>Added</p>' + html)

def showAllSession(request):
    html = '<table border=1>'
    for k, v in request.session.items():
        html += '<tr><td>{}</td><td>{}</td></tr>'.format(k, v)
    html += '</table>'
    return HttpResponse(html)

# def deleteSession(request):
#     del request.session['counter']
#     return HttpResponse('Delete session succes')