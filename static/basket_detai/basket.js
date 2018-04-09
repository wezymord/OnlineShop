$(document).ready(function() {

    function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');


      function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }


    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    $(".add_to_basket").click(function () {
        var display_quantity_products = $('.display_quantity_products');
        var dispal_price_basket = $('.dispal_price_basket');
        var display_price_basket = 0;
        var products_in_basket = display_quantity_products.data('value');


        if($.inArray(this.id, products_in_basket) === -1) {
            display_quantity_products.text(parseInt(display_quantity_products.text()) + 1);
            display_price_basket += parseFloat(this.name);
        }

        dispal_price_basket.text((parseFloat(dispal_price_basket.text()) + parseFloat(display_price_basket)).toFixed(2) + ' EUR');

        $.ajax({
            type: "POST",
            url: "/basket/",
            data: {
                'product_id': this.id,
                'product_amount': 1
            }
        });
    });


    $('.product_amount').change(function () {
        var product_amount = this.value;
        var product_quantity = $('.product_quantity');
        var product_amount_selected = $('.product_amount option:selected');
        var product_id = this.id;
        var price_product_order = $('.price_product_order');
        var price_per_product = this.dataset.inlineType;
        var product_price = $('.product_price');
        var total_product_price = (parseFloat(product_amount) * parseFloat(price_per_product)).toFixed(2);
        var all_price = $('.total_price');
        var dispal_price_basket = $('.dispal_price_basket');
        var total_price = 0;

        $.each(product_price, function (index, product_price) {
            if (product_id === product_price.id) {
                product_price.innerHTML = total_product_price + ' EUR';

                $.each(price_product_order, function (index, value) {
                    if (product_id === value.id) {
                        value.innerHTML = (parseFloat(price_per_product) * parseInt(product_amount)).toFixed(2);
                    }
                });
            }
        });

        $.each(product_amount_selected, function (index, value) {
            if (parseInt(value.value) > 1) {
                total_price += parseFloat(value.value) * parseFloat(value.id);
            } else {
                total_price += parseFloat(value.value) * parseFloat(value.id);
            }
        });

        $.each(product_quantity, function (index, value) {
            if (product_id === value.id) {
                value.innerHTML = product_amount;
            }
        });

        all_price.text(parseFloat(total_price).toFixed(2) + ' EUR');
        dispal_price_basket.text(parseFloat(total_price).toFixed(2) + ' EUR');

        $.ajax({
            type: "PUT",
            url: "/basket/" + this.id,
            data: {
                'product_id': this.id,
                'product_amount': this.value
            }
        });
    });


    $('.remove-from-cart').click(function () {
        var product = $('.current_product');
        var product_id = this.id;
        var total_price = 0;
        var all_price = $('.total_price');
        var dispal_price_basket = $('.dispal_price_basket');
        var display_quantity_products = $('.display_quantity_products');

        $.each( product, function(index, value) {
            if (product_id === value.id) {
                total_price += parseInt(dispal_price_basket.text()) - parseInt(value.dataset.inlineType);
                display_quantity_products.text(parseInt(display_quantity_products.text()) - 1);
                value.remove()
            };
        });

        all_price.text((total_price).toFixed(2) + ' EUR');
        dispal_price_basket.text((total_price).toFixed(2) + ' EUR');

        $.ajax({
            type: "DELETE",
            url: "/basket/" + this.id,
            data: {
                "product_id": this.id
            }
        });
    });

    $(".shipping-method").focus(function() {
        var id = this.id;
        var product_price = $("label");
        var products_price = $('.products-cost').html();
        var total_price = $('.shipping-total');
        var shipping_price = 0;

        $.each( product_price, function(index, value) {
            if (parseInt(id) === index+1) {
                shipping_price += parseInt(value.id);
                $('.shipping-cost').html((parseFloat(value.id)).toFixed(2) + ' EUR');
            }
        });

        total_price.html((parseFloat(products_price) + shipping_price).toFixed(2) + ' EUR')
    });
});