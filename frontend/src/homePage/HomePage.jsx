// Imports
import { NavLink } from "react-router-dom";
import "./HomePage.css";

// Define and export the HomePage component so App.jsx can use it
export default function HomePage() {
  return (
    <div className="home-page">

      {/* Navbar */}
      <nav className="home-nav">
        <NavLink to="/" className="home-nav-logo">Project-Ate</NavLink>
        <NavLink to="/login" className="btn-primary">Login</NavLink>
      </nav>

      {/* Description */}
      <section className="Website-Description">
        <div className="Web-content">
          <span className="tag-line">Fresh bundles weekly</span>
          <h1>Eat <em>well,</em><br />play better.</h1>
          <p>Discover curated food bundles designed for every lifestyle —
            from family favourites to healthy goals.</p>
          <div className="web-buttons">
            <NavLink to="/user" className="btn-primary">Browse Bundles</NavLink>
            <NavLink to="/login" className="btn-secondary">Login to order</NavLink>
          </div>
        </div>

        {/* Bundle preview cards on the right side */}
        <div className="Description-visual">
          <div className="food-grid">
            {[
              { name: "Kids Favourites", price: "£18.75" },
              { name: "Low Carb",        price: "£20.00" },
              { name: "Vegan Delight",   price: "£22.50" },
              { name: "High Protein",    price: "£25.00" },
            ].map((b) => (
              <div className="food-card" key={b.name}>
                <div className="food-card-name">{b.name}</div>
                <div className="food-card-price">{b.price}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Taglines */}
      <div className="tagline-bar">
        {[
          { text: "Loved by 2,000+ families" },
          { text: "Free delivery over £30"   },
          { text: "Eco-friendly packaging"   },
          { text: "Secure checkout"          },
        ].map((t) => (
          <div className="tagline-item" key={t.text}>
            {t.text}
          </div>
        ))}
      </div>

      {/* Principle cards - explains the key benefits of Project-Ate */}
      <section className="principle-section">
        <p className="section-label">Why Project-Ate?</p>
        <h2 className="section-title">Eating right shouldn't be complicated</h2>

        <div className="principle-grid">
          {[
            { title: "Bundles for every goal",
              desc: "Whether it's low-carb, family-friendly, or high protein — we've curated the perfect bundle for your lifestyle." },
            { title: "Earn rewards as you eat",
              desc: "Use the in-app game to rack up points with every order. Turn healthy habits into real rewards." },
            { title: "Quick & easy ordering",
              desc: "Browse bundles, pick yours, and check out in under a minute. No fuss, no meal planning headaches." },
          ].map((p) => (
            <div className="prop-card" key={p.title}>
              <h3>{p.title}</h3>
              <p>{p.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* I have hardcoded the bundles for now just to c what itll look like so
      that will need to be connected to db or whatever x */}
      <section className="bundles-section">
        <p className="section-label">This week's picks</p>
        <h2 className="section-title">Available Bundles</h2>

        <div className="bundles-grid">
          {[
            { name: "Kids Favourites Bundle", meta: "6 items · Perfect for ages 4–12",   price: "£18.75", tag: "Popular" },
            { name: "Low Carb Bundle",         meta: "8 items · High in protein & fibre", price: "£20.00", tag: "Healthy" },
            { name: "Vegan Delight Bundle",    meta: "7 items · 100% plant-based",        price: "£22.50", tag: null     },
          ].map((b) => (
            <div className="bundle-card" key={b.name}>
              <div className="bundle-body">
                <h3>{b.name}</h3>
                <p className="bundle-meta">{b.meta}</p>
                {b.tag && <span className="bundle-tag">{b.tag}</span>}
                <div className="bundle-footer">
                  <div className="bundle-price">{b.price}</div>
                  <NavLink to="/login" className="btn-add">+ Get</NavLink>
                </div>
              </div>
            </div>
          ))}
        </div>

        <NavLink to="/user" className="view-all">View all bundles</NavLink>
      </section>

    </div>
  );
}
