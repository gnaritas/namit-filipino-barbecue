#!/usr/bin/env python3
"""Namit Filipino Barbecue — Columbia MD (9200 Old Annapolis Rd). Template-v2 multi-page build.
Every claim traced in evidence.json. Unknowns (hours, prices, reservations, delivery radius)
omitted — never guessed. Facts: hoodline/citybiz (owners, truck 2022->storefront soft open
2026-11-20), Baltimore Magazine via hoodline (sisig, lumpia, inasal, pancit, lechon),
Yelp/local.yahoo/MapQuest (phone 443-774-8969), card body (address, clover ordering, socials,
Bacolod origin). Zero JS. Hand-rolled HTML/CSS. noindex on demo host per lane doctrine.
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, 'public')
os.makedirs(PUB, exist_ok=True)

ORIGIN = 'https://namit-filipino-barbecue-demo.up.railway.app'
BRAND = 'Namit Filipino Barbecue'
BRAND_SHORT = 'Namit'
CITY = 'Columbia, MD'
STREET = '9200 Old Annapolis Road'
FULL_ADDR = '9200 Old Annapolis Road, Columbia, MD 21045'
PHONE = '+14437748969'
PHONE_TXT = '(443) 774-8969'
EMAIL = 'namitdmv@gmail.com'
CLOVER = 'https://www.clover.com/online-ordering/namit'
FB = 'https://www.facebook.com/namitFilipinobbq'
IG = 'https://www.instagram.com/namitfilipinobbq'
MAPQ = 'https://www.google.com/maps?q=9200%20Old%20Annapolis%20Road%2C%20Columbia%2C%20MD%2021045'
LAT, LON = 39.2353986, -76.8304298  # ArcGIS World Geocode of 9200 Old Annapolis Rd 21045 — exact address match, see evidence.json
NAP = f'{BRAND} · {STREET}, Columbia, MD 21045 · <a href="tel:{PHONE}">{PHONE_TXT}</a>'

def head(title, desc, path):
    u = ORIGIN + path
    return f'''<!-- BUILT-2026-11-25 -->
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{u}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{u}">
<meta property="og:image" content="{ORIGIN}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{ORIGIN}/og.png">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site">
<div class="sitenav">
  <a class="brand" href="/">{BRAND_SHORT}<span>Filipino Barbecue · Columbia, MD</span></a>
  <input type="checkbox" id="navtoggle" class="navtoggle" aria-label="Toggle menu">
  <label for="navtoggle" class="navbtn" aria-hidden="true"><i></i></label>
  <nav class="links" aria-label="Main">
    <a href="/menu">Menu</a>
    <a href="/barbecue">Barbecue</a>
    <a href="/ordering">Ordering</a>
    <a href="/contact">Contact</a>
    <a class="btn btn-sm" href="{CLOVER}">Order online</a>
  </nav>
</div>
</header>
<main id="main">
'''

FOOT = f'''</main>
<footer class="foot">
  <div class="footinner">
    <p class="footbrand">{BRAND}</p>
    <address class="footline">{NAP}</address>
    <p class="footline"><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{FB}">Facebook</a> · <a href="{IG}">Instagram</a></p>
    <p class="footline"><a href="/contact">Contact &amp; directions</a> · <a href="/privacy">Privacy</a></p>
  </div>
</footer>
</body>
</html>
'''

CTA_ROW = f'''<p class="ctorow"><a class="btn btn-big" href="{CLOVER}">Order online</a>
      <a class="btn btn-ghost btn-big" href="tel:{PHONE}">Call {PHONE_TXT}</a>
      <a class="btn btn-ghost btn-big" href="{MAPQ}">Get directions</a></p>'''

def ld(node):
    return '<script type="application/ld+json">' + json.dumps(node, ensure_ascii=False) + '</script>\n'

RESTAURANT = {
    "@context": "https://schema.org",
    "@type": "Restaurant",
    "name": BRAND,
    "image": ORIGIN + "/og.png",
    "url": ORIGIN + "/",
    "telephone": "+1-443-774-8969",
    "servesCuisine": ["Filipino", "Barbecue"],
    "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": "Columbia",
                "addressRegion": "MD", "postalCode": "21045", "addressCountry": "US"},
    "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LON},
    "hasMap": MAPQ,
    "sameAs": [FB, IG],
    "founder": [{"@type": "Person", "name": "Maria Carmel Tabligan"},
                {"@type": "Person", "name": "Paolo Peñalosa"}],
}

def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1,
                                 "name": n, "item": ORIGIN + p} for i, (n, p) in enumerate(items)]}

def pagehead(kicker, h1, sub, crumbs_html=""):
    return f'''<section class="pagehead">
  <div class="phinner">
    <p class="kicker">{kicker}</p>
    <h1>{h1}</h1>
    <p class="sub">{sub}</p>
    {CTA_ROW}
  </div>
</section>
'''

def navbar(current, crumbs_html=""):
    return f'''<nav class="youare" aria-label="Breadcrumb">{crumbs_html}</nav>'''

# ---------------------------------------------------------------- HOME
index = head("Filipino Barbecue in Columbia, MD — Namit Filipino Barbecue",
    "Filipino barbecue from Bacolod — inasal, sisig, lumpia, pancit, lechon — charcoal-grilled at Namit Filipino Barbecue, 9200 Old Annapolis Road, Columbia, MD.",
    "/")
index += f'''<section class="hero">
  <div class="heroinner">
    <p class="tagline">Halin sa Bacolod! — <em>From Bacolod!</em></p>
    <p class="kicker">Now grilling in Columbia, Maryland</p>
    <h1>Namit means <span class="emberword">delicious</span>.<br>Filipino barbecue,<br>charcoal-grilled.</h1>
    <p class="sub">Bacolod recipes and Filipino classics, the same skewers that built a loyal food-truck crowd across Anne Arundel and Howard counties — now served at our first storefront on Old Annapolis Road, right by the Howard County Circuit Courthouse.</p>
    {CTA_ROW}
    <p class="addrline">{STREET} · Columbia, MD 21045</p>
  </div>
</section>

<section class="strip">
  <p>Halin sa Bacolod! Filipino barbecue from the City of Smiles, grilled in Columbia.</p>
</section>

<section class="story" id="story">
  <p class="kicker">From a food truck to a front door</p>
  <h2>Years of skewers. Now a place to call home.</h2>
  <p>Nanit began in 2022 as a food truck, popping up around Anne Arundel and Howard counties with skewers of charcoal-grilled meat alongside Filipino staples. The truck regularly sold out — demand kept outrunning what the grill could carry in a day.</p>
  <p>In October 2026 the truck parked for good. On November 20, 2026, Namit opened its first brick-and-mortar restaurant at 9200 Old Annapolis Road, near Routes 29 and 108 — with help from a loan, grant and counseling through the Howard County Economic Development Authority.</p>
  <ul class="timeline">
    <li><b>2022</b><span>Food truck launches in Howard County</span></li>
    <li><b>Oct 2026</b><span>The truck parks for good</span></li>
    <li><b>Nov 20, 2026</b><span>First storefront soft opens in Columbia</span></li>
  </ul>
</section>

<section class="grillsec" id="grill">
  <p class="kicker">On the grill</p>
  <h2>The dishes Namit is known for</h2>
  <div class="dishgrid">
    <article class="dish"><h3>Inasal</h3><p>The charcoal-grilled chicken Bacolod is famous for — seasoned, skewered, flame-kissed.</p></article>
    <article class="dish"><h3>Sisig</h3><p>Sizzling chopped pork with its crisp-edged, squeeze-of-calamansi way of serving itself.</p></article>
    <article class="dish"><h3>Lumpia</h3><p>Crispy golden spring rolls — the party plate of every Filipino fiesta.</p></article>
    <article class="dish"><h3>Pancit</h3><p>Stir-fried noodles, long served for long lives.</p></article>
    <article class="dish"><h3>Lechon</h3><p>Pork roasted till the skin crackles — the celebration centerfold.</p></article>
    <article class="dish more"><h3>And more</h3><p>The menu rounds out the grill with Filipino home cooking. For what is on today, call <a href="tel:{PHONE}">{PHONE_TXT}</a> or check <a href="{CLOVER}">online ordering</a>.</p></article>
  </div>
  <p class="seemore"><a class="btn btn-ghost" href="/barbecue">More about the barbecue →</a> <a class="btn btn-ghost" href="/menu">See the menu →</a></p>
</section>

<section class="people">
  <p class="kicker">The kitchen</p>
  <h2>Maria Carmel &amp; Paolo — chef and owner, both</h2>
  <p>Maria Carmel Tabligan and Paolo Peñalosa — who also goes by Pawie Pen — own Namit and cook it together. They built its following one skewer at a time from the truck, and the regulars who lined up for it are the reason there is now a front door to walk through.</p>
  <p class="socialrow"><a href="{FB}">Facebook</a> · <a href="{IG}">Instagram</a></p>
</section>

<section class="visit" id="visit">
  <p class="kicker">Visit</p>
  <h2>Find Namit in Columbia</h2>
  <div class="visitgrid">
    <div class="visitinfo">
      <address><b>{BRAND}</b><br>{STREET}<br>Columbia, MD 21045</address>
      <p><a href="tel:{PHONE}">{PHONE_TXT}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p>Just down from the Howard County Circuit Courthouse, near Routes 29 and 108.</p>
      <p><a class="btn" href="{CLOVER}">Order online for pickup</a></p>
    </div>
    <div class="mapbox">
      <iframe title="Map to Namit Filipino Barbecue, 9200 Old Annapolis Road, Columbia, MD" src="{MAPQ}&output=embed" loading="lazy"></iframe>
    </div>
  </div>
  <div class="faq">
    <h2>Quick answers</h2>
    <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"><h3 itemprop="name">Where is Namit Filipino Barbecue?</h3><div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"><p itemprop="text">At {FULL_ADDR}, just down from the Howard County Circuit Courthouse near Routes 29 and 108.</p></div></div>
    <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"><h3 itemprop="name">Can I order online?</h3><div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"><p itemprop="text">Yes — Namit's online ordering runs through Clover. Or call ahead at {PHONE_TXT}.</p></div></div>
    <div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"><h3 itemprop="name">What should I try first?</h3><div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"><p itemprop="text">The classics that built the truck: inasal, sisig, lumpia, pancit and lechon.</p></div></div>
  </div>
</section>
''' + ld(dict(RESTAURANT, **{"@graph": [
    {"@type": "FAQPage", "@id": ORIGIN + "/#faq", "mainEntity": [
        {"@type": "Question", "name": "Where is Namit Filipino Barbecue?", "acceptedAnswer": {"@type": "Answer", "text": f"At {FULL_ADDR}, just down from the Howard County Circuit Courthouse near Routes 29 and 108."}},
        {"@type": "Question", "name": "Can I order online?", "acceptedAnswer": {"@type": "Answer", "text": f"Yes — Namit's online ordering runs through Clover. Or call ahead at {PHONE_TXT}."}},
        {"@type": "Question", "name": "What should I try first?", "acceptedAnswer": {"@type": "Answer", "text": "The classics that built the truck: inasal, sisig, lumpia, pancit and lechon."}}]}]})) + FOOT
pages = {"index.html": index}

# ---------------------------------------------------------------- MENU hub
menu = head("Menu — Namit Filipino Barbecue, Columbia MD",
    "The Namit Filipino Barbecue menu in Columbia, MD: inasal, sisig, lumpia, pancit, lechon and Filipino home cooking. Order ahead on Clover or call (443) 774-8969.",
    "/menu")
menu += pagehead("Menu", "What Namit grills", "The dishes the truck was known for, served at the storefront. For today's full menu and prices, call or order on Clover.")
menu += f'''<section>
  <div class="menurows">
    <div class="mrow"><div><h3>Inasal</h3><p>Bacolod-style charcoal-grilled chicken — Namit's signature fire.</p></div><span class="dot"></span></div>
    <div class="mrow"><div><h3>Sisig</h3><p>Sizzling chopped pork, crisp edges, calamansi.</p></div><span class="dot"></span></div>
    <div class="mrow"><div><h3>Lumpia</h3><p>Crispy golden spring rolls.</p></div><span class="dot"></span></div>
    <div class="mrow"><div><h3>Pancit</h3><p>Stir-fried noodles for long lives.</p></div><span class="dot"></span></div>
    <div class="mrow"><div><h3>Lechon</h3><p>Crackling-skinned roasted pork.</p></div><span class="dot"></span></div>
    <div class="mrow"><div><h3>Skewers</h3><p>Barbecued meats on the stick — what the truck was built on.</p></div><span class="dot"></span></div>
  </div>
  <p class="menunote">The menu follows the market and the day. Prices are in store and on <a href="{CLOVER}">Clover online ordering</a>, or ask at the counter — <a href="tel:{PHONE}">{PHONE_TXT}</a>.</p>
  <p class="ctorow"><a class="btn btn-big" href="{CLOVER}">Order on Clover</a> <a class="btn btn-ghost btn-big" href="/barbecue">More about the barbecue</a></p>
</section>
''' + ld({"@context": "https://schema.org", "@type": "Menu", "name": "Namit Filipino Barbecue Menu", "inLanguage": "en", "hasMenuItem": [
    {"@type": "MenuItem", "name": n} for n in ["Inasal", "Sisig", "Lumpia", "Pancit", "Lechon", "Skewers"]],
    "servesCuisine": ["Filipino"], "audience": {"@type": "Audience", "audienceType": "Columbia, MD diners"}}) + FOOT
pages["menu.html"] = menu

# ---------------------------------------------------------------- BARBECUE detail
bbq = head("Inasal, Lechon & Sisig — Namit Filipino Barbecue, Columbia MD",
    "Inasal, lechon and sisig — Bacolod-style Filipino barbecue charcoal-grilled in Columbia, MD by Namit Filipino Barbecue.",
    "/barbecue")
bbq += pagehead("Barbecue", "Inasal, lechon &amp; sisig — the Bacolod fire", "Bacolod is the City of Smiles, and chicken inasal is what it is famous for grilling. Namit brings that fire to Columbia on a storefront grill.")
bbq += f'''<section>
  <article class="longform">
    <h2>What "Filipino barbecue" means here</h2>
    <p>Filipino barbecue is its own tradition: meats seasoned bright with vinegar and calamansi, colored with achuete, grilled hard over coals. Inasal — the chicken Bacolod grill masters are known for — is Namit's signature. Sisig brings the sizzle: chopped pork with crisp edges, served hot enough to crack an egg on it. Lechon is the celebration: pork roasted till the skin crackles.</p>
    <h2>From the truck's grill to this one</h2>
    <p>For years, whatever Namit grilled sold out before the day was done — demand kept outrunning the truck. The storefront grill is the answer to that: owners and chefs Maria Carmel Tabligan and Paolo Peñalosa built the first kitchen so the skewers stop running out.</p>
    <p class="ctorow"><a class="btn btn-big" href="{CLOVER}">Order online</a> <a class="btn btn-ghost btn-big" href="tel:{PHONE}">Call {PHONE_TXT}</a></p>
    <p class="crumbsline">Full spread: <a href="/menu">the menu</a> · <a href="/ordering">takeout &amp; online ordering</a> · <a href="/contact">visit us</a></p>
  </article>
</section>
''' + ld({"@context": "https://schema.org", "@type": "Service", "name": "Bacolod-style Filipino barbecue", "serviceType": "Dining and takeaway of Filipino barbecue", "provider": RESTAURANT, "areaServed": {"@type": "City", "name": "Columbia, MD"}, "url": ORIGIN + "/barbecue"}) + FOOT
pages["barbecue.html"] = bbq

# ---------------------------------------------------------------- ORDERING detail
order = head("Takeout & Online Ordering — Namit Filipino Barbecue, Columbia MD",
    "Order Namit Filipino Barbecue for pickup in Columbia, MD — online ordering through Clover, or call ahead at (443) 774-8969.",
    "/ordering")
order += pagehead("Ordering", "Takeout &amp; online ordering", "Namit's online ordering runs through Clover. Order ahead, pick up at the storefront, or call the counter.")
order += f'''<section>
  <article class="longform">
    <h2>Order ahead</h2>
    <p>Namet's official online ordering channel is <a href="{CLOVER}">Clover online ordering</a>. Place the order there and pick it up at {STREET}. Call ahead at <a href="tel:{PHONE}">{PHONE_TXT}</a> and the counter will take care of the rest.</p>
    <h3>Good to know</h3>
    <ul class="plainlist">
      <li>The full menu, prices and today's specials live on Clover and at the counter.</li>
      <li>Pickup is at the storefront — just down from the Howard County Circuit Courthouse, near Routes 29 and 108.</li>
      <li>Questions about a big order or a party? <a href="/contact">Send us a note</a> or call the counter.</li>
    </ul>
    <p class="ctorow"><a class="btn btn-big" href="{CLOVER}">Order on Clover</a> <a class="btn btn-ghost btn-big" href="tel:{PHONE}">Call {PHONE_TXT}</a></p>
    <p class="crumbsline"><a href="/menu">See the menu</a> · <a href="/barbecue">More about the barbecue</a> · <a href="/contact">Contact &amp; directions</a></p>
  </article>
</section>
''' + ld({"@context": "https://schema.org", "@type": "Service", "name": "Takeout and online ordering", "serviceType": "Takeout", "provider": RESTAURANT, "areaServed": {"@type": "City", "name": "Columbia, MD"}, "url": ORIGIN + "/ordering"}) + FOOT
pages["ordering.html"] = order

# ---------------------------------------------------------------- CONTACT
contact = head("Contact & Directions — Namit Filipino Barbecue, Columbia MD",
    "Contact Namit Filipino Barbecue in Columbia, MD: (443) 774-8969, namitdmv@gmail.com, 9200 Old Annapolis Road — directions, map and message form.",
    "/contact")
contact += pagehead("Contact", "Talk to Namit", "Call the counter, send a note, or come find us on Old Annapolis Road.")
contact += f'''<section>
  <div class="visitgrid">
    <div class="visitinfo">
      <h2>The storefront</h2>
      <address><b>{BRAND}</b><br>{STREET}<br>Columbia, MD 21045</address>
      <p><a href="tel:{PHONE}">{PHONE_TXT}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p><a href="{FB}">Facebook</a> · <a href="{IG}">Instagram</a></p>
      <p><a class="btn" href="{CLOVER}">Order online</a></p>
      <p class="crumbsline">Also: <a href="/menu">menu</a> · <a href="/barbecue">barbecue</a> · <a href="/ordering">ordering</a></p>
    </div>
    <div class="mapbox">
      <iframe title="Map to Namit Filipino Barbecue, 9200 Old Annapolis Road, Columbia, MD" src="{MAPQ}&output=embed" loading="lazy"></iframe>
    </div>
  </div>
  <div class="formwrap">
    <h2>Send a note</h2>
    <form class="cform" method="post" action="/contact">
      <label for="f-name">Your name</label>
      <input id="f-name" name="name" type="text" autocomplete="name">
      <label for="f-email">Email</label>
      <input id="f-email" name="email" type="email" autocomplete="email">
      <label for="f-msg">Message</label>
      <textarea id="f-msg" name="message" rows="5" required></textarea>
      <p><button class="btn btn-big" type="submit">Send message</button></p>
    </form>
    <p class="formnote">We answer as fast as the grill lets us.</p>
  </div>
</section>
''' + ld(crumbs([("Home", "/"), ("Contact", "/contact")])) + FOOT
pages["contact.html"] = contact

# ---------------------------------------------------------------- PRIVACY
priv = head("Privacy Policy — Namit Filipino Barbecue",
    "Privacy policy for the Namit Filipino Barbecue website: no cookies, no trackers, contact-form messages only.",
    "/privacy")
priv += pagehead("Privacy", "This site keeps things simple", "No cookies, no trackers, no advertising scripts — just the menu, the map, and the message form.")
priv += f'''<section>
  <article class="longform">
    <h2>What this site collects</h2>
    <p>This website sets no cookies and loads no analytics or advertising scripts. Links out to Facebook, Instagram and Clover follow your browser there, where their own privacy policies apply.</p>
    <h2>The message form</h2>
    <p>Whatever you type into the contact form — your name, email and message — is sent to the business for the sole purpose of getting back to you. It is not sold, shared, or used for anything else.</p>
    <h2>Questions</h2>
    <p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{PHONE}">{PHONE_TXT}</a>.</p>
  </article>
</section>
''' + ld({"@context": "https://schema.org", "@type": "WebPage", "name": "Privacy Policy", "url": ORIGIN + "/privacy",
          "about": {"@type": "Restaurant", "name": BRAND}}) + FOOT
pages["privacy.html"] = priv

# ---------------------------------------------------------------- 404 + THANKS
nf = head("Page Not Found — Namit Filipino Barbecue", "Page not found at the Namit Filipino Barbecue website.", "/404")
nf += f'''<section class="nf">
  <p class="big404">4 0 4</p>
  <h1>That plate is empty</h1>
  <p>The page you asked for isn't here. The grill, though, still is.</p>
  <p class="ctorow"><a class="btn btn-big" href="/">Back home</a> <a class="btn btn-ghost btn-big" href="/menu">See the menu</a> <a class="btn btn-ghost btn-big" href="/contact">Contact us</a></p>
</section>
''' + FOOT
pages["404.html"] = nf

th = head("Thank You — Namit Filipino Barbecue", "Your message was sent to Namit Filipino Barbecue.", "/thanks")
th += f'''<section class="nf">
  <p class="tagline">Salamat!</p>
  <h1>Your message is sent</h1>
  <p>The Namit team will get back to you as fast as the grill lets them. Need it right now? Call <a href="tel:{PHONE}">{PHONE_TXT}</a> or order on <a href="{CLOVER}">Clover</a>.</p>
  <p class="ctorow"><a class="btn btn-big" href="/">Back home</a></p>
</section>
''' + FOOT
pages["thanks.html"] = th

# ---------------------------------------------------------------- statics
sitemap_pages = ["/", "/menu", "/barbecue", "/ordering", "/contact", "/privacy"]
pages["sitemap.xml"] = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
    "".join(f'<url><loc>{ORIGIN}{p}</loc><lastmod>2026-11-26</lastmod></url>\n' for p in sitemap_pages) + '</urlset>\n'
pages["robots.txt"] = f"User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n"

for name, body in pages.items():
    with open(os.path.join(PUB, name), "w", encoding="utf-8") as f:
        f.write(body)
    print(f"wrote {name} ({len(body.encode('utf-8'))} B)")
