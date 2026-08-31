#!/usr/bin/env python3
"""Generates products.html, product/<slug>.html, sitemap.xml and index.html's
featured grid from data/products.json — the single source of truth for product
data. Re-run this after editing products.json."""
import json
import os
import re
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")
DOMAIN = "https://www.invisionhealthcare.co.in"

with open(os.path.join(ROOT, "data", "products.json")) as f:
    PRODUCTS = json.load(f)

os.makedirs(os.path.join(PUBLIC, "product"), exist_ok=True)

CATEGORY_ORDER = [
    "Diabetes Care",
    "Neuro & Vitamin Care",
    "Gastro Care",
    "Bone & Joint Care",
    "Eye Care",
    "Respiratory Care",
]

ICON_SEARCH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'
ICON_SHIELD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v6c0 5-3.5 8-7 9-3.5-1-7-4-7-9V6l7-3z"/><path d="M9 12l2 2 4-4"/></svg>'
ICON_FLASK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 2v6L4 19a1 1 0 0 0 1 2h14a1 1 0 0 0 1-2L15 8V2"/><path d="M9 2h6"/><path d="M7.5 14h9"/></svg>'
ICON_LEAF = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 4C10 4 4 10 4 20c10 0 16-6 16-16z"/><path d="M4 20l7-7"/></svg>'
ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.1-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.3 1.8.6 2.7a2 2 0 0 1-.4 2.1L8 9.9a16 16 0 0 0 6 6l1.4-1.4a2 2 0 0 1 2.1-.4c.9.3 1.8.5 2.7.6a2 2 0 0 1 1.8 2.2z"/></svg>'
ICON_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg>'
ICON_PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>'
ICON_CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>'
ICON_IMAGE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="1.5"/><path d="m21 15-5-5L5 21"/></svg>'

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))

def haystack(p):
    parts = [p["name"], p["composition"], p["category"], "Invision Healthcare", p["slug"]] + p.get("keywords", [])
    return esc(" ".join(parts).lower())

def badge(p):
    return ('<span class="badge badge-rx">Prescription</span>' if p["rx"]
            else '<span class="badge badge-otc">OTC</span>')

def header(prefix, active):
    def link(href, label, key):
        cls = ' class="active"' if key == active else ""
        return f'<a href="{prefix}{href}"{cls}>{label}</a>'
    return f'''<header class="site-header">
  <div class="wrap">
    <a href="{prefix}index.html" class="brand">
      <img src="{prefix}assets/img/logo.png" alt="Invision Healthcare logo" width="42" height="42">
      <span class="brand-text"><strong>Invision Healthcare</strong><span>WHO-GMP Certified Pharma</span></span>
    </a>
    <button class="nav-toggle" id="navToggle" aria-label="Toggle menu" aria-expanded="false">&#9776;</button>
    <nav class="main-nav" id="mainNav">
      {link("index.html", "Home", "home")}
      {link("products.html", "Products", "products")}
      {link("about.html", "About", "about")}
      {link("contact.html", "Contact", "contact")}
    </nav>
    <div class="header-search">
      <form action="{prefix}products.html" method="get">
        {ICON_SEARCH}
        <input type="search" name="q" placeholder="Search medicine, salt or Invision Healthcare..." aria-label="Search products">
      </form>
    </div>
  </div>
</header>
'''

def footer(prefix):
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div>
      <div class="brand-text"><strong>Invision Healthcare</strong></div>
      <p>WHO-GMP certified pharmaceutical company manufacturing quality medicines across diabetes, neuro care, gastro, bone &amp; joint and eye care categories.</p>
    </div>
    <div>
      <h4>Company</h4>
      <a href="{prefix}about.html">About Us</a>
      <a href="{prefix}products.html">Our Products</a>
      <a href="{prefix}contact.html">Contact</a>
    </div>
    <div>
      <h4>Categories</h4>
      {''.join(f'<a href="{prefix}products.html?category={quote(c)}">{esc(c)}</a>' for c in CATEGORY_ORDER)}
    </div>
    <div>
      <h4>Get in touch</h4>
      <a href="tel:+919560093447">+91-9560093447</a>
      <a href="mailto:invisionhealthcare@gmail.com">invisionhealthcare@gmail.com</a>
      <a href="{prefix}contact.html">Dwarka, New Delhi</a>
    </div>
  </div>
  <div class="footer-bottom">&copy; 2025 Invision Healthcare. All Rights Reserved. WHO-GMP &amp; ISO 9001:2015 Certified.</div>
