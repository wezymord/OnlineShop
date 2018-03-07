from django import template

register = template.Library()

@register.filter(name='get_title_photo')
def get_title_photo(product):
    photos = product.photo.all()
    photo = []
    for url in photos:
        photo.append(url.image_urls)

    return photo[0]
