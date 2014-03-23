$(function() {
	/*--------- start crawl form -----------*/
	$('#crawl-btn').click(function (event) {
		$('.bubble-box').show();
		$('.bubble-box').focus();
	});
	$('.bubble-box input').focus(function (event) {
		$('.bubble-box').show();
	});
	$('.bubble-box input').blur(function (event) {
		$('.bubble-box').hide();
	});
	$('.bubble-box').focus(function (event) {
		$('.bubble-box').show();
	});
	$('.bubble-box').blur(function (event) {
		$('.bubble-box').hide();
	});
	/*---------- end crawl form ------------*/

	/*---------- start search  ------------*/
	$('.nav input').click(function (event) {
		$(this).select();
	});
	$('#search-input').on('search', function (event) {
		var search_nick = $.trim($(this).val());
		if (search_nick == '')
			return;
		var search_uid = '';
		var dataList = $("#search-result");
		var options = $("#search-result").children();
		for (var i = 0; i < options.length; i++) {
			if (search_nick == options[i].value) {
				search_uid = $(options[i]).attr('id').replace('uid_', '');
			}
		}
		if (search_uid != '') {
			$('#loading-div').show();
			changeGraphAjax(search_uid);
		} 
	});
	$('#search-input').on('input', function (event) {
		var val = $(this).val();
		if(val === '') return;
		$.get($SCRIPT_ROOT + '/search', {keyword:val}, function(data) {
			var dataList = $("#search-result");
			dataList.empty();
			json = eval("("+data+")");
			for (var i = 0; i < json.length; i++) {
				var opt = $('<option id="uid_' + json[i]['uid'] + '"></option>').attr('value', json[i]['nick']);
				dataList.append(opt);		
			}
		},"json");
	});
	/*---------- end search result ------------*/
});

function crawl() {
	var crawl_uid = $.trim($('#crawl_uid').val());
	var username = $.trim($('#username').val());
	var pwd = $.trim($('#pwd').val());
	if (crawl_uid == '' || username == '' || pwd == '') {
		$('#bubble-box-error').html('Please check your input.');
		return;
	}
	$.ajax({
		type: 'POST',
		url: $SCRIPT_ROOT + '/crawl',
		contentType: 'application/json; charset=urf-8',
		data: { 'crawl_uid': crawl_uid,
				'username': username,
				'pwd': pwd},
		success: function(data) {
			// json = eval("("+data+")");
			alert(data);
		},
		error: function(data) {
		}
	});
}
