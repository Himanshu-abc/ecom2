
    let auth_token;
    $(document).ready(function(){
        $.ajax({
            type: 'get',
            url: 'https://www.universal-tutorial.com/api/getaccesstoken',
            success: function(data){
                auth_token = data.auth_token
                getCountry(data.auth_token)
            },
            error: function(error){
                console.log(error);
            },
            headers: {
    "Accept": "application/json",
    "api-token": "FLuc1IEZ6LDaMu_yendreBM7bUDnCujjr-s-_O3C_Iwx85eWUIUyy2IRunHAOO9Cblw",
    "user-email": "himanshu.patidar@neosoftmail.com"
            }
        })
        $('#country').change(function(){
            getState();
        })
        $('#state').change(function(){
            getCity();
        })
    })
    function getCountry(auth_token){
        $.ajax({
            type: 'get',
            url: 'https://www.universal-tutorial.com/api/countries/',
            success: function(data){
                data.forEach(element => {
                    $('#country').append('<option value="'+element.country_name+'">'+element.country_name+'</option>');
                });
//                getState(auth_token)
            },
            error: function(error){
                console.log(error);
            },
            headers: {
                "Authorization": "Bearer "+ auth_token,
                "Accept": "application/json"
            }
        })
        }
    function getState(){
        let country_name = $('#country').val();
        $.ajax({
            type: 'get',
            url: 'https://www.universal-tutorial.com/api/states/'+country_name,
            success: function(data){
            $('#state').empty();
                data.forEach(element => {
                    $('#state').append('<option value="'+element.state_name+'">'+element.state_name+'</option>');
                });
//                getCity(auth_token)
            },
            error: function(error){
                console.log(error);
            },
            headers: {
                "Authorization": "Bearer "+ auth_token,
                "Accept": "application/json"
            }
        })
    }
    function getCity(){
        let state_name = $('#state').val();
        $.ajax({
            type: 'get',
            url: 'https://www.universal-tutorial.com/api/cities/'+state_name,
            success: function(data){
                $('#city').empty();
                data.forEach(element => {
                    $('#city').append('<option value="'+element.city_name+'">'+element.city_name+'</option>');
                });
            },
            error: function(error){
                console.log(error);
            },
            headers: {
                "Authorization": "Bearer "+ auth_token,
                "Accept": "application/json"
            }
        })
    }