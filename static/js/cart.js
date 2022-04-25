//csrf_token

///////////////////////////////////////////////////////////////////////

var updateButtons = document.getElementsByClassName("update-cart")
for(i=0;i<updateButtons.length;i++){
    updateButtons[i].addEventListener('click',function(){
    var productId = this.dataset.product_id
    var action = this.dataset.product_action
    console.log(productId,action)
    console.log(user)

    var url = '/update_cart/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken': csrftoken,
			},
			body:JSON.stringify({'productId':productId, 'action':action })
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		   location.reload()
		});
    }
    )
}
