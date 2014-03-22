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
			$.ajax({
				type: 'GET',
				url: $SCRIPT_ROOT + '/graph',
				contentType: 'application/json; charset=utf-8',
				data: {'uid': search_uid},
				success: function(data) {
					json = eval("("+data+")");

					var nodes = json.nodes;
					var links = json.links;

					weiboGraph.addNodes(nodes);
					weiboGraph.addLinks(links);
					weiboGraph.update();
				},
				error: function(data) {
					$('#loading-div').hide();
					alert('Ajax to get graph occur error.')
				}
			});
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
	
	/*---------- start iframe ------------*/
	$('iframe').load(function() {
		$('#loading-div').hide();
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
					$('#loading-div').show();
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
							$('#loading-div').hide();
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