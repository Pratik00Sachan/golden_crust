// --- Constants ---
const LOCAL_STORAGE_CART_KEY = 'goldenCrustCart';

// --- Cart Management ---

// Helper function to get cart from local storage
function getCart() {
    const cart = localStorage.getItem(LOCAL_STORAGE_CART_KEY);
    return cart ? JSON.parse(cart) : [];
}

// Helper function to save cart to local storage
function saveCart(cart) {
    localStorage.setItem(LOCAL_STORAGE_CART_KEY, JSON.stringify(cart));
    updateCartIconCount();
}

// Add to cart function
function addToCart(productId, productName, productPrice, productImage) {
    let cart = getCart();
    const existingProductIndex = cart.findIndex(item => item.id === productId);

    if (existingProductIndex > -1) {
        cart[existingProductIndex].quantity += 1;
    } else {
        cart.push({
            id: productId,
            name: productName,
            price: parseFloat(productPrice),
            imageSrc: productImage,
            quantity: 1
        });
    }
    saveCart(cart);
    // alert(`${productName} has been added to your cart!`); // Original alert
    showNotification(`${productName} added to cart!`);
}

// Update cart icon count in header
function updateCartIconCount() {
    const cart = getCart();
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    
    const countNavElement = document.getElementById('cart-item-count-nav');
    const countIconElement = document.getElementById('cart-item-count-icon');

    if (countNavElement) {
        countNavElement.textContent = `(${totalItems})`;
    }
    if (countIconElement) {
        countIconElement.textContent = `(${totalItems})`;
    }
}

// Display cart contents on cart.html
function displayCart() {
    const cart = getCart();
    const cartContentDiv = document.getElementById('cart-content');
    const cartTableContainer = document.getElementById('cart-table-container');
    const cartSummaryContainer = document.getElementById('cart-summary-container');
    const cartItemsList = document.getElementById('cart-items-list');
    
    if (!cartItemsList || !cartContentDiv || !cartTableContainer || !cartSummaryContainer) {
        // Not on cart page or elements missing
        return;
    }

    cartItemsList.innerHTML = ''; // Clear previous items

    if (cart.length === 0) {
        cartContentDiv.innerHTML = `
            <div class="empty-cart-message">
                <p>Your cart is currently empty.</p>
                <a href="${document.body.dataset.productsUrl || './products.html'}">Start Shopping!</a>
            </div>`; // Use dataset for URL if available
        cartTableContainer.style.display = 'none';
        cartSummaryContainer.style.display = 'none';
    } else {
        cartContentDiv.innerHTML = ''; // Clear empty cart message
        cartTableContainer.style.display = ''; // Show table
        cartSummaryContainer.style.display = ''; // Show summary

        cart.forEach(item => {
            const itemRow = document.createElement('tr');
            itemRow.innerHTML = `
                <td>
                    <div class="cart-item-details">
                        <img src="${item.imageSrc}" alt="${item.name}" class="cart-item-img">
                        <span class="cart-item-title">${item.name}</span>
                    </div>
                </td>
                <td>$${item.price.toFixed(2)}</td>
                <td class="cart-item-quantity">
                    <button onclick="updateQuantity('${item.id}', -1, this)">-</button>
                    <input type="number" value="${item.quantity}" min="1" onchange="handleQuantityInputChange('${item.id}', this.value)">
                    <button onclick="updateQuantity('${item.id}', 1, this)">+</button>
                </td>
                <td>$${(item.price * item.quantity).toFixed(2)}</td>
                <td><button class="remove-item-btn" onclick="removeFromCart('${item.id}')">Remove</button></td>
            `;
            cartItemsList.appendChild(itemRow);
        });
    }
    calculateTotals();
    updateCartIconCount();
}

// Handle direct input change for quantity
function handleQuantityInputChange(productId, newQuantity) {
    const quantity = parseInt(newQuantity);
    if (isNaN(quantity) || quantity < 1) {
        // If invalid, revert to 1 or remove? For now, let's refresh to previous state or set to 1.
        // This part might need more sophisticated handling or rely on +/- buttons primarily.
        // For simplicity, we'll just update with the potentially invalid value and let updateQuantity handle it.
        updateQuantity(productId, 0, null, quantity); // Special handling for direct input
    } else {
        updateQuantity(productId, 0, null, quantity); // Special handling for direct input
    }
}


