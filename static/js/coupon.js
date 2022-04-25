//csrf_token

///////////////////////////////////////////////////////////////////////


var coupon_button = document.getElementsByClassName("coupon_button")
coupon_button[0].addEventListener('click',function(){

    const coupon_code = document.getElementById('coupon_code')
    var code = coupon_code.value;

    var url = '/apply_coupon/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken': csrftoken,
			},
			body:JSON.stringify({'coupon_code':code})
		})
		.then((response) => {
//		   console.log(response,'response');
		   return response.json();
		})
		.then((data) => {
//		if (data.is_applied=='YES')
//		{
//		   var div = document.getElementById('final_value');
//		   div.innerHTML =  "Final Amount: " + " " + data.final_value;
//		}
//		else{
//		   var div = document.getElementById('final_value');
//		   div.innerHTML =  'Invalid coupon code';
//		}
		location.reload()
		});
})
