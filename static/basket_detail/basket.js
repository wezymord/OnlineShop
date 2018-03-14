$(document).ready(function() {

    function getCookie(c_name){

        if (document.cookie.length > 0)
        {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1)
            {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start,c_end));
            }
        }
        return "";
    }

     $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });

    $("button").click(function() {
        $.ajax({
            type: "POST",
            url: "/main_page/",
            data: {
                'product_id': this.id
            }
        });
    });

    var sum = 0;
    $('.product_amount').change(function() {
        var product_amount = this.value;
        var product_amount_selected = $('.product_amount option:selected');
        var product_id = this.id;
        var price_per_product = this.dataset.inlineType;
        var product_price = $('.product_price');
        var total_product_price = parseInt(product_amount) * parseFloat(price_per_product);
        var all_product_price = $('#total_price');
        var total_price = 0;

        $.each( product_price, function( index, value) {
        if (product_id === value.id) {
            value.innerHTML = total_product_price  + ' EUR';
            };
        });

        $.each( product_amount_selected, function( index, value) {
            if (parseInt(value.value) > 1) {
                total_price += parseFloat(value.value) * parseFloat(value.id);
            } else {
                total_price += parseFloat(value.value) * parseFloat(value.id);
            }
        });

        all_product_price.text(total_price + ' EUR');

        $.ajax({
            type: "POST",
            url: "/basket/",
            data: {
                'product_id_add': this.id,
                'product_amount': this.value
            }
        });
    });

    $('.remove-from-cart').click(function() {
        var product = $('.current_product');
        var product_id = this.id;
        });

        $.ajax({
            type: "POST",
            url: "/basket/",
            data: {
                'product_id_remove': this.id,
            }
        });
    });

});