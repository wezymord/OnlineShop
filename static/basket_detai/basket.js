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
        var product_id = this.id;
        var display_quantity_products = $('.display_quantity_products');
        var total_basket_price = $('.total-basket-price');
        var display_price_basket = 0;
        var products_in_basket = display_quantity_products.data('value');

        // Quantity all products and total price in button
        if($.inArray(product_id, products_in_basket) === -1) {
            if($.inArray(product_id, product_in_basket) === -1) {
                product_in_basket.push(product_id);
                display_quantity_products.text(parseInt(display_quantity_products.text()) + 1);
                display_price_basket += parseFloat(this.name);
            }
        }

        total_basket_price.text((parseFloat(total_basket_price.text()) + parseFloat(display_price_basket)).toFixed(2) + ' EUR');

        $.ajax({
            type: "POST",
            url: "/basket/",
            data: {
                'product_id': this.id,
                'quantity_product': 1
            }
        });
    });


    $('.quantity_products').change(function () {
        var product_id = this.id;
        var quantity_product = this.value;
        var price_per_product = this.dataset.inlineType;

        // Subtotal product price in basket and dropdown
        var dropdown_product_price = $('.dropdown-product-price');
        var subtotal_product_price = $('.subtotal-product-price');
        $.each(subtotal_product_price, function (index, subtotal_product_price) {
            if (product_id === subtotal_product_price.id) {
                subtotal_product_price.innerHTML = (parseFloat(quantity_product) * parseFloat(price_per_product)).toFixed(2) + ' EUR';

                $.each(dropdown_product_price, function (index, value) {
                    if (product_id === value.id) {
                        value.innerHTML = (parseFloat(price_per_product) * parseInt(quantity_product)).toFixed(2);
                    }
                });
            }
        });

        // Total products price in basket and dropdown
        var dropdown_basket_price = $('.dropdown-basket-price');
        var total_basket_price = $('.total-basket-price');
        var summary_price = 0;
        var quantity_product_selected = $('.quantity_products option:selected');
        $.each(quantity_product_selected, function (index, value) {
            summary_price += parseFloat(value.value * value.id);
        });

        total_basket_price.text((summary_price).toFixed(2) + ' EUR');
        dropdown_basket_price.text((summary_price).toFixed(2) + ' EUR');

        // Quantity product in dropdown
        var dropdown_product_quantity = $('.dropdown-product-quantity');
        $.each(dropdown_product_quantity, function (index, value) {
            if (product_id === value.id) {
                value.innerHTML = quantity_product;
            }
        });


        $.ajax({
            type: "PUT",
            url: "/basket/" + product_id,
            data: {
                'product_id': product_id,
                'quantity_product': quantity_product
            }
        });
    });


    // Removing product from basket
    $('.remove-from-cart').click(function () {
        var selected_product = $('.selected-product');
        var product_id = this.id;
        var summary_price = 0;
        var display_quantity_products = $('.display_quantity_products');
        var subtotal_product_price = $('.subtotal-product-price');
        var total_basket_price = $('.total-basket-price');

        $.each( selected_product, function(index, value) {
            if (product_id === value.id) {
                summary_price += parseInt(total_basket_price.text()) - parseInt(value.dataset.inlineType);
                display_quantity_products.text(parseInt(display_quantity_products.text()) - 1);
                value.remove()
            };
        });

        subtotal_product_price.text((summary_price).toFixed(2) + ' EUR');
        total_basket_price.text((summary_price).toFixed(2) + ' EUR');

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