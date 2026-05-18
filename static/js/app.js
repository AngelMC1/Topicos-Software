const API_PRODUCTS = "/api/products/";
const API_CHECKOUT = "/api/v2/checkout/place-order/";
const API_EXCHANGE_RATE = "/api/exchange-rate/";

let _usdToCop = null;

async function getUsdToCop() {
    if (_usdToCop) return _usdToCop;
    try {
        const res = await fetch(API_EXCHANGE_RATE);
        const data = await res.json();
        _usdToCop = data.rate;
    } catch {
        _usdToCop = 4100;
    }
    return _usdToCop;
}

function formatUSD(valueCOP, rate) {
    return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
        maximumFractionDigits: 2,
    }).format(valueCOP / rate);
}

// Fallback for environments where Django's JavaScriptCatalog is not loaded
if (typeof gettext === "undefined") {
    window.gettext = function (s) { return s; };
}

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

    container.innerHTML = `<p class="text-muted">${gettext("Cargando productos...")}</p>`;

    try {
        const [response, usdRate] = await Promise.all([fetch(API_PRODUCTS), getUsdToCop()]);
        const products = await response.json();

        if (!products.length) {
            container.innerHTML = `<p class="text-muted">${gettext("No hay productos disponibles.")}</p>`;
            return;
        }

        container.innerHTML = products.map(product => `
            <div class="col-md-6 col-lg-4">
                <div class="card product-card">
                    <img src="${product.image_url || 'https://via.placeholder.com/400x300?text=Producto'}" class="card-img-top" alt="${product.name}">
                    <div class="card-body p-4">
                        <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
                            <h5 class="card-title fw-bold mb-0">${product.name}</h5>
                            <span class="product-badge">${gettext("Importado")}</span>
                        </div>
                        <p class="card-text text-muted">${product.description || gettext("Producto importado disponible.")}</p>
                        <p class="price mb-1">${formatPrice(product.price)}</p>
                        <p class="text-muted small mb-3">≈ ${formatUSD(product.price, usdRate)}</p>
                        <button class="btn btn-dark w-100" onclick="addToCart(${product.id}, '${String(product.name).replace(/'/g, "\\'")}', ${product.price}, '${(product.image_url || '').replace(/'/g, "\\'")}')">
                            ${gettext("Agregar al carrito")}
                        </button>
                    </div>
                </div>
            </div>
        `).join("");
    } catch (error) {
        container.innerHTML = `<p class="text-danger">${gettext("No se pudieron cargar los productos.")}</p>`;
    }
}

function addToCart(id, name, price, image_url = "") {
    const cart = getCart();
    const existing = cart.find(item => item.product_id === id);

    if (existing) {
        existing.qty += 1;
    } else {
        cart.push({
            product_id: id,
            name,
            price,
            image_url,
            qty: 1
        });
    }

    saveCart(cart);
    alert(gettext("Producto agregado al carrito."));
}

async function loadCart() {
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
                    <h3 class="fw-bold mb-2">${gettext("Tu carrito está vacío")}</h3>
                    <p class="text-muted mb-4">${gettext("Todavía no has agregado productos. Ve al catálogo y empieza a construir tu pedido.")}</p>
                    <a href="/catalogo/" class="btn btn-dark premium-btn-main">${gettext("Explorar catálogo")}</a>
                </div>
            </div>
        `;
        totalElement.textContent = formatPrice(0);
        if (countElement) countElement.textContent = "0";
        return;
    }

    const usdRate = await getUsdToCop();
    let total = 0;
    let count = 0;

    container.innerHTML = cart.map((item, index) => {
        const subtotal = item.price * item.qty;
        total += subtotal;
        count += item.qty;
        const imgSrc = item.image_url || "https://via.placeholder.com/400x300?text=Producto";

        return `
            <div class="col-12">
                <div class="cart-item-premium">
                    <div class="cart-item-image">
                        <img src="${imgSrc}" alt="${item.name}">
                    </div>

                    <div class="cart-item-content">
                        <div class="d-flex justify-content-between align-items-start flex-wrap gap-3">
                            <div>
                                <span class="product-badge mb-2 d-inline-block">${gettext("Producto seleccionado")}</span>
                                <h4 class="fw-bold mb-1">${item.name}</h4>
                                <p class="cart-item-price mb-0">${formatPrice(item.price)} ${gettext("c/u")} <span class="text-muted small">≈ ${formatUSD(item.price, usdRate)}</span></p>
                            </div>

                            <div class="text-lg-end">
                                <p class="text-muted mb-1">${gettext("Subtotal")}</p>
                                <h5 class="fw-bold mb-0">${formatPrice(subtotal)}</h5>
                                <p class="text-muted small mb-0">≈ ${formatUSD(subtotal, usdRate)}</p>
                            </div>
                        </div>

                        <div class="cart-actions-row mt-4">
                            <div class="qty-control">
                                <button class="qty-btn" onclick="changeQty(${index}, -1)">−</button>
                                <span class="qty-value">${item.qty}</span>
                                <button class="qty-btn" onclick="changeQty(${index}, 1)">+</button>
                            </div>

                            <button class="btn btn-outline-danger delete-btn" onclick="removeItem(${index})">
                                ${gettext("Eliminar")}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join("");

    totalElement.textContent = formatPrice(total);
    if (countElement) countElement.textContent = count;
    const usdTotalEl = document.getElementById("cart-total-usd");
    if (usdTotalEl) usdTotalEl.textContent = `≈ ${formatUSD(total, usdRate)}`;
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

async function loadCheckoutSummary() {
    const summary = document.getElementById("checkout-summary");
    if (!summary) return;

    const cart = getCart();

    if (!cart.length) {
        summary.innerHTML = `<p class="mb-0 text-muted">${gettext("No hay productos en el carrito.")}</p>`;
        return;
    }

    const usdRate = await getUsdToCop();
    let total = 0;

    summary.innerHTML = cart.map(item => {
        const subtotal = item.price * item.qty;
        total += subtotal;
        return `
            <div class="checkout-item p-3 mb-2">
                <div class="d-flex justify-content-between align-items-start">
                    <span>${item.name} x ${item.qty}</span>
                    <div class="text-end">
                        <strong class="d-block">${formatPrice(subtotal)}</strong>
                        <small class="text-muted">≈ ${formatUSD(subtotal, usdRate)}</small>
                    </div>
                </div>
            </div>
        `;
    }).join("") + `
        <hr>
        <div class="d-flex justify-content-between align-items-start">
            <strong>${gettext("Total estimado")}</strong>
            <div class="text-end">
                <strong class="d-block">${formatPrice(total)}</strong>
                <small class="text-muted">≈ ${formatUSD(total, usdRate)}</small>
            </div>
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
            alertBox.innerHTML = `<div class="alert alert-warning">${gettext("El carrito está vacío.")}</div>`;
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
                alertBox.innerHTML = `<div class="alert alert-success">${gettext("Pedido enviado correctamente.")}</div>`;
                localStorage.removeItem("cart");
                form.reset();
                loadCheckoutSummary();
            } else {
                alertBox.innerHTML = `<div class="alert alert-danger">${data.detail || gettext("No se pudo enviar el pedido.")}</div>`;
            }
        } catch (error) {
            alertBox.innerHTML = `<div class="alert alert-danger">${gettext("Error de conexión con el servidor.")}</div>`;
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    loadProducts();
    loadCart();
    loadCheckoutSummary();
    setupCheckoutForm();
});
