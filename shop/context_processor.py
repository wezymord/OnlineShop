def add_variable_to_context(request):
    if 'basket' in request.session.keys():
        return {'amount_products': len(request.session['basket'].keys())}
    else:
        return {'amount_products': 0}