</footer>
<script src="{prefix}assets/js/main.js"></script>
'''

def page(title, description, canonical_path, prefix, active, body, extra_head=""):
    canonical = f"{DOMAIN}/{canonical_path}" if canonical_path else DOMAIN + "/"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/x-icon" href="{prefix}favicon.ico">
<meta name="robots" content="index, follow">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/assets/img/logo.png">
<link href="https://fonts.googleapis.com/css?family=Inter:400,600,700&display=swap" rel="stylesheet">
<link href="{prefix}assets/css/style.css" rel="stylesheet">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-L7TDWK9TQP"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-L7TDWK9TQP');</script>
{extra_head}</head>
<body>
{header(prefix, active)}
{body}
{footer(prefix)}
</body>
</html>
'''

# ---------------- Product card partial ----------------
def product_card(p, prefix):
    img = f"{prefix}assets/img/products/{p['slug']}/1"
    if p.get("hasImage", True):
        thumb_inner = f'''<picture>
      <source srcset="{img}.webp" type="image/webp">
      <img src="{img}.jpg" alt="{esc(p['name'])} - {esc(p['composition'])} box" width="480" height="360" loading="lazy">
    </picture>'''
    else:
        thumb_inner = f'<div class="thumb-placeholder">{ICON_IMAGE}<span>Image coming soon</span></div>'
    return f'''<article class="product-card" data-category="{esc(p['category'])}" data-search="{haystack(p)}">
  <a class="thumb" href="{prefix}product/{p['slug']}.html">
    {thumb_inner}
  </a>
  <div class="body">
    <span class="cat">{esc(p['category'])}</span>
    <h3><a href="{prefix}product/{p['slug']}.html">{esc(p['name'])}</a></h3>
    <p class="composition">{esc(p['composition'])}</p>
    <div class="meta-row">
      {badge(p)}
      <a class="view-link" href="{prefix}product/{p['slug']}.html">View details &rarr;</a>
    </div>
  </div>
</article>'''

# ---------------- product/<slug>.html ----------------
def build_product_page(p):
    prefix = "../"
    others = [x for x in PRODUCTS if x["slug"] != p["slug"] and x["category"] == p["category"]][:3]
    if len(others) < 3:
        others += [x for x in PRODUCTS if x["slug"] != p["slug"] and x not in others][: 3 - len(others)]
    img_base = f"{prefix}assets/img/products/{p['slug']}"
    has_image = p.get("hasImage", True)
    schema = {
        "@context": "https://schema.org",
        "@type": "Drug",
        "name": p["name"],
        "activeIngredient": p["composition"],
        "description": p["uses"],
        "manufacturer": {"@type": "Organization", "name": "Invision Healthcare"},
        "url": f"{DOMAIN}/product/{p['slug']}.html",
    }
    if has_image:
        schema["image"] = f"{DOMAIN}/assets/img/products/{p['slug']}/1.jpg"
    extra_head = f'<script type="application/ld+json">{json.dumps(schema)}</script>\n'
    if has_image:
        thumbs = "\n".join(
            f'<button type="button" data-full="{img_base}/{i}.jpg" class="{"active" if i == 1 else ""}">'
            f'<img src="{img_base}/{i}.jpg" alt="{esc(p["name"])} view {i}" width="64" height="64"></button>'
            for i in (1, 2)
        )
        gallery_html = f'''<div class="gallery-main" id="galleryMain">
          <picture>
            <source id="galleryWebp" srcset="{img_base}/1.webp" type="image/webp">
            <img id="galleryImg" src="{img_base}/1.jpg" alt="{esc(p['name'])} - {esc(p['composition'])}" width="500" height="500">
          </picture>
        </div>
        <div class="gallery-thumbs">{thumbs}</div>'''
    else:
        gallery_html = f'''<div class="gallery-main gallery-placeholder">
          {ICON_IMAGE}
          <p>Product image coming soon</p>
        </div>'''
    body = f'''<main>
  <div class="wrap section">
    <div class="product-detail">
      <div>
        {gallery_html}
      </div>
      <div>
        <span class="pd-category">{esc(p['category'])}</span>
        <h1 class="pd-name">{esc(p['name'])}</h1>
        <p class="pd-composition">{esc(p['composition'])}</p>
        <div class="pd-facts">
          <div class="pd-fact"><strong>Pack Size</strong>{esc(p['packSize'])}</div>
          <div class="pd-fact"><strong>Status</strong>{"Prescription Required" if p['rx'] else "OTC"}</div>
          <div class="pd-fact"><strong>Manufactured By</strong>Invision Healthcare</div>
        </div>
        <p>{esc(p['shortDescription'])}</p>
        <div class="pd-section">
          <h2>Uses</h2>
          <p>{esc(p['uses'])}</p>
        </div>
        <div class="pd-disclaimer">This information is for reference only and does not replace professional medical advice. Please consult a registered medical practitioner or pharmacist before use, especially for prescription products.</div>
        <div class="hero-cta" style="margin-top:24px;">
          <a class="btn btn-primary" href="{prefix}contact.html">Enquire About This Product</a>
          <a class="btn btn-outline" style="border-color:var(--color-line);color:var(--color-primary);" href="{prefix}products.html">&larr; Back to All Products</a>
        </div>
      </div>
    </div>

    <h2 class="related-heading">Related Products</h2>
    <div class="product-grid">
      {''.join(product_card(o, prefix) for o in others)}
    </div>
  </div>
</main>
<script>
document.querySelectorAll('.gallery-thumbs button').forEach(function(btn){{
  btn.addEventListener('click', function(){{
    document.getElementById('galleryImg').src = btn.dataset.full;
    document.getElementById('galleryWebp').srcset = btn.dataset.full.replace('.jpg', '.webp');
    document.querySelectorAll('.gallery-thumbs button').forEach(function(b){{ b.classList.remove('active'); }});
    btn.classList.add('active');
  }});
}});
</script>
'''
    title = f"{p['name']} - {p['composition']} | Invision Healthcare"
    desc = f"{p['name']} ({p['composition']}) by Invision Healthcare. {p['shortDescription']} Pack: {p['packSize']}."
    html = page(title, desc, f"product/{p['slug']}.html", prefix, "products", body, extra_head)
    with open(os.path.join(PUBLIC, "product", f"{p['slug']}.html"), "w") as f:
        f.write(html)

