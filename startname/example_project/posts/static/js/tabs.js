;(function($){
	$.fn.tabs = function(options){
		var settings = $.extend({
			enterAnimation: 'fadeIn',
			exitAnimation: 'fadeOut'
		}, options);
		var windowWidth = $(window).width();
		var parentWrappers = $(this);
		
		var createSelectDropdown = function(parentWrapper, currentTabId){
			var tabNavList = [];
			var tabNavs = parentWrapper.find('ul.tab-nav li a');
			$.each(tabNavs, function(index, navLink){
				var temp = {};
				temp.text = $(navLink).text();
				temp.target = $(navLink).attr('data-target');
				tabNavList.push(temp);
			});
			var select = '<select class="tab-nav"></select>';
			parentWrapper.prepend(select);
			$.each(tabNavList, function(index, navEle){
				parentWrapper.find('select.tab-nav').append('<option value="'+navEle.target+'"">'+navEle.text+'</option>');
			});
			parentWrapper.find('select.tab-nav').val(currentTabId);
		};

		var showNewTab = function(parentWrapper, targetTabId, initialize){
			parentWrapper.find('.tab-content').off();
			var currActiveTab = parentWrapper.find('.target-tabs .tab-content.active');
			var currActiveTabBtn = parentWrapper.find('ul.tab-nav li.active');
			var targetTab = parentWrapper.find('.target-tabs .tab-content#'+targetTabId);
			var targetTabBtn = parentWrapper.find('ul.tab-nav a[data-target="'+targetTabId+'"]').closest('li');	
			currActiveTab.removeClass('animated '+settings.enterAnimation);
			targetTab.removeClass('animated '+settings.exitAnimation);		
			//Perform animation on desktop only
			if(windowWidth > 640 && !initialize){
				currActiveTab.addClass('animated '+settings.exitAnimation).one('webkitAnimationEnd oanimationend oAnimationEnd msTransitionEnd animationend', function(){
					currActiveTab.removeClass('active');
					targetTab.addClass('active').addClass('animated '+settings.enterAnimation);
					currActiveTabBtn.removeClass('active');
					targetTabBtn.addClass('active');
				});
			}
			else{
				//Dont Perform animations on mobile
				currActiveTab.removeClass('active');
				targetTab.addClass('active');
				currActiveTabBtn.removeClass('active');
				targetTabBtn.addClass('active');
			}
		}

		var init = function(parentWrapper){
			parentWrapper = $(parentWrapper);
			//getInitiallyActiveTab
			var currentTabId = parentWrapper.find('ul.tab-nav li.active a').attr('data-target');
			//show initially active tab
			showNewTab(parentWrapper, currentTabId, true);
			//Create a selectDropdwn for smaller sceens
			createSelectDropdown(parentWrapper, currentTabId);
			parentWrapper.find('select.tab-nav').on('change', function(){
				var _this = $(this);
				var targetTabId = _this.val();
				var currTabId = parentWrapper.find('ul.tab-nav li.active a').attr('data-target');
				if(targetTabId != currTabId)
					showNewTab(parentWrapper, targetTabId, false);
			});
			parentWrapper.find('ul.tab-nav li').on('click', 'a', function(e){
				e.preventDefault();
				var _this = $(this);
				var targetTabId = _this.attr('data-target');
				var currTabId = parentWrapper.find('ul.tab-nav li.active a').attr('data-target');
				if(targetTabId != currTabId)
					showNewTab(parentWrapper, targetTabId, false);
				parentWrapper.find('select.tab-nav').val(targetTabId);
			});
			$(window).resize(function(){
				windowWidth = $(window).width();
			});
		};

		return this.each(function(index, node){
			//initialize different tab-wrappers in HTML
			init(node);
		});
	};
}(jQuery));


