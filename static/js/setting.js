
//execute after document is loaded(does not wait for stylesheet)
document.addEventListener('DOMContentLoaded', function() {
	//generate % picker list
	list_generator();
});

//After everything(including css, img...) is fully loaded
window.addEventListener('load', function () {
	option_clicked();
	detect_num();
});

function　option_clicked(){
	//when lower bound option is clicked, toggle option picker 
	$('div#bound, div#start, div#end').click(function(){
		current = this.id;
		gsap.to('div.'+current, {
	        duration: 0.3,
	        y: -window.innerHeight
	    }).play();
		//make sure displayed number & picker position are on the same spot
		if(current=='bound'){
			setTimeout(function(){$('ul#bound').animate({scrollTop: (parseInt($('input.bound').val(),10)-2)*60}, 0)}, 200);	
		}else if(current=='start'){
			setTimeout(function(){$('ul#start').animate({scrollTop: (parseInt($('input.start').val(),10)-1)*60}, 0)}, 200);	
		}else if(current=='end'){
			setTimeout(function(){$('ul#end').animate({scrollTop: (parseInt($('input.end').val(),10)-12)*60}, 0)}, 200);	
		}

	});
	//when user click outside of option picker, untoggle the option picker 
	$('.pop-up').click(function(event){
		if (!event.target.matches('.pop-up-bg, .list')) {
			gsap.to(".pop-up", {
		        duration: 0.3,
		        y: window.innerHeight
		    }).play();
		}
	}); 
}

//executed once input box is blured after focused
function verify_value(){
	//if value entered null or 0
	if($('.goal-value').val() == 0 || $('.goal-value').val() == null){
		$('.goal').css({'border-bottom': 'solid #F15837 1.5px'});
		$('.hint').css({'color': '#F15837'});
	}else{	//back to normal otherwise
		$('.goal').css({'border-bottom': 'solid #e6e6e8 1.5px'});
		$('.hint').css({'color': '#BBBCBE'});
	}
}

//generate % picker list
function list_generator(){
	for (i = 0; i < 100; i++) {
		$('ul#bound').append('<div class="list">'+i+'%</div>');
	}
	for (j = 1; j < 24; j++) {
		if(j<12){
			$('ul#start').append('<div class="list">'+j+' : 00</div>');
		}else{
			$('ul#end').append('<div class="list">'+j+' : 00</div>');
		}
	}
}

//executed when 'done' button is clicked 
function detect_num(){
	$('span#bound').click(function(){
		//set displayed value to user's preference
		$('input.bound').val(Math.round($('ul#bound').scrollTop()/60));
	});
	$('span#start').click(function(){
		//set displayed value to user's preference
		$('input.start').val(Math.round($('ul#start').scrollTop()/60)+1);
	});
	$('span#end').click(function(){
		//set displayed value to user's preference
		$('input.end').val(Math.round($('ul#end').scrollTop()/60)+12);
	});
}