for p in PRODUCTS:
    build_product_page(p)

# ---------------- products.html ----------------
def build_products_page():
    prefix = ""
    chips = "".join(
        f'<button type="button" class="chip{" active" if c == "All" else ""}" data-category="{esc(c)}">{esc(c)}</button>'
        for c in ["All"] + CATEGORY_ORDER
    )
    cards = "\n".join(product_card(p, prefix) for p in PRODUCTS)
    body = f'''<main>
  <div class="wrap section">
    <div class="section-head">
      <div>
        <h1>All Products</h1>
        <p>{len(PRODUCTS)} WHO-GMP certified medicines from Invision Healthcare. Search by brand name, salt/composition, or company.</p>
      </div>
    </div>
    <div class="search-bar">
      {ICON_SEARCH}
      <input type="search" id="productSearch" placeholder="Search e.g. Sayomax, Voglibose, diabetes, Invision Healthcare...">
    </div>
    <div class="chip-row" id="categoryChips">{chips}</div>
    <p class="result-count" id="resultCount"></p>
    <div class="product-grid" id="productGrid">
      {cards}
    </div>
    <p class="no-results" id="noResults">No medicines matched your search. Try a different name, salt, or category.</p>
  </div>
</main>
<script src="{prefix}assets/js/search.js"></script>
'''
    html = page(
        "All Medicines | Invision Healthcare | WHO-GMP Certified Pharmaceuticals",
        "Browse and search the complete range of WHO-GMP certified medicines from Invision Healthcare by brand name, salt composition, or category.",
        "products.html", prefix, "products", body,
    )
    with open(os.path.join(PUBLIC, "products.html"), "w") as f:
        f.write(html)

build_products_page()

