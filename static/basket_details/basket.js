$(document).ready(function() {

    function getCookie(c_name) {

        if (document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start, c_end));
            }
        }
        return "";
    }

    $.ajaxSetup({
        headers: {"X-CSRFToken": getCookie("csrftoken")}
    });


    var product_in_basket = [];
    $(".add_to_basket").click(function () {
        var product_amount_basket = $('.count');
        var all_price_main = $('.total_price_main');
        var total_price = 0;

        if($.inArray(this.id, product_in_basket) === -1) {
            product_amount_basket.text(parseInt(product_amount_basket.text()) + 1);
            total_price += parseInt(this.name);
        }
        product_in_basket.push(this.id);
        all_price_main.text(parseInt(all_price_main.text()) + total_price + ' EUR');

        $.ajax({
            type: "POST",
            url: "/basket/",
            data: {
                'product_id': this.id,
                'product_amount': 1
            }
        });
    });


    var sum = 0;
    $('.product_amount').change(function () {
        var product_amount = this.value;
        var product_amount_selected = $('.product_amount option:selected');
        var product_id = this.id;
        var price_per_product = this.dataset.inlineType;
        var product_price = $('.product_price');
        var total_product_price = parseInt(product_amount) * parseFloat(price_per_product);
        var all_price = $('.total_price');
        var all_price_main = $('.total_price_main');
        var total_price = 0;

        $.each(product_price, function (index, value) {
            if (product_id === value.id) {
                value.innerHTML = total_product_price + ' EUR';
            };
        });

        $.each(product_amount_selected, function (index, value) {
            if (parseInt(value.value) > 1) {
                total_price += parseFloat(value.value) * parseFloat(value.id);
            } else {
                total_price += parseFloat(value.value) * parseFloat(value.id);
            }
        });

        all_price.text(total_price + ' EUR');
        all_price_main.text(total_price + ' EUR');

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

        $.each( product, function( index, value) {
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


    $(".form-group input").blur(function() {

        $.ajax({
            type: "POST",
            url: "/checkout_address/",
            data: {
                'first_name': $('#checkout-fn').val(),
                'last_name': $('#checkout-ln').val(),
                'email': $('#checkout-email').val(),
                'phone_number': $('#checkout-phone').val(),
                'company': $('#checkout-company').val(),
                'country': $('#checkout-country').val(),
                'city': $('#checkout-city').val(),
                'postal_code': $('#checkout-zip').val(),
                'address1': $('#checkout-address1').val(),
                'address2': $('#checkout-address2').val()
            }
        });
    });
});