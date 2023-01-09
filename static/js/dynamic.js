var button = document.getElementsByClassName('updCart')
var button2 = document.getElementsByClassName('checkout')
for(var i=0;i<button.length;i++)
{
    button[i].addEventListener('click',function(){
        var productId = this.dataset.product;
        var productAction = this.dataset.action;
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
    var url = 'upd_quantity'
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
    .then(data=>{        
        document.getElementsByClassName(productId)[0].innerHTML=data.quantity;
        if (data.quantity == 0)
            var d = document.getElementById("div"+productId);
            d.remove();
        console.log(data.quantity);
    });
}

for(var i=0;i<button2.length;i++)
{
    button2[i].addEventListener('click',function(){
        location.href='checkout';
    })
}