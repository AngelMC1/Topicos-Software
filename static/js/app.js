const API_PRODUCTS = "/api/products/";
const API_CHECKOUT = "/api/v2/checkout/place-order/";

function getCart() {
    return JSON.parse(localStorage.getItem("cart")) || [];
}

function saveCart(cart) {
    localStorage.setItem("cart", JSON.stringify(cart));
}

function formatPrice(value) {
    return new Intl.NumberFormat("es-CO", {
        style: "currency",
        currency: "COP",
        maximumFractionDigits: 0
    }).format(value);
}

async function loadProducts() {
    const container = document.getElementById("products-container");
    if (!container) return;

    container.innerHTML = `<p class="text-muted">Cargando productos...</p>`;

    try {
        const response = await fetch(API_PRODUCTS);
        const products = await response.json();

        if (!products.length) {
            container.innerHTML = `<p class="text-muted">No hay productos disponibles.</p>`;
            return;
        }

        container.innerHTML = products.map(product => `
            <div class="col-md-6 col-lg-4">
                <div class="card product-card">
                    <img src="${product.image_url || 'https://via.placeholder.com/400x300?text=Producto'}" class="card-img-top" alt="${product.name}">
                    <div class="card-body p-4">
                        <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
                            <h5 class="card-title fw-bold mb-0">${product.name}</h5>
                            <span class="product-badge">Importado</span>
                        </div>
                        <p class="card-text text-muted">${product.description || "Producto importado disponible."}</p>
                        <p class="price mb-3">${formatPrice(product.price)}</p>
                        <button class="btn btn-dark w-100" onclick="addToCart(${product.id}, '${String(product.name).replace(/'/g, "\\'")}', ${product.price})">
                            Agregar al carrito
                        </button>
                    </div>
                </div>
            </div>
        `).join("");
    } catch (error) {
        container.innerHTML = `<p class="text-danger">No se pudieron cargar los productos.</p>`;
    }
}

function addToCart(id, name, price) {
    const cart = getCart();
    const existing = cart.find(item => item.product_id === id);

    if (existing) {
        existing.qty += 1;
    } else {
        cart.push({
            product_id: id,
            name,
            price,
            qty: 1
        });
    }

    saveCart(cart);
    alert("Producto agregado al carrito.");
}

function loadCart() {
    const container = document.getElementById("cart-container");
    const totalElement = document.getElementById("cart-total");
    const countElement = document.getElementById("cart-count");
    if (!container || !totalElement) return;

    const cart = getCart();

    if (!cart.length) {
        container.innerHTML = `
            <div class="col-12">
                <div class="empty-cart-box">
                    <div class="empty-cart-icon">🛒</div>
                    <h3 class="fw-bold mb-2">Tu carrito está vacío</h3>
                    <p class="text-muted mb-4">Todavía no has agregado productos. Ve al catálogo y empieza a construir tu pedido.</p>
                    <a href="/catalogo/" class="btn btn-dark premium-btn-main">Explorar catálogo</a>
                </div>
            </div>
        `;
        totalElement.textContent = formatPrice(0);
        if (countElement) countElement.textContent = "0";
        return;
    }

    let total = 0;
    let count = 0;

    container.innerHTML = cart.map((item, index) => {
        const subtotal = item.price * item.qty;
        total += subtotal;
        count += item.qty;

        return `
            <div class="col-12">
                <div class="cart-item-premium">
                    <div class="cart-item-image">
                        <img src="https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80" alt="${item.name}">
                    </div>

                    <div class="cart-item-content">
                        <div class="d-flex justify-content-between align-items-start flex-wrap gap-3">
                            <div>
                                <span class="product-badge mb-2 d-inline-block">Producto seleccionado</span>
                                <h4 class="fw-bold mb-1">${item.name}</h4>
                                <p class="text-muted mb-2">Producto agregado al carrito para tu pedido.</p>
                                <p class="cart-item-price mb-0">${formatPrice(item.price)} c/u</p>
                            </div>

                            <div class="text-lg-end">
                                <p class="text-muted mb-1">Subtotal</p>
                                <h5 class="fw-bold mb-0">${formatPrice(subtotal)}</h5>
                            </div>
                        </div>

                        <div class="cart-actions-row mt-4">
                            <div class="qty-control">
                                <button class="qty-btn" onclick="changeQty(${index}, -1)">−</button>
                                <span class="qty-value">${item.qty}</span>
                                <button class="qty-btn" onclick="changeQty(${index}, 1)">+</button>
                            </div>

                            <button class="btn btn-outline-danger delete-btn" onclick="removeItem(${index})">
                                Eliminar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join("");

    totalElement.textContent = formatPrice(total);
    if (countElement) countElement.textContent = count;
}

function changeQty(index, delta) {
    const cart = getCart();
    if (!cart[index]) return;

    cart[index].qty += delta;

    if (cart[index].qty <= 0) {
        cart.splice(index, 1);
    }

    saveCart(cart);
    loadCart();
    loadCheckoutSummary();
}

function removeItem(index) {
    const cart = getCart();
    cart.splice(index, 1);
    saveCart(cart);
    loadCart();
    loadCheckoutSummary();
}

function loadCheckoutSummary() {
    const summary = document.getElementById("checkout-summary");
    if (!summary) return;

    const cart = getCart();

    if (!cart.length) {
        summary.innerHTML = `<p class="mb-0 text-muted">No hay productos en el carrito.</p>`;
        return;
    }

    let total = 0;

    summary.innerHTML = cart.map(item => {
        const subtotal = item.price * item.qty;
        total += subtotal;
        return `
            <div class="checkout-item p-3 mb-2">
                <div class="d-flex justify-content-between">
                    <span>${item.name} x ${item.qty}</span>
                    <strong>${formatPrice(subtotal)}</strong>
                </div>
            </div>
        `;
    }).join("") + `
        <hr>
        <div class="d-flex justify-content-between">
            <strong>Total estimado</strong>
            <strong>${formatPrice(total)}</strong>
        </div>
    `;
}

function setupCheckoutForm() {
    const form = document.getElementById("checkout-form");
    const alertBox = document.getElementById("checkout-alert");
    if (!form || !alertBox) return;

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const cart = getCart();

        if (!cart.length) {
            alertBox.innerHTML = `<div class="alert alert-warning">El carrito está vacío.</div>`;
            return;
        }

        const payload = {
            customer_email: document.getElementById("customer_email").value,
            items: cart.map(item => ({
                product_id: item.product_id,
                qty: item.qty
            })),
            address: {
                city: document.getElementById("city").value,
                address_line: document.getElementById("address_line").value
            }
        };

        try {
            const response = await fetch(API_CHECKOUT, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok) {
                alertBox.innerHTML = `<div class="alert alert-success">Pedido enviado correctamente.</div>`;
                localStorage.removeItem("cart");
                form.reset();
                loadCheckoutSummary();
            } else {
                alertBox.innerHTML = `<div class="alert alert-danger">${data.detail || "No se pudo enviar el pedido."}</div>`;
            }
        } catch (error) {
            alertBox.innerHTML = `<div class="alert alert-danger">Error de conexión con el servidor.</div>`;
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    loadProducts();
    loadCart();
    loadCheckoutSummary();
    setupCheckoutForm();
});