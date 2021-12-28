$(document).ready(function(){
    $( "a.nav" ).click(function( event ) {
        event.preventDefault();
        $("html, body").animate({ scrollTop: $($(this).attr("href")).offset().top }, 500);
    });

	$(window).scroll(function(){
			if($(window).scrollTop() > 100) {
				$('#scroll_top').show();
			} else {
				$('#scroll_top').hide();
			}
	});

	$('#scroll_top').click(function(){
		$('html, body').animate({scrollTop: 0}, 600);
		return false;
	});

	$('.first_summary').click(function(){
		$('.first_table').slideToggle(300, function(){
			if ($(this).is(':hidden')) {
				$('.first_summary').removeClass('active');
			} else {
				$('.first_summary').addClass('active');
			}
		});
		return false;
	});

	$('.second_summary').click(function(){
		$('.second_table_wrapper').slideToggle(300, function(){
			if ($(this).is(':hidden')) {
				$('.second_summary').removeClass('active');
			} else {
				$('.second_summary').addClass('active');
			}
		});
		return false;
	});

	$('.third_summary').click(function(){
		$('.third_table_wrapper').slideToggle(300, function(){
			if ($(this).is(':hidden')) {
				$('.third_summary').removeClass('active');
			} else {
				$('.third_summary').addClass('active');
			}
		});
		return false;
	});

	$('.input_charge').click(function(){
		$('.charge_form').slideToggle(300, function(){
			if ($(this).is(':hidden')) {
				$('.input_charge').removeClass('active');
			} else {
				$('.input_charge').addClass('active');
			}
		});
		return false;
	});

	$('.input_payment').click(function(){
		$('.payment_form').slideToggle(300, function(){
			if ($(this).is(':hidden')) {
				$('.input_payment').removeClass('active');
			} else {
				$('.input_payment').addClass('active');
			}
		});
		return false;
	});

	$('#id_flats_form').change(function () {
		let option_text = $(this).val()
		let data = {
			selected_flat: option_text
		}
		let elems = $('.data')
		console.log(elems.length)

			$(".data").remove();


		$.ajax({
			url:'/selected_flat',
			type: 'get',
			data: data,
			success: function (data){
				let result = data['data']
				if (!result){
					$('.second_table').css('display', 'none')
				}
				else{
					$.each(result[0], function (index, value){
						$('.charges').append(
							'<td class="data">'+ value +'</td>'
						)
					})
					$.each(result[1], function (index, value){
						$('.payments').append(
							'<td class="data">'+ value+ '</td>'
						)
					})

				}
			}
		})
	});

	$(function () {
    	$("#id_datetime").datetimepicker({
      	format: 'Y-m-d H:i',
    	});
  	});

	$(function (){
		$('#payment_form #id_datetime').datetimepicker({
      	format: 'Y-m-d H:i',
    	});
	});

	$('#charge_form').on('submit', function (e){
		e.preventDefault();
		$.ajax({
			type: 'post',
			url: 'charge_input/',
			data: {
				charge_amount: $('#id_charge_amount').val(),
				charge_flat: $('#id_flat').val(),
				charge_date: $('#id_datetime').val(),
				csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
			},
			success:function (){
				alert("Добавлено");
			}
		})
	})

	$('#payment_form').on('submit', function (e){
		e.preventDefault();
		$.ajax({
			type: 'post',
			url: 'payment_input/',
			data: {
				payment_amount: $('#id_payment_amount').val(),
				payment_flat: $('#payment_form #id_flat').val(),
				payment_date: $('#payment_form #id_datetime').val(),
				csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
			},
			success:function (){
				alert("Добавлено");
			}
		})
	})
});