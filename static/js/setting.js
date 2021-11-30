
//execute after document is loaded(does not wait for stylesheet)
document.addEventListener('DOMContentLoaded', function() {
	//generate % picker list
	list_generator();
});

//After everything(including css, img...) is fully loaded
window.addEventListener('load', function () {
	lower_bound_clicked();
	detect_num();
});

function　lower_bound_clicked(){
	//when lower bound option is clicked, toggle option picker 
	$('#bound').click(function(){
		gsap.to(".pop-up", {
	        duration: 0.3,
	        y: -window.innerHeight
	    }).play();
		//make sure displayed number & picker position are on the same spot
		setTimeout(function(){$(".picker-list").animate({scrollTop: (parseInt($('.pnum').text(),10)-1)*60}, 0)}, 300);
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
	for (i = 1; i < 100; i++) {
		$('.picker-list').append('<div class="list">'+i+'%</div>');
	}
}

//executed when 'done' button is clicked 
function detect_num(){
	$('.pop-up button').click(function(){
		//set displayed value to user's preference
		$('.pnum').text(Math.round($('.picker-list').scrollTop()/60)+1);
	});
	
}