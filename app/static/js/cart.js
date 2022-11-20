function addToCart(id, name, price) {
    event.preventDefault()

    fetch('/api/add-cart', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function (res) {
        console.info(res)
        return res.json()
    }).then(function (data) {
        console.info(data)
        let counter = document.getElementById('cart_counter')
        counter.innerText = data.total_quantity
    }).catch(function (err) {
        console.error(err)
    })
}

function pay() {
    if (confirm('Bạn có chắc chắn muốn thanh toán không?') == true) {
        fetch('/api/pay', {
            method: 'post'

        }).then(function (res) {
            return res.json()
        }).then(function (data) {
            if(data.code==200)
                location.reload()
        }).catch(function (err) {
            console.error(err)
        })
    }
}