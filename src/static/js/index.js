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
	$('#search-input').keyup(function (event) {
		if (event.keyCode == 13) {
			alert('aaaaaaaa--');
		}
	});
	$('#search-input').on('input', function (event) {
		if (event.keyCode == 13) {
			$('#loading').show();
			$('iframe').hide();
			uid = $(this).attr('id').replace('uid_', '');
			$.ajax({
				type: 'GET',
				url: $SCRIPT_ROOT + '/change_graph',
				contentType: 'application/html; charset=utf-8',
				data: {'uid': uid},
				success: function(data) {
					json = eval("("+data+")");
					if (json.isSucceed) {
						//$('#user_info').html('uid:"'+json.uid+'", nick:"'+json.nick+'", follows:"'+json.follows+'", fans:"'+json.fans+'", db_follows:"'+json.db_follows+'", db_fans:"'+json.db_fans+'"}');
						$('iframe').attr('src', '/graph?uid='+json.uid);
					} else {
						alert('Get graph failed.')
					}
				},
				error: function(data) {
					$('#loading').hide();
					$('iframe').show();
					alert('Ajax to get graph occur error.')
				}
			});
		} else{
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
				$("#search-result option").each(function(index) {
				 	$(this).click(function (event) {
				 		alert('aaa');
				 	});
				});
				
			},"json");
		}
	});
	/*---------- end search result ------------*/
	
	/*---------- start iframe ------------*/
	$('iframe').load(function() {
		$('#loading').hide();
	    $('iframe').show();
	});


});


/*function search() {
	var keyword = $.trim($('#search-input').val());
	if (keyword != '') {
		$('#search-result-box').html('');
		$.ajax({
			type: 'GET',
			url: $SCRIPT_ROOT + '/search',
			contentType: 'application/json; charset=utf-8',
			data: {'keyword': keyword},
			success: function(data) {
				json = eval("("+data+")");
				var htmlStr = '';
				for (var i = 0; i < json.length; i++) {
					htmlStr = '<li id="uid_' + json[i]['uid'] + '">' + json[i]['nick'] + '</li>';
					$('#search-result-box').append(htmlStr);
				}
				$('#search-result-box li').click(function(event) {
					$('#loading').show();
					$('iframe').hide();
					uid = $(this).attr('id').replace('uid_', '');
					$.ajax({
						type: 'GET',
						url: $SCRIPT_ROOT + '/change_graph',
						contentType: 'application/html; charset=utf-8',
						data: {'uid': uid},
						success: function(data) {
							json = eval("("+data+")");
							if (json.isSucceed) {
								//$('#user_info').html('uid:"'+json.uid+'", nick:"'+json.nick+'", follows:"'+json.follows+'", fans:"'+json.fans+'", db_follows:"'+json.db_follows+'", db_fans:"'+json.db_fans+'"}');
								$('iframe').attr('src', '/graph?uid='+json.uid);
							} else {
								alert('Get graph failed.')
							}
						},
						error: function(data) {
							$('#loading').hide();
							$('iframe').show();
							alert('Ajax to get graph occur error.')
						}
					});
				});
				$('#search-result-box').show();
			}
		});
	}
}*/