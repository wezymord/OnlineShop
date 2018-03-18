def add_variable_to_context(request):
    if request.session.items():
        return {'amount_products': len(request.session['basket'].keys())}
    else:
        return {'amount_products': 0}

