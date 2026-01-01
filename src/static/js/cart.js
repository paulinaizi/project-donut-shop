document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', handleAddToCart);
    });

    function handleAddToCart(event) {
        const button = event.currentTarget;
        const donutId = button.dataset.donutId;
        const source = button.dataset.source || 'offer';

        let toppings = null;

        if (source === 'creator' && button.dataset.toppings) {
            toppings = JSON.parse(button.dataset.toppings);
        }

        fetch('/cart/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                donut_id: donutId,
                toppings: toppings
            })
        })
        .then(res => res.json())
        .then(data => {
            const badge = document.querySelector('.cart-count');
            if (badge) {
                badge.textContent = data.cart_quantity;
            }
            else {
                const wrapper = document.querySelector('.cart-wrapper'); 
                const span = document.createElement('span'); 
                span.classList.add('cart-count'); 
                span.textContent = data.cart_quantity; 
                wrapper.appendChild(span);                
            }
            // console.log('Dodano do koszyka:', data);
        });

    }

    document.querySelectorAll('.qty-btn.plus').forEach(btn => {
        btn.addEventListener('click', () => {
            const key = btn.dataset.key;
            const qtySpan = btn.parentElement.querySelector('.qty-value');
            const newQty = parseInt(qtySpan.textContent) + 1;

            updateCartQty(key, newQty);
        });
    });

    document.querySelectorAll('.qty-btn.minus').forEach(btn => {
        btn.addEventListener('click', () => {
            const key = btn.dataset.key;
            const qtySpan = btn.parentElement.querySelector('.qty-value');
            const newQty = parseInt(qtySpan.textContent) - 1;

            updateCartQty(key, newQty);
        });
    });

    document.querySelectorAll('.remove-item').forEach(btn => {
        btn.addEventListener('click', () => {
            const key = btn.dataset.key;

            fetch('/cart/delete/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ key: key })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'ok') {
                    location.reload();
                }
            });
        });
    });


    function updateCartQty(key, qty) {
        fetch('/cart/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ key, qty })
        })
            .then(res => res.json())
            .then(() => {
                location.reload();
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

});
