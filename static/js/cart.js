var button = document.getElementsByClassName('updCart')

for(var i=0;i<button.length;i++)
{
    button[i].addEventListener('click',function(){
        var productId = this.dataset.product;
        var productAction = this.dataset.action;
        console.log(productId,productAction,"USER:",user);
        if(user=="AnonymousUser")
        {
            location.href="login";
        }
        else
        {
            updItem(productId,productAction);
        }
    })
}

function updItem(productId,productAction)
{
    var url = 'update_item'
    console.log('Sending data..')
    fetch(
        url,
        {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrfToken
            },
            body:JSON.stringify({'productId':productId,'action':productAction})
        }
    ).then(res=>{return res.json()})
    .then(data=>console.log(data));
}