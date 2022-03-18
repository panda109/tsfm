var valid = true;

//execute after document is loaded(does not wait for stylesheet)
document.addEventListener('DOMContentLoaded', function() {
	//generate % picker list
	list_generator();
	if($('input.gp').val()=='0'){
		$('input.gp').hide();
		$('.no-gp').show();
	}
});

//After everything(including css, img...) is fully loaded
window.addEventListener('load', function () {
	option_clicked();
	detect_num();
	detect_number();
	gsap.to(".loading", {
        duration: 0.15,
        opacity: 0,
		onComplete: function(){$('.loading').css("display","none");}
    }).play();
});

function detect_number(){
	$('#goal').keyup(function(){
		if ($(this).val() > 9999 || $('.goal-value').val() == 0 || $('.goal-value').val() == null){
			$('.goal').css({'border-bottom': 'solid #F15837 1.5px'});
			$('.goal-hint').css({'color': '#F15837'});
			$('#goal').css({'color': '#F15837'});
			$('.save-button').css({'pointer-events': 'none', 'color':'grey'});
		}else{
			$('.goal').css({'border-bottom': 'solid #e6e6e8 1.5px'});
			$('.goal-hint').css({'color': '#BBBCBE'});
			$('#goal').css({'color': 'black'});
			$('.save-button').css({'pointer-events': 'auto', 'color':'#174A9F'});
		}
	});
	$('#diff').keyup(function(){
		if ($(this).val() > 9999 || $('.diff-setting').val() == 0 || $('.diff-setting').val() == null){
			$('.diff').css({'border-bottom': 'solid #F15837 1.5px'});
			$('.diff-hint').css({'color': '#F15837'});
			$('#diff').css({'color': '#F15837'});
			$('.save-button').css({'pointer-events': 'none', 'color':'grey'});
		}else{
			$('.diff').css({'border-bottom': 'solid #e6e6e8 1.5px'});
			$('.diff-hint').css({'color': '#BBBCBE'});
			$('#diff').css({'color': 'black'});
			$('.save-button').css({'pointer-events': 'auto', 'color':'#174A9F'});
		}
	});
}

function　option_clicked(){
	//when lower bound option is clicked, toggle option picker 
	$('div#bound, div#start, div#end, div#gp').click(function(){
		current = this.id;
		gsap.to('div.'+current, {
	        duration: 0.3,
	        y: -window.innerHeight
	    }).play();
		//make sure displayed number & picker position are on the same spot
		if(current=='bound'){
			setTimeout(function(){$('ul#bound').animate({scrollTop: (parseInt($('input.bound').val(),10))*60}, 0)}, 200);	
		}else if(current=='start'){
			setTimeout(function(){$('ul#start').animate({scrollTop: (parseInt($('input.start').val(),10)-1)*60}, 0)}, 200);	
		}else if(current=='end'){
			setTimeout(function(){$('ul#end').animate({scrollTop: (parseInt($('input.end').val(),10)-12)*60}, 0)}, 200);	
		}else if(current=='gp'){
			if($('input.gp').val()!='0'){
				setTimeout(function(){$('ul#gp').animate({scrollTop: (parseInt($('input.gp').val(),10))*60}, 0)}, 200);
			}
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

//generate % picker list
function list_generator(){
	for (i = 0; i < 100; i++) {
		$('ul#bound').append('<div class="list">'+i+'</div>');
	}
	for (j = 1; j < 24; j++) {
		if(j<12){
			$('ul#start').append('<div class="list">'+j+'</div>');
		}else{
			$('ul#end').append('<div class="list">'+j+'</div>');
		}
	}
	for (l = 1; l < 11; l++) {
			$('ul#gp').append('<div class="list">'+l+'</div>');
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
	$('span#gp').click(function(){
		//set displayed value to user's preference
		$('input.gp').val(Math.round($('ul#gp').scrollTop()/60));
		if(Math.round($('ul#gp').scrollTop()/60 == 0)){
			$('input.gp').hide();
			$('.no-gp').show();
		}else{
			$('input.gp').show();
			$('.no-gp').hide();
		}
	});
}