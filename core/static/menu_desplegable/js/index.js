// Dropdown Menu
var dropdown = document.querySelectorAll('.dropdown');
var dropdownArray = Array.prototype.slice.call(dropdown,0);
dropdownArray.forEach(function(el){
	var button = el.querySelector('a[data-toggle="dropdown"]'),
			menu = el.querySelector('.dropdown-menu'),
			arrow = button.querySelector('i.icon-arrow');

	button.onclick = function(event) {
		if(!menu.hasClass('show')) {
			menu.classList.add('show');
			menu.classList.remove('hide');
			if(arrow){
				arrow.classList.add('open');
				arrow.classList.remove('close');
			}
			event.preventDefault();
		}
		else {
			menu.classList.remove('show');
			menu.classList.add('hide');
			if(arrow){
				arrow.classList.remove('open');
				arrow.classList.add('close');
			}
			event.preventDefault();
		}
	};
})


$(window).click(function(){
	var menu = $('.dropdown .show')[0];
	if(menu){
		var arrow = $('.dropdown .icon-arrow')[0];
		menu.classList.remove('show');
		menu.classList.add('hide');
		if(arrow){
			arrow.classList.remove('open');
			arrow.classList.add('close');
		}

	}
});


Element.prototype.hasClass = function(className) {
    return this.className && new RegExp("(^|\\s)" + className + "(\\s|$)").test(this.className);
};