// Update quantity of an item in the cart
function updateQuantity(productId, change, buttonElement, directValue) {
    let cart = getCart();
    const itemIndex = cart.findIndex(item => item.id === productId);

    if (itemIndex > -1) {
        if (directValue !== undefined) { // From direct input
            cart[itemIndex].quantity = parseInt(directValue);
        } else { // From +/- buttons
            cart[itemIndex].quantity += change;
        }

        if (cart[itemIndex].quantity < 1) {
            cart[itemIndex].quantity = 1; // Prevent quantity from going below 1
            // Or, optionally, remove the item: cart.splice(itemIndex, 1);
        }
        saveCart(cart);
        displayCart(); // Refresh cart display
    }
}

// Remove item from cart
function removeFromCart(productId) {
    let cart = getCart();
    cart = cart.filter(item => item.id !== productId);
    saveCart(cart);
    displayCart(); // Refresh cart display
}

// Calculate totals for the cart
function calculateTotals() {
    const cart = getCart();
    const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    
    // Conceptual discount: 10%
    const discountPercentage = 0.10; 
    const discountAmount = subtotal * discountPercentage;
    
    const shippingCost = 5.00; // Fixed shipping for now
    
    const total = subtotal - discountAmount + shippingCost;

    const subtotalEl = document.getElementById('cart-subtotal');
    const discountEl = document.getElementById('cart-discount');
    const shippingEl = document.getElementById('cart-shipping');
    const totalEl = document.getElementById('cart-total');

    if (subtotalEl) subtotalEl.textContent = `$${subtotal.toFixed(2)}`;
    if (discountEl) discountEl.textContent = `-$${discountAmount.toFixed(2)}`;
    if (shippingEl) shippingEl.textContent = `$${shippingCost.toFixed(2)}`;
    if (totalEl) totalEl.textContent = `$${total.toFixed(2)}`;
}


// --- General UI ---

// Simple notification function
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'cart-notification';
    notification.textContent = message;
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Modal functionality (existing)
function openModal() {
    const modal = document.getElementById('deliveryModal');
    if (modal) modal.style.display = 'flex';
}

function closeModal() {
    const modal = document.getElementById('deliveryModal');
    if (modal) modal.style.display = 'none';
}

// Close modal when clicking outside (existing)
window.addEventListener('click', function(event) {
    const modal = document.getElementById('deliveryModal');
    if (modal && event.target == modal) {
        closeModal();
    }
});


// Profile page tab functionality (existing)
function switchTab(event, tabName) {
    const tabcontent = document.querySelectorAll(".tab-content");
    tabcontent.forEach(tc => tc.style.display = "none");

    const tablinks = document.querySelectorAll(".tab");
    tablinks.forEach(tl => tl.classList.remove("active"));

    const activeTabContent = document.getElementById(tabName);
    if (activeTabContent) activeTabContent.style.display = "block";
    if (event.currentTarget) event.currentTarget.classList.add("active");
}

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    // Update cart icon count on all pages
    updateCartIconCount();

    // If on cart page, display the cart
    if (document.getElementById('cart-items-list')) {
        // Pass the products URL to the script for the "Start Shopping" link
        const productsLink = document.querySelector('a[href*="products"]'); // more robust selector
        if (productsLink) {
             document.body.dataset.productsUrl = productsLink.href;
        }
        displayCart();
    }

    // Add to cart button event listeners (modified from original)
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productCard = this.closest('.product-card');
            if (productCard) {
                const id = this.dataset.id || productCard.querySelector('.product-title').textContent.replace(/\s+/g, '-').toLowerCase(); // Fallback ID
                const name = this.dataset.name || productCard.querySelector('.product-title').textContent;
                const price = this.dataset.price || productCard.querySelector('.current-price').textContent.replace('$', '');
                const image = this.dataset.image || productCard.querySelector('.product-img').src;
                
                addToCart(id, name, price, image);
            }
        });
    });
    
    // Initialize profile tabs if they exist
    const initialTab = document.querySelector('.profile-tabs .tab');
    if (initialTab && document.getElementById('orders')) { 
        initialTab.click(); 
    }
});
