$(function(){

	$("#form").validate({
		rules: {
			name: {
				required: true,
				minlength: 2
			},
			population:{
				required: true
			},
			title:{
				required: true
			},
			nation: {
				required: true
			},
			classification: {
				required: true,
			},
			phone: {
				required: true,
				number: true,
				minlength: 11
			},
			email: {
				required: true,
				email: true
			},
			message: {
				required: true
			}
		},
		messages: {
			name: {
				required: 'This field is required',
				minlength: 'Minimum length: 2'
			},
			population:{
				required: 'This field is required'
			},
			title: {
				required: 'This field is required'
			},
			nation: {
				required: 'This field is required'
			},
			classification: {
				required: 'This field is required'
			},
			phone: {
				required: 'This field is required',
				number: 'Invalid phone number',
				length: 'Length: 11'
			},
			email: 'Invalid e-mail address',
			message: {
				required: 'This field is required'
			}
		},
		success: function(label) {
			label.html('OK').removeClass('error').addClass('ok');
			setTimeout(function(){
				label.fadeOut(500);
			}, 2000)
		}
	});

});