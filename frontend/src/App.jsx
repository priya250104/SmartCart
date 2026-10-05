import { NavLink, Route, Routes } from 'react-router-dom';
import { useMemo, useState } from 'react';

const defaultProducts = [
  {
    id: 1,
    name: 'Smart Speaker Pro',
    price: 129.99,
    description: 'Premium voice assistant with room-filling sound.',
    image: 'https://images.unsplash.com/photo-1546435770-a3e426bf472b',
  },
  {
    id: 2,
    name: 'Minimal Desk Lamp',
    price: 49.99,
    description: 'Warm ambient lighting for focused work.',
    image: 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85',
  },
  {
    id: 3,
    name: 'Classic Leather Backpack',
    price: 89.99,
    description: 'Made for daily carry and all-day comfort.',
    image: 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518',
  },
];

function Layout({ cart, products, addToCart, removeFromCart, clearCart }) {
  const total = useMemo(
    () => cart.reduce((sum, item) => sum + item.quantity * item.price, 0),
    [cart]
  );

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand-wrap">
          <span className="brand-mark">S</span>
          <h1>SmartCart</h1>
        </div>

        <nav className="nav">
          <NavLink className="nav-link" to="/">Home</NavLink>
          <NavLink className="nav-link" to="/products">Products</NavLink>
          <NavLink className="nav-link" to="/cart">Cart</NavLink>
          <NavLink className="nav-link" to="/login">Login</NavLink>
          <NavLink className="nav-link" to="/checkout">Checkout</NavLink>
        </nav>

        <div className="cart-pill">Cart: {cart.length} · ${total.toFixed(2)}</div>
      </header>

      <main className="page-container">
        <Routes>
          <Route path="/" element={<HomePage products={products} addToCart={addToCart} />} />
          <Route path="/products" element={<ProductsPage products={products} addToCart={addToCart} />} />
          <Route path="/cart" element={<CartPage cart={cart} removeFromCart={removeFromCart} clearCart={clearCart} />} />
          <Route path="/login" element={<AuthPage mode="login" />} />
          <Route path="/register" element={<AuthPage mode="register" />} />
          <Route path="/checkout" element={<CheckoutPage cart={cart} clearCart={clearCart} />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </main>
    </div>
  );
}

function HomePage({ products, addToCart }) {
  return (
    <div>
      <section className="hero">
        <div>
          <p className="eyebrow">Curated everyday essentials</p>
          <h2>Smart shopping for modern living.</h2>
          <p>
            Discover premium electronics, home finds, and personal accessories designed to simplify life.
          </p>
          <div className="hero-actions">
            <NavLink to="/products" className="primary-btn">Shop now</NavLink>
            <NavLink to="/register" className="secondary-btn">Create account</NavLink>
          </div>
        </div>
      </section>

      <section className="product-grid">
        {products.map((product) => (
          <article key={product.id} className="product-card">
            <img src={product.image} alt={product.name} />
            <div className="product-body">
              <h3>{product.name}</h3>
              <p>{product.description}</p>
              <div className="product-footer">
                <strong>${product.price.toFixed(2)}</strong>
                <button onClick={() => addToCart(product)}>Add to cart</button>
              </div>
            </div>
          </article>
        ))}
      </section>
    </div>
  );
}

function ProductsPage({ products, addToCart }) {
  return (
    <div>
      <h2 className="section-title">All products</h2>
      <div className="product-grid">
        {products.map((product) => (
          <article key={product.id} className="product-card">
            <img src={product.image} alt={product.name} />
            <div className="product-body">
              <h3>{product.name}</h3>
              <p>{product.description}</p>
              <div className="product-footer">
                <strong>${product.price.toFixed(2)}</strong>
                <button onClick={() => addToCart(product)}>Add</button>
              </div>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}

function CartPage({ cart, removeFromCart, clearCart }) {
  const total = cart.reduce((sum, item) => sum + item.quantity * item.price, 0);

  if (cart.length === 0) {
    return (
      <div className="empty-state">
        <h2>Your cart is empty</h2>
        <NavLink to="/products" className="primary-btn">Browse products</NavLink>
      </div>
    );
  }

  return (
    <div>
      <h2 className="section-title">Your cart</h2>
      <div className="cart-list">
        {cart.map((item) => (
          <div key={item.id} className="cart-item">
            <div>
              <strong>{item.name}</strong>
              <p>
                {item.quantity} × ${item.price.toFixed(2)}
              </p>
            </div>
            <button onClick={() => removeFromCart(item.id)}>Remove</button>
          </div>
        ))}
      </div>
      <div className="cart-summary">
        <strong>Total: ${total.toFixed(2)}</strong>
        <div className="summary-actions">
          <button className="secondary-btn" onClick={clearCart}>Clear</button>
          <NavLink to="/checkout" className="primary-btn">Checkout</NavLink>
        </div>
      </div>
    </div>
  );
}

function AuthPage({ mode }) {
  return (
    <div className="auth-card">
      <h2>{mode === 'login' ? 'Welcome back' : 'Create your account'}</h2>
      <form className="auth-form">
        {mode === 'register' && <input type="text" placeholder="Full name" />}
        <input type="email" placeholder="Email" />
        <input type="password" placeholder="Password" />
        <button type="button" className="primary-btn">
          {mode === 'login' ? 'Login' : 'Register'}
        </button>
      </form>
    </div>
  );
}

function CheckoutPage({ cart, clearCart }) {
  const total = cart.reduce((sum, item) => sum + item.quantity * item.price, 0);

  return (
    <div className="checkout-card">
      <h2 className="section-title">Checkout</h2>
      <div className="checkout-summary">
        <p>Items: {cart.reduce((sum, item) => sum + item.quantity, 0)}</p>
        <p>Subtotal: ${total.toFixed(2)}</p>
        <p>Shipping: $0.00</p>
        <h3>Total: ${total.toFixed(2)}</h3>
      </div>
      <button
        className="primary-btn"
        onClick={() => {
          clearCart();
          window.alert('Order placed successfully!');
        }}
      >
        Place order
      </button>
    </div>
  );
}

function NotFoundPage() {
  return (
    <div className="empty-state">
      <h2>Page not found</h2>
      <NavLink to="/" className="primary-btn">Back home</NavLink>
    </div>
  );
}

export default function App() {
  const [products] = useState(defaultProducts);
  const [cart, setCart] = useState([]);

  const addToCart = (product) => {
    setCart((currentCart) => {
      const item = currentCart.find((entry) => entry.id === product.id);
      if (item) {
        return currentCart.map((entry) =>
          entry.id === product.id ? { ...entry, quantity: entry.quantity + 1 } : entry
        );
      }
      return [...currentCart, { ...product, quantity: 1 }];
    });
  };

  const removeFromCart = (productId) => {
    setCart((currentCart) => currentCart.filter((item) => item.id !== productId));
  };

  const clearCart = () => setCart([]);

  return <Layout cart={cart} products={products} addToCart={addToCart} removeFromCart={removeFromCart} clearCart={clearCart} />;
}