# ---------------- sitemap.xml ----------------
def build_sitemap():
    urls = ["", "about.html", "products.html", "contact.html"] + [f"product/{p['slug']}.html" for p in PRODUCTS]
    items = "\n".join(
        f"  <url><loc>{DOMAIN}/{u}</loc><priority>{'1.00' if u=='' else '0.80' if 'product/' not in u else '0.64'}</priority></url>"
        for u in urls
    )
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{items}
</urlset>
'''
    with open(os.path.join(PUBLIC, "sitemap.xml"), "w") as f:
        f.write(xml)

build_sitemap()

def build_robots():
    with open(os.path.join(PUBLIC, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")

build_robots()

# ---------------- index.html ----------------
def build_home():
    prefix = ""
    featured = PRODUCTS[:8]
    cards = "\n".join(product_card(p, prefix) for p in featured)
    hero_imgs = "\n".join(
        f'<img src="assets/img/products/{p["slug"]}/1.jpg" alt="{esc(p["name"])} box" width="200" height="200" loading="lazy">'
        for p in PRODUCTS[:4]
    )
    cat_chip_links = "".join(
        f'<a class="chip" href="products.html?category={quote(c)}">{esc(c)}</a>' for c in CATEGORY_ORDER
    )
    body = f'''<main>
  <section class="hero">
    <div class="wrap">
      <div>
        <span class="badge">WHO-GMP &amp; ISO 9001:2015 Certified</span>
        <h1>Quality medicines you can search, verify and trust.</h1>
        <p class="lead">Invision Healthcare manufactures and markets pharmaceutical products across diabetes, neuro care, gastro, bone &amp; joint and eye care &mdash; every product backed by real, verified composition data.</p>
        <div class="hero-cta">
          <a class="btn btn-light" href="products.html">Browse All Products</a>
          <a class="btn btn-outline" href="contact.html">Contact Us</a>
        </div>
        <div class="hero-stats">
          <div><strong>{len(PRODUCTS)}+</strong><span>Products</span></div>
          <div><strong>6</strong><span>Therapeutic Categories</span></div>
          <div><strong>WHO-GMP</strong><span>Certified Manufacturing</span></div>
        </div>
      </div>
      <div class="hero-visual">{hero_imgs}</div>
    </div>
  </section>

  <section class="trust-strip">
    <div class="wrap">
      <div class="trust-item">{ICON_SHIELD}WHO-GMP Certified</div>
      <div class="trust-item">{ICON_FLASK}ISO 9001:2015 Certified</div>
      <div class="trust-item">{ICON_LEAF}Manufactured in Roorkee, Uttarakhand</div>
      <div class="trust-item">{ICON_PIN}Headquartered in New Delhi</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head">
        <div>
          <h2>Our Products</h2>
          <p>A quick look at our range &mdash; search the full catalog by medicine name, salt, or company.</p>
        </div>
        <a class="btn btn-primary" href="products.html">View All {len(PRODUCTS)} Products</a>
      </div>
      <div class="chip-row">{cat_chip_links}</div>
      <div class="product-grid">
        {cards}
      </div>
    </div>
  </section>

  <section class="section section-alt">
    <div class="wrap content-grid">
      <div>
        <h2>About Invision Healthcare</h2>
        <p>Invision Healthcare is a WHO-GMP certified pharmaceutical company headquartered in New Delhi, manufacturing and marketing medicines across neuropathic pain, diabetes, gastro, bone &amp; joint, eye care and respiratory categories, in partnership with WHO-GMP &amp; ISO 9001:2015 certified manufacturing units.</p>
        <a class="btn btn-primary" href="about.html">Learn More About Us</a>
        <div class="info-cards">
          <div class="info-card">{ICON_SHIELD}<h3>Certified Quality</h3><p>Every product is manufactured under WHO-GMP and ISO 9001:2015 certified facilities.</p></div>
          <div class="info-card">{ICON_FLASK}<h3>Verified Composition</h3><p>Product data on this site is verified directly against real packaging, not placeholder text.</p></div>
          <div class="info-card">{ICON_LEAF}<h3>Wide Therapeutic Range</h3><p>From diabetes and neuro care to eye drops &mdash; a diverse, growing product portfolio.</p></div>
        </div>
      </div>
      <div class="hero-visual" style="background:#fff;border-color:var(--color-line);">
        {"".join(f'<img src="assets/img/products/{p["slug"]}/2.jpg" alt="{esc(p["name"])}" width="200" height="200" loading="lazy">' for p in PRODUCTS[8:12])}
      </div>
    </div>
  </section>
