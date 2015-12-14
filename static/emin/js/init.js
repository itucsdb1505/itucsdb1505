$(function(){

	$("#form").validate({
		rules: {
			name: {
				required: true,
				minlength: 2,
			},
			population:{
				required: true,
				number:true
			},
			coordinates:{
				number:true
			},
			classification: {
				required: true,
				digits:true
			},
			title:{
				required: true
			},
			phone: {
				required: true,
				number: true,
				minlength: 11
			},
			mail: {
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
				required: 'This field is required',
				number: 'Please enter a valid number'
			},
			coordinates:{
				number: 'Please enter a valid number'
			},
			classification: {
				required: 'This field is required',
				digits:'Please enter only digits'
			},
			title: {
				required: 'This field is required'
			},
			phone: {
				required: 'This field is required',
				number: 'Invalid phone number',
				minlength: 'Length: 11'
			},
			mail: {
				required: 'This field is required',
				email: 'Invalid e-mail address'
			},
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
