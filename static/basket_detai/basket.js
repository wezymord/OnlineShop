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


    var product_in_basket = [];
    $(".add_to_basket").click(function () {
        var product_amount_basket = $('.count');
        var all_price_main = $('.total_price_main');
        var total_price = 0;

        if($.inArray(this.id, product_in_basket) === -1) {
            product_amount_basket.text(parseInt(product_amount_basket.text()) + 1);
            total_price += parseFloat(this.name);
        }

        product_in_basket.push(this.id);
        all_price_main.text((parseFloat(all_price_main.text()) + parseFloat(total_price)).toFixed(2) + ' EUR');

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
        var all_price_main = $('.total_price_main');
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
        all_price_main.text(parseFloat(total_price).toFixed(2) + ' EUR');

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
        var all_price_main = $('.total_price_main');
        var product_amount_basket = $('.count');

        $.each( product, function(index, value) {
            if (product_id === value.id) {
                total_price += parseInt(all_price_main.text()) - parseInt(value.dataset.inlineType);
                product_amount_basket.text(parseInt(product_amount_basket.text()) - 1);
                value.remove()
            };
        });

        all_price.text(total_price + ' EUR');
        all_price_main.text(total_price + ' EUR');

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