</main>
'''
    html = page(
        "Invision Healthcare | WHO-GMP Certified Pharmaceutical Company | Search Our Medicines",
        "Invision Healthcare is a WHO-GMP & ISO 9001:2015 certified pharmaceutical company. Browse and search our full range of diabetes, neuro care, gastro, bone & joint and eye care medicines.",
        "", prefix, "home", body,
    )
    with open(os.path.join(PUBLIC, "index.html"), "w") as f:
        f.write(html)

build_home()

# ---------------- about.html ----------------
def build_about():
    prefix = ""
    body = f'''<main>
  <section class="section">
    <div class="wrap content-grid">
      <div>
        <span class="badge" style="background:var(--color-bg);color:var(--color-primary);">About Us</span>
        <h1>Invision Healthcare</h1>
        <p>Invision Healthcare (IHC) is a WHO-GMP certified pharmaceutical company headquartered in New Delhi. We market medicines across neuropathic pain, diabetes care, gastro health, bone &amp; joint care, eye care and respiratory categories, manufactured in partnership with WHO-GMP &amp; ISO 9001:2015 certified manufacturing units based in Roorkee, Uttarakhand.</p>
        <p>Every product listed on this website is verified directly against its actual packaging &mdash; brand name, composition and pack size &mdash; so that doctors, pharmacists and stockists can rely on accurate, up-to-date information.</p>
      </div>
      <div class="hero-visual" style="background:#fff;border-color:var(--color-line);">
        {"".join(f'<img src="assets/img/products/{p["slug"]}/1.jpg" alt="{esc(p["name"])}" width="200" height="200" loading="lazy">' for p in PRODUCTS[:4])}
      </div>
    </div>
  </section>

  <section class="section section-alt">
    <div class="wrap">
      <div class="section-head"><div><h2>What We Stand For</h2></div></div>
      <div class="info-cards">
        <div class="info-card">{ICON_SHIELD}<h3>WHO-GMP &amp; ISO 9001:2015</h3><p>Our manufacturing partners hold WHO-GMP and ISO 9001:2015 certification, verified on-pack.</p></div>
        <div class="info-card">{ICON_FLASK}<h3>Verified Product Data</h3><p>Every composition and pack size on this site is cross-checked against the physical product.</p></div>
        <div class="info-card">{ICON_LEAF}<h3>Diverse Portfolio</h3><p>{len(PRODUCTS)} products across {len(CATEGORY_ORDER)} therapeutic categories, and growing.</p></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section-head"><div><h2>Our Categories</h2></div></div>
      <div class="product-grid">
        {''.join(f'<div class="info-card"><h3>{esc(c)}</h3><p>{len([p for p in PRODUCTS if p["category"]==c])} products</p><a href="products.html?category={quote(c)}">View products &rarr;</a></div>' for c in CATEGORY_ORDER)}
      </div>
    </div>
  </section>
</main>
'''
    html = page(
        "About Invision Healthcare | WHO-GMP Certified Pharmaceutical Company",
        "Invision Healthcare is a WHO-GMP & ISO 9001:2015 certified pharmaceutical company based in New Delhi, manufacturing medicines across six therapeutic categories.",
        "about.html", prefix, "about", body,
    )
    with open(os.path.join(PUBLIC, "about.html"), "w") as f:
        f.write(html)

build_about()

# ---------------- contact.html ----------------
def build_contact():
    prefix = ""
    body = f'''<main>
  <section class="section">
    <div class="wrap">
      <div class="section-head"><div><h1>Contact Us</h1><p>Reach out for product enquiries, stockist &amp; distributor queries.</p></div></div>
      <div class="contact-grid">
        <div class="contact-card">
          <div class="contact-row">{ICON_PHONE}<div><strong>Phone</strong><a href="tel:+919560093447">+91-9560093447</a></div></div>
          <div class="contact-row">{ICON_MAIL}<div><strong>Email</strong><a href="mailto:invisionhealthcare@gmail.com">invisionhealthcare@gmail.com</a></div></div>
          <div class="contact-row">{ICON_PIN}<div><strong>Registered Office</strong>No. 141, Sector 3, Pocket 16,<br>Dwarka, New Delhi - 110078, India</div></div>
          <div class="contact-row">{ICON_CLOCK}<div><strong>Business Hours</strong>Mon - Sat, 10:00 AM - 6:00 PM</div></div>
          <a class="btn btn-primary" href="https://wa.me/919560093447" style="margin-top:10px;">Chat on WhatsApp</a>
        </div>
        <div class="contact-card">
          <h3>Looking for a specific medicine?</h3>
          <p>Use our product search to check composition, pack size and category before you enquire.</p>
          <a class="btn btn-outline" style="border-color:var(--color-line);color:var(--color-primary);" href="products.html">Search Products</a>
          <h3 style="margin-top:24px;">Stockists &amp; Distributors</h3>
          <p>For distribution and stockist partnerships, please write to us at <a href="mailto:invisionhealthcare@gmail.com">invisionhealthcare@gmail.com</a> with your region and business details.</p>
        </div>
      </div>
    </div>
  </section>
</main>
'''
    html = page(
        "Contact Invision Healthcare | WHO-GMP Certified Pharmaceuticals",
        "Get in touch with Invision Healthcare for product enquiries, stockist and distributor partnerships. Based in Dwarka, New Delhi.",
        "contact.html", prefix, "contact", body,
    )
    with open(os.path.join(PUBLIC, "contact.html"), "w") as f:
        f.write(html)

build_contact()

print(f"Generated {len(PRODUCTS)} product pages, products.html, index.html, about.html, contact.html, sitemap.xml")
