(function ($) {
	$( document ).ready( function () {
		init();
	});
	
	function init() {
		$("#cuenco_submit").click(function(){  
			$.post($SCRIPT_ROOT + "/_urlgen", {url: $("#url").val()}, function(data) {
				$("#url").val((data.result));
			}); 
		});
		
		$('#url').keypress(function (e) {
		  if (e.which == 13) {
			$.post($SCRIPT_ROOT + "/_urlgen", {url: $("#url").val()}, function(data) {
				$("#url").val((data.result));
			}); 
		  }
		});		
		
		$("#url").click(function() {
			if ($("#url").val() == 'Enter a URL to shorten.') {
				$("#url").val('');
			}
		});
		
		$("#url").blur(function() {
			if ($("#url").val() == '') {
				$("#url").val('Enter a URL to shorten.');
			}
		});
	}
})(jQuery);