var search_button = document.getElementsByClassName("search-form")
search_button[0].addEventListener('click' ,async()=>{
var query = document.getElementById("search_query")
query = query.value
var url = '/search/'

		const response = await fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken': csrftoken,
			},
			body:JSON.stringify({'query':query})
		})
		response.json()
		.then(res => {
		console.log(res[0].fields.image)
		const element = document.getElementsByTagName('body')[0];
		element.innerHTML =
		`<div class="col-md-4">
		         <div class="card mb-4 box-shadow">
                        <img class="card-img-top" src=/images/${res[0].fields.image} width="300" height="210"
                             alt="Card image cap">
                        <div class="card-body">
                            <strong><p class="card-text text-dark">${res[0].fields.product_name}</p></strong>
                            <hr>
                            <p class="text-muted text-truncate">${res[0].fields.description}</p>
                            <div class="d-flex justify-content-between align-items-center">
                                <div class="btn-group">
                                    <button type="button" class="btn btn-sm btn-outline-primary"><a
                                            style="text-decoration:none"
                                            href= /product_view/${res[0].pk}>View & Add to Cart</a></button>
                                </div>
                                <strong class="card-text">$ ${res[0].fields.price}</strong>
                            </div>
                        </div>
                    </div>
                </div>`;
		})
}
);
