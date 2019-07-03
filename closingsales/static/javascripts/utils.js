(function(win) {
	'use strict';

	var utils = {};
	utils.extract = function(str) {
		var index = str.indexOf('</p>');
		if (index == -1) return str;
		return str.substring(0, index + 4);
	}

	utils.isAdblockerActive = function(fn) {
		var adBlockEnabled = false;
		var testAd = document.createElement('div');
		testAd.innerHTML = '&nbsp;';
		testAd.className = 'adsbox';
		document.body.appendChild(testAd);
		window.setTimeout(function() {
		  if (testAd.offsetHeight === 0) {
		    adBlockEnabled = true;
		  }
		  testAd.remove();
		  fn(adBlockEnabled);
		}, 100);
	}
	window.utils = utils;
}(window));
