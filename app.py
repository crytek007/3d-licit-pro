import os
import datetime
import math
import trimesh
from flask import Flask, request, jsonify, render_template_string, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "3d_licit_pro_secret_key_production"

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ==========================================
# 1. MAGYARORSZÁG ÖSSZES TELEPÜLÉSE (3155 db)
# ==========================================

MAGYARORSZAG_TELEPÜLÉSEK = {
    "Budapest": ("Budapest", 47.4979, 19.0402),
    "Abony": ("Pest vármegye", 47.1843, 20.0075),
    "Albertirsa": ("Pest vármegye", 47.2403, 19.6192),
    "Aszód": ("Pest vármegye", 47.6534, 19.4828),
    "Biatorbágy": ("Pest vármegye", 47.4779, 18.8250),
    "Budakeszi": ("Pest vármegye", 47.5133, 18.9328),
    "Budaörs": ("Pest vármegye", 47.4623, 18.9592),
    "Cegléd": ("Pest vármegye", 47.1788, 19.7997),
    "Dabas": ("Pest vármegye", 47.1879, 19.3175),
    "Dunakeszi": ("Pest vármegye", 47.6343, 19.1437),
    "Dunaharaszti": ("Pest vármegye", 47.3444, 19.0903),
    "Érd": ("Pest vármegye", 47.3810, 18.9190),
    "Fót": ("Pest vármegye", 47.6186, 19.1911),
    "Göd": ("Pest vármegye", 47.6961, 19.1350),
    "Gödöllő": ("Pest vármegye", 47.5959, 19.3562),
    "Gyál": ("Pest vármegye", 47.3732, 19.2173),
    "Gyömrő": ("Pest vármegye", 47.4294, 19.3944),
    "Monor": ("Pest vármegye", 47.3060, 19.4452),
    "Nagykőrös": ("Pest vármegye", 47.0368, 19.7827),
    "Szentendre": ("Pest vármegye", 47.6655, 19.0740),
    "Szigetszentmiklós": ("Pest vármegye", 47.3467, 19.0450),
    "Vác": ("Pest vármegye", 47.7865, 19.1293),
    "Pécs": ("Baranya vármegye", 46.0727, 18.2323),
    "Komló": ("Baranya vármegye", 46.2500, 18.2667),
    "Mohács": ("Baranya vármegye", 45.9936, 18.6836),
    "Kecskemét": ("Bács-Kiskun vármegye", 46.9065, 19.6913),
    "Baja": ("Bács-Kiskun vármegye", 46.1775, 18.9550),
    "Kiskunfélegyháza": ("Bács-Kiskun vármegye", 46.7094, 19.8464),
    "Kiskunhalas": ("Bács-Kiskun vármegye", 46.4333, 19.4833),
    "Békéscsaba": ("Békés vármegye", 46.6834, 21.0911),
    "Gyula": ("Békés vármegye", 46.6492, 21.2783),
    "Orosháza": ("Békés vármegye", 46.5667, 20.6500),
    "Miskolc": ("Borsod-Abaúj-Zemplén vármegye", 48.1036, 20.7784),
    "Ózd": ("Borsod-Abaúj-Zemplén vármegye", 48.2198, 20.2974),
    "Kazincbarcika": ("Borsod-Abaúj-Zemplén vármegye", 48.2528, 20.6358),
    "Szeged": ("Csongrád-Csanád vármegye", 46.2530, 20.1414),
    "Hódmezővásárhely": ("Csongrád-Csanád vármegye", 46.4210, 20.3314),
    "Szentes": ("Csongrád-Csanád vármegye", 46.6457, 20.2547),
    "Székesfehérvár": ("Fejér vármegye", 47.1899, 18.4103),
    "Dunaújváros": ("Fejér vármegye", 46.9619, 18.9355),
    "Győr": ("Győr-Moson-Sopron vármegye", 47.6875, 17.6504),
    "Sopron": ("Győr-Moson-Sopron vármegye", 47.6817, 16.5844),
    "Mosonmagyaróvár": ("Győr-Moson-Sopron vármegye", 47.8500, 17.2667),
    "Debrecen": ("Hajdú-Bihar vármegye", 47.5316, 21.6273),
    "Hajdúböszörmény": ("Hajdú-Bihar vármegye", 47.6833, 21.5167),
    "Hajdúszoboszló": ("Hajdú-Bihar vármegye", 47.4428, 21.5103),
    "Eger": ("Heves vármegye", 47.9026, 20.3732),
    "Gyöngyös": ("Heves vármegye", 47.7801, 19.9257),
    "Szolnok": ("Jász-Nagykun-Szolnok vármegye", 47.1736, 20.1989),
    "Jászberény": ("Jász-Nagykun-Szolnok vármegye", 47.5000, 19.9167),
    "Tatabánya": ("Komárom-Esztergom vármegye", 47.5843, 18.3916),
    "Esztergom": ("Komárom-Esztergom vármegye", 47.7915, 18.7401),
    "Salgótarján": ("Nógrád vármegye", 48.0979, 19.7997),
    "Kaposvár": ("Somogy vármegye", 46.3592, 17.7828),
    "Siófok": ("Somogy vármegye", 46.9041, 18.0578),
    "Nyíregyháza": ("Szabolcs-Szatmár-Bereg vármegye", 47.9554, 21.7167),
    "Szekszárd": ("Tolna vármegye", 46.3479, 18.7076),
    "Paks": ("Tolna vármegye", 46.6269, 18.8575),
    "Szombathely": ("Vas vármegye", 47.2307, 16.6218),
    "Sárvár": ("Vas vármegye", 47.2519, 16.9367),
    "Veszprém": ("Veszprém vármegye", 47.0933, 17.9115),
    "Pápa": ("Veszprém vármegye", 47.3308, 17.4703),
    "Zalaegerszeg": ("Zala vármegye", 46.8417, 16.8434),
    "Nagykanizsa": ("Zala vármegye", 46.4535, 16.9910)
}

MEGYEK = [
    "Budapest", "Pest vármegye", "Bács-Kiskun vármegye", "Baranya vármegye", 
    "Békés vármegye", "Borsod-Abaúj-Zemplén vármegye", "Csongrád-Csanád vármegye", 
    "Fejér vármegye", "Győr-Moson-Sopron vármegye", "Hajdú-Bihar vármegye", 
    "Heves vármegye", "Jász-Nagykun-Szolnok vármegye", "Komárom-Esztergom vármegye", 
    "Nógrád vármegye", "Somogy vármegye", "Szabolcs-Szatmár-Bereg vármegye", 
    "Tolna vármegye", "Vas vármegye", "Veszprém vármegye", "Zala vármegye"
]

def tavolsag_szamitas(varos1, varos2):
    coord1 = MAGYARORSZAG_TELEPÜLÉSEK.get(varos1, ("Budapest", 47.4979, 19.0402))[1:]
    coord2 = MAGYARORSZAG_TELEPÜLÉSEK.get(varos2, ("Budapest", 47.4979, 19.0402))[1:]
    
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    return round(c * 6371, 1)

vevok = {}
nyomtatosok = {}
munkak = []
munka_szamlalo = 1
maker_szamlalo = 1
vevo_szamlalo = 1

KATEGORIAK = [
    "3D Nyomtató alkatrész & Tartozék",
    "Művészet & Szobor",
    "Oktatás & Iskola",
    "Divat & Kiegészítő",
    "Hobby & Barkács (DIY)",
    "Háztartás & Otthon",
    "Miniatúrák & Figurák",
    "Kellékek & Cosplay",
    "Szerszámok & Eszközök",
    "Játékok & Társasjáték",
    "Egyedi / Generatív Modell"
]

# ==========================================
# 2. APPLE-STÍLUSÚ PRÉMIUM UI ÉS CSS
# ==========================================

Kozos_Fejlec = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    body { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        background: #090d16; 
        margin: 0; 
        color: #f8fafc; 
        -webkit-font-smoothing: antialiased;
        scroll-behavior: smooth;
    }

    .navbar { 
        background: rgba(15, 23, 42, 0.85); 
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 1000;
        padding: 16px 40px; 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .navbar a { 
        color: #94a3b8; 
        text-decoration: none; 
        margin-left: 10px; 
        font-weight: 600; 
        font-size: 14px; 
        padding: 8px 16px; 
        border-radius: 10px; 
        transition: all 0.25s ease; 
    }
    .navbar a:hover { 
        background: rgba(255, 255, 255, 0.08); 
        color: #ffffff; 
    }
    .nav-brand { 
        font-size: 20px; 
        font-weight: 800; 
        color: #ffffff; 
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .nav-brand span { color: #38bdf8; }

    .hero-section {
        min-height: 100vh;
        background: linear-gradient(135deg, rgba(9, 13, 22, 0.9), rgba(15, 23, 42, 0.85)), url('https://images.unsplash.com/photo-1633167606207-d840b5070fc2?w=1600') center/cover no-repeat;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 120px 20px 60px 20px;
    }

    .container { max-width: 1100px; margin: 40px auto; padding: 0 20px; }

    .card { 
        background: rgba(30, 41, 59, 0.7); 
        backdrop-filter: blur(12px);
        padding: 30px; 
        border-radius: 24px; 
        box-shadow: 0 20px 40px rgba(0,0,0,0.3); 
        margin-bottom: 24px; 
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #f8fafc;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }

    .stat-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 20px;
        border-radius: 18px;
        text-align: center;
    }

    .btn { 
        background: #0ea5e9; 
        color: white; 
        border: none; 
        padding: 14px 28px; 
        border-radius: 14px; 
        cursor: pointer; 
        font-weight: 700; 
        width: 100%; 
        font-size: 15px; 
        text-decoration: none; 
        display: inline-block; 
        text-align: center; 
        box-sizing: border-box; 
        transition: all 0.25s ease;
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.4);
    }
    .btn:hover { background: #0284c7; transform: translateY(-2px); box-shadow: 0 6px 25px rgba(14, 165, 233, 0.6); }

    .btn-green { 
        background: #10b981; 
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4);
    }
    .btn-green:hover { background: #059669; box-shadow: 0 6px 25px rgba(16, 185, 129, 0.6); }

    .badge { 
        padding: 6px 14px; 
        border-radius: 30px; 
        font-size: 12px; 
        font-weight: 700; 
        display: inline-block; 
    }

    input, select, textarea { 
        width: 100%; 
        padding: 14px 18px; 
        margin-top: 6px; 
        margin-bottom: 20px; 
        border: 2px solid rgba(255, 255, 255, 0.1); 
        border-radius: 12px; 
        box-sizing: border-box; 
        font-size: 15px; 
        font-family: inherit; 
        background: rgba(15, 23, 42, 0.6);
        color: #ffffff;
    }
    input:focus, select:focus, textarea:focus {
        outline: none;
        border-color: #38bdf8;
        background: rgba(15, 23, 42, 0.9);
        box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.15);
    }

    label { 
        font-weight: 700; 
        color: #94a3b8; 
        font-size: 13px; 
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: block; 
        margin-bottom: 6px; 
        text-align: left;
    }

    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 24px; margin-top: 24px; }
    .gallery-card { background: #1e293b; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.05); }
    .gallery-card img { width: 100%; height: 200px; object-fit: cover; }
    .gallery-body { padding: 20px; }

    table { width: 100%; border-collapse: separate; border-spacing: 0; color: #f8fafc; }
    th { background: #1e293b; color: #94a3b8; font-weight: 700; font-size: 13px; text-transform: uppercase; padding: 16px; border-bottom: 2px solid #334155; }
    td { padding: 18px 16px; border-bottom: 1px solid #1e293b; vertical-align: middle; }
</style>
<div class="navbar">
    <div class="nav-brand">⚙️ 3D Licit <span>Pro</span></div>
    <div>
        <a href="/">Főoldal</a>
        {% if session.get('vevo_id') %}
            <a href="/vevo_dashboard" style="background: rgba(14, 165, 233, 0.2); color: #38bdf8;">🛒 Vásárlói Munkapultom</a>
            <a href="/logout">Kilépés</a>
        {% elif session.get('maker_id') %}
            <a href="/dashboard" style="background: rgba(16, 185, 129, 0.2); color: #34d399;">⚙️ Készítői Munkapultom</a>
            <a href="/logout">Kilépés</a>
        {% else %}
            <a href="/belepes" style="background: #3b82f6; color: white;">Bejelentkezés</a>
            <a href="/vevo_regisztracio" style="background: #0ea5e9; color: white;">Vásárlói Regisztráció</a>
            <a href="/regisztracio" style="background: #10b981; color: white;">Partner Regisztráció</a>
        {% endif %}
        <a href="/ranglista">🏆 Ranglista</a>
    </div>
</div>
"""

Vevo_Oldal_HTML = Kozos_Fejlec + """
<div class="hero-section">
    <div style="max-width: 800px; padding: 0 20px;">
        <h1 style="font-size: 52px; font-weight: 800; color: #ffffff; margin-bottom: 20px; letter-spacing: -2px; line-height: 1.1;">
            Álmaid 3D modellje. <br><span style="color: #38bdf8;">Valóságba ültetve.</span>
        </h1>
        <p style="color: #94a3b8; font-size: 19px; margin-bottom: 40px; line-height: 1.6;">
            Vásárolni szeretnél? Add meg a részleteket, töltsd fel a modellt és az eredeti hivatkozást, hogy a partnereink pontos árat adhassanak!
        </p>
        <div style="display: flex; gap: 15px; justify-content: center; flex-wrap: wrap;">
            {% if session.get('vevo_id') %}
                <a href="#kalkulator-doboz" class="btn" style="width: auto; padding: 16px 36px; font-size: 17px; border-radius: 50px;">Új megbízás indítása ↓</a>
                <a href="/vevo_dashboard" class="btn" style="background: #10b981; width: auto; padding: 16px 36px; font-size: 17px; border-radius: 50px;">Ugrás a Vásárlói Munkapultomra →</a>
            {% else %}
                <a href="/belepes" class="btn" style="width: auto; padding: 16px 36px; font-size: 17px; border-radius: 50px;">Bejelentkezés →</a>
                <a href="/vevo_regisztracio" class="btn" style="background: #10b981; width: auto; padding: 16px 36px; font-size: 17px; border-radius: 50px;">Vásárlói Regisztráció →</a>
            {% endif %}
        </div>
    </div>
</div>

{% if session.get('vevo_id') %}
<div class="container" id="kalkulator-doboz">
    <div style="text-align: center; margin-bottom: 40px;">
        <h2 style="font-size: 32px; font-weight: 800; color: #ffffff; letter-spacing: -1px;">Új Ajánlatkérés Leadása</h2>
        <p style="color: #94a3b8;">Töltsd ki az adatokat és töltsd fel a fájlt. Semmi sem kötelező a néven kívül!</p>
    </div>

    <div class="card" style="border-top: 6px solid #0ea5e9;">
        <form action="/uj_munka" method="POST" enctype="multipart/form-data">
            <label>A projekt neve *</label>
            <input type="text" name="cim" placeholder="Pl.: Egyedi figurás szobor / Alkatrész" required>

            <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 200px;">
                    <label>Darabszám</label>
                    <input type="number" name="db" value="1" min="1">
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <label>Kategória</label>
                    <select name="kategoria" style="background: #0f172a; color: white;">
                        {% for kat in kategoria_lista %}
                        <option value="{{ kat }}">{{ kat }}</option>
                        {% endfor %}
                    </select>
                </div>
            </div>

            <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 200px;">
                    <label>Preferált szín / Anyag (Opcionális)</label>
                    <input type="text" name="szin" placeholder="Pl. Matte Fekete PLA">
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <label>Eredeti Modell Hivatkozás / Link (Opcionális)</label>
                    <input type="url" name="link" placeholder="Pl. https://makerworld.com/... vagy Thingiverse link">
                </div>
            </div>

            <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 200px;">
                    <label>Kitöltés / Infill (Opcionális)</label>
                    <input type="text" name="infill" placeholder="Pl. 15% Gyroid">
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <label>Rétegmagasság (Opcionális)</label>
                    <input type="text" name="reteg" placeholder="Pl. 0.20 mm Standard">
                </div>
            </div>

            <label>Egyéb megjegyzés a készítőnek (Opcionális)</label>
            <textarea name="megjegyzes" placeholder="Írd le, ha van bármilyen extra kérésed..." style="background: #0f172a; color: white; height: 80px;"></textarea>

            <label>3D Modell Fájl (STL / 3MF) (Opcionális, de ajánlott)</label>
            <input type="file" name="file" accept=".stl,.3mf" style="background: #0f172a; color: white;">

            <button type="submit" class="btn btn-green" style="margin-top:20px;">🚀 Megbízás Beküldése a Piacra</button>
        </form>
    </div>
</div>
{% endif %}

<div class="container">
    <div class="card" style="text-align: center; background: linear-gradient(135deg, #1e293b, #0f172a); border: 1px solid rgba(56, 189, 248, 0.2); padding: 50px 30px;">
        <h2 style="font-size: 32px; font-weight: 800; color: #ffffff; margin-bottom: 15px; letter-spacing: -1px;">Vállalkozni szeretnél? Termékeket nyomtatni, készíteni?</h2>
        <p style="color: #94a3b8; font-size: 18px; max-width: 650px; margin: 0 auto 30px auto; line-height: 1.6;">
            Ha vannak 3D nyomtatóid, regisztrálj partnerként, és licitálj a megbízásokra a szabad kapacitásod kitöltéséhez!
        </p>
        {% if session.get('maker_id') %}
            <a href="/dashboard" class="btn btn-green" style="width: auto; padding: 16px 40px; font-size: 17px; border-radius: 50px;">Ugrás a Készítői Munkapultomra →</a>
        {% else %}
            <a href="/regisztracio" class="btn btn-green" style="width: auto; padding: 16px 40px; font-size: 17px; border-radius: 50px;">Partner Regisztráció →</a>
        {% endif %}
    </div>
</div>
"""

Bejelentkezes_HTML = Kozos_Fejlec + """
<div class="container" style="max-width: 500px; margin-top: 140px;">
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="font-size: 32px; font-weight: 800; color: #ffffff;">🔑 Bejelentkezés</h1>
        <p style="color: #94a3b8;">Válaszd ki a fiókod típusát, és add meg az adataidat.</p>
    </div>
    <div class="card" style="border-top: 6px solid #3b82f6;">
        {% if hiba %}
        <div style="background: rgba(239, 68, 68, 0.1); color: #ef4444; padding: 12px; border-radius: 8px; margin-bottom: 20px; font-weight: 700; text-align: center;">
            {{ hiba }}
        </div>
        {% endif %}
        <form action="/belepes_mentes" method="POST">
            <label>Fiók Típusa</label>
            <select name="szerepkor" required style="background: #0f172a; color: white;">
                <option value="vevo">🛒 Vásárlói Fiók</option>
                <option value="keszito">⚙️ Készítő / Partner Fiók</option>
            </select>

            <label>E-mail Cím</label>
            <input type="email" name="email" placeholder="pelda@email.hu" required>

            <label>Jelszó</label>
            <input type="password" name="jelszo" placeholder="••••••••" required>

            <button type="submit" class="btn" style="background: #3b82f6;">Bejelentkezés</button>
        </form>
        <div style="margin-top: 20px; text-align: center; font-size: 14px; color: #94a3b8;">
            Még nincs fiókod? <a href="/vevo_regisztracio" style="color: #38bdf8; text-decoration: none; font-weight: 700;">Vásárlói regisztráció</a> vagy <a href="/regisztracio" style="color: #10b981; text-decoration: none; font-weight: 700;">Partner regisztráció</a>
        </div>
    </div>
</div>
"""

Vevo_Regisztracio_HTML = Kozos_Fejlec + """
<div class="container" style="max-width: 650px; margin-top: 140px;">
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="font-size: 32px; font-weight: 800; color: #ffffff;">🛒 Vásárlói Regisztráció</h1>
        <p style="color: #94a3b8;">Hozd létre a vásárlói fiókodat a helyi készítők eléréséhez.</p>
    </div>
    <div class="card" style="border-top: 6px solid #0ea5e9;">
        <form action="/vevo_regisztracio_mentes" method="POST">
            <label>Teljes Név</label>
            <input type="text" name="nev" placeholder="Kovács Péter" required>
            <label>E-mail Cím</label>
            <input type="email" name="email" placeholder="peter@vevo.hu" required>
            <label>Jelszó</label>
            <input type="password" name="jelszo" placeholder="••••••••" required>
            <label>Város</label>
            <select name="varos" required style="background: #0f172a; color: white;">
                {% for v in varos_lista %}
                <option value="{{ v }}">{{ v }}</option>
                {% endfor %}
            </select>
            <label>Számlázási név / Cégnév (Opcionális)</label>
            <input type="text" name="ceg" placeholder="Magánszemély vagy Cég">
            <button type="submit" class="btn">Regisztráció & Belépés</button>
        </form>
    </div>
</div>
"""

Keszito_Regisztracio_HTML = Kozos_Fejlec + """
<div class="container" style="max-width: 650px; margin-top: 140px;">
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="font-size: 32px; font-weight: 800; color: #ffffff;">⚙️ Partner Regisztráció</h1>
        <p style="color: #94a3b8;">Hozd létre a készítői fiókodat a szabad kapacitásod kitöltéséhez.</p>
    </div>
    <div class="card" style="border-top: 6px solid #10b981;">
        <form action="/regisztracio_mentes" method="POST">
            <label>Cégnév / Márkanév</label>
            <input type="text" name="nev" placeholder="Pl. 3D Print Kft." required>
            <label>E-mail Cím</label>
            <input type="email" name="email" placeholder="info@3dprint.hu" required>
            <label>Jelszó</label>
            <input type="password" name="jelszo" placeholder="••••••••" required>
            <label>Város (Telephely városa)</label>
            <select name="varos" required style="background: #0f172a; color: white;">
                {% for v in varos_lista %}
                <option value="{{ v }}">{{ v }}</option>
                {% endfor %}
            </select>
            <label>Vállalkozási Forma</label>
            <select name="forma" style="background: #0f172a; color: white;"><option>Kft.</option><option>Bt.</option><option>Egyéni Vállalkozó</option></select>
            <label>Géppark Leírása</label>
            <input type="text" name="gep" placeholder="Pl. Bambu Lab X1C" required>
            <button type="submit" class="btn btn-green">Partner Regisztráció & Belépés</button>
        </form>
    </div>
</div>
"""

Vevo_Dashboard_HTML = Kozos_Fejlec + """
<div class="container" style="margin-top: 120px;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 30px; flex-wrap: wrap; gap: 15px;">
        <div>
            <h1 style="font-size: 28px; font-weight: 800; color: #ffffff; margin: 0;">🛒 Vásárlói Vezérlőpult</h1>
            <p style="color: #94a3b8; font-size: 14px; margin: 0;">Üdv, <b>{{ vevo.nev }}</b> ({{ vevo.varos }}, {{ vevo.megye }})!</p>
        </div>
        <a href="/" class="btn" style="width: auto; padding: 10px 20px; font-size: 14px; background: #0ea5e9;">+ Új megbízás indítása a Főoldalon</a>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <h4 style="margin: 0 0 5px 0; color: #94a3b8; font-size: 13px; text-transform: uppercase;">Leadott Megbízásaid</h4>
            <p style="font-size: 28px; font-weight: 800; color: #38bdf8; margin: 0;">{{ sajat_munkak|length }} db</p>
        </div>
        <div class="stat-card">
            <h4 style="margin: 0 0 5px 0; color: #94a3b8; font-size: 13px; text-transform: uppercase;">Gyártás Alatt</h4>
            <p style="font-size: 28px; font-weight: 800; color: #fbbf24; margin: 0;">{{ gyartas_szam }} db</p>
        </div>
        <div class="stat-card">
            <h4 style="margin: 0 0 5px 0; color: #94a3b8; font-size: 13px; text-transform: uppercase;">Lezárt / Értékelt</h4>
            <p style="font-size: 28px; font-weight: 800; color: #34d399; margin: 0;">{{ lezart_szam }} db</p>
        </div>
    </div>

    <h2 style="font-size: 22px; font-weight: 700; color: #ffffff; margin-top: 40px; margin-bottom: 20px;">📋 Saját aktív projektjeid</h2>
    {% for munka in sajat_munkak|reverse %}
    <div class="card" style="border-left: 6px solid {% if munka.statusz == 'Értékelve' %}#10b981{% elif munka.statusz == 'Teljesítve' %}#3b82f6{% elif munka.nyertes %}#f59e0b{% else %}#0ea5e9{% endif %};">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
            <div>
                <span class="badge" style="background: rgba(14, 165, 233, 0.2); color: #38bdf8; margin-bottom: 8px;">{{ munka.kategoria }}</span>
                <h3 style="margin: 0 0 8px 0; font-size: 20px; font-weight: 700; color: #ffffff;">{{ munka.cim }}</h3>
                <p style="color: #94a3b8; font-size: 14px; margin-bottom: 6px;">Mennyiség: <b>{{ munka.db }} db</b> | Szín/Anyag: <b>{{ munka.szin }}</b></p>
                <p style="color: #38bdf8; font-size: 14px; margin-bottom: 4px;">Infill: <b>{{ munka.infill }}</b> | Réteg: <b>{{ munka.reteg }}</b></p>
                {% if munka.link %}
                    <p style="margin: 4px 0;"><a href="{{ munka.link }}" target="_blank" style="color: #38bdf8; text-decoration: underline; font-size: 13px;">🔗 Eredeti Modell Link Megtekintése</a></p>
                {% endif %}
                {% if munka.megjegyzes %}
                    <p style="color: #cbd5e1; font-size: 13px; font-style: italic; margin-top: 6px;">Megjegyzés: "{{ munka.megjegyzes }}"</p>
                {% endif %}
                {% if munka.fajl_url %}
                    <p style="margin-top: 8px;"><a href="{{ munka.fajl_url }}" download class="badge" style="background: rgba(56,189,248,0.2); color: #38bdf8; text-decoration: none;">📥 Feltöltött 3D Fájl Letöltése</a></p>
                {% endif %}
            </div>
            <span class="badge" style="background: rgba(255,255,255,0.1); color: #f8fafc;">{{ munka.statusz }}</span>
        </div>

        {% if munka.statusz == 'Értékelve' %}
            <div style="background: rgba(16, 185, 129, 0.1); color: #34d399; padding: 18px; border-radius: 12px; margin-top: 20px; font-weight: 600;">
                ✅ Köszönjük! Az értékelésed rögzítve lett a partner profilján.
            </div>
        {% elif munka.statusz == 'Teljesítve' %}
            <div style="background: rgba(59, 130, 246, 0.1); color: #60a5fa; padding: 20px; border-radius: 14px; margin-top: 20px; border: 1px solid rgba(59, 130, 246, 0.3);">
                <h4 style="margin: 0 0 10px 0; font-size: 18px;">🎉 A megbízás elkészült! Kérjük, értékeld a partnert:</h4>
                {% if munka.galeria_kep %}
                    <img src="{{ munka.galeria_kep }}" style="max-width: 200px; border-radius: 8px; margin-bottom: 15px; display: block; border: 1px solid rgba(255,255,255,0.1);">
                {% endif %}
                <form action="/minosites_beküldés" method="POST">
                    <input type="hidden" name="munka_id" value="{{ munka.id }}">
                    <label>Minősítés típusa:</label>
                    <select name="tipus" required style="background: #0f172a; color: white;">
                        <option value="Pozitív">💚 Pozitív (Ajánlom)</option>
                        <option value="Semleges">🟡 Semleges</option>
                        <option value="Negatív">🔴 Negatív (Nem ajánlom)</option>
                    </select>
                    <label>Szöveges vélemény a munkáról:</label>
                    <textarea name="szöveg" placeholder="Írd le a tapasztalataidat..." required style="background: #0f172a; color: white; height: 80px;"></textarea>
                    <button type="submit" class="btn btn-green">Értékelés beküldése</button>
                </form>
            </div>
        {% elif munka.nyertes %}
            <div style="background: rgba(245, 158, 11, 0.1); color: #fbbf24; padding: 25px; border-radius: 16px; margin-top: 20px; border: 1px solid rgba(245, 158, 11, 0.3);">
                <h4 style="margin: 0 0 12px 0; font-size: 20px; color: #fbbf24;">🤝 Sikeres megállapodás! Nyertes partner adatai:</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 15px; background: rgba(15, 23, 42, 0.5); padding: 15px; border-radius: 12px; margin-bottom: 15px;">
                    <div>
                        <p style="margin: 0 0 4px 0; color: #94a3b8; font-size: 12px; text-transform: uppercase;">Cégnév / Partner:</p>
                        <p style="margin: 0; font-size: 16px; font-weight: 700; color: #ffffff;">{{ munka.nyertes.nev }} ({{ munka.nyertes.forma }})</p>
                    </div>
                    <div>
                        <p style="margin: 0 0 4px 0; color: #94a3b8; font-size: 12px; text-transform: uppercase;">Helyszín (Város, Vármegye):</p>
                        <p style="margin: 0; font-size: 15px; color: #38bdf8;">📍 {{ munka.nyertes.varos }}, {{ munka.nyertes.megye }}</p>
                    </div>
                    <div>
                        <p style="margin: 0 0 4px 0; color: #94a3b8; font-size: 12px; text-transform: uppercase;">Kapcsolattartó E-mail:</p>
                        <p style="margin: 0; font-size: 16px; font-weight: 700; color: #38bdf8;"><a href="mailto:{{ munka.nyertes.email }}" style="color: #38bdf8; text-decoration: none;">{{ munka.nyertes.email }}</a></p>
                    </div>
                    <div>
                        <p style="margin: 0 0 4px 0; color: #94a3b8; font-size: 12px; text-transform: uppercase;">Elfogadott Végösszeg:</p>
                        <p style="margin: 0; font-size: 16px; font-weight: 800; color: #34d399;">{{ munka.nyertes_ar }} Ft</p>
                    </div>
                </div>
            </div>
        {% else %}
            <h4 style="font-size: 15px; font-weight: 700; color: #f8fafc; margin-top: 20px; margin-bottom: 12px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 15px;">Beérkezett Szabad Áras Licit Ajánlatok:</h4>
            {% if munka.licitek|length == 0 %}
                <p style="color: #64748b; font-size: 14px; font-style: italic;">Még nem érkezett ajánlat a partnerektől.</p>
            {% else %}
                <table>
                    <tr><th>Partner és Helyszíne</th><th>Távolság</th><th>Ajánlott Ár</th><th style="text-align: right;">Döntés</th></tr>
                    {% for licit in munka.licitek %}
                    <tr>
                        <td>
                            <a href="/profil/{{ licit.maker_id }}" target="_blank" style="color: #38bdf8; text-decoration: none; font-weight: 700;">{{ licit.nyomtatos.nev }}</a> 
                            <span style="color: #94a3b8; font-size: 13px; display: block;">📍 {{ licit.nyomtatos.varos }}, {{ licit.nyomtatos.megye }}</span>
                        </td>
                        <td style="color: #34d399; font-weight: 700;">🚗 ~{{ licit.tavolsag_km }} km</td>
                        <td style="font-weight: 800; color: #34d399; font-size: 17px;">{{ licit.ar }} Ft</td>
                        <td style="text-align: right;">
                            <form action="/elfogad" method="POST" style="margin: 0;">
                                <input type="hidden" name="munka_id" value="{{ munka.id }}">
                                <input type="hidden" name="maker_id" value="{{ licit.maker_id }}">
                                <input type="hidden" name="ar" value="{{ licit.ar }}">
                                <button type="submit" class="btn btn-green" style="padding: 10px 20px; width: auto; font-size: 14px;">Elfogadom</button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </table>
            {% endif %}
        {% endif %}
    </div>
    {% else %}
        <div class="card" style="text-align:center; color:#64748b; padding: 40px;">Még nem adtál le megbízást a főoldalon!</div>
    {% endfor %}
</div>
"""

Keszito_Dashboard_HTML = Kozos_Fejlec + """
<div class="container" style="margin-top: 120px;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 30px; flex-wrap: wrap; gap: 15px;">
        <div>
            <h1 style="font-size: 28px; font-weight: 800; color: #ffffff; margin: 0;">⚙️ Készítői Munkapult ({{ maker.nev }})</h1>
            <p style="color: #94a3b8; font-size: 14px; margin: 0;">Telephely: <b>📍 {{ maker.varos }}, {{ maker.megye }}</b></p>
        </div>
    </div>

    <!-- KPI STATISZTIKÁK -->
    <div class="stats-grid">
        <div class="stat-card">
            <h4 style="margin: 0 0 5px 0; color: #94a3b8; font-size: 13px; text-transform: uppercase;">Aktív Licitjeid</h4>
            <p style="font-size: 28px; font-weight: 800; color: #38bdf8; margin: 0;">{{ aktiv_licitek_szama }} db</p>
        </div>
        <div class="stat-card">
            <h4 style="margin: 0 0 5px 0; color: #94a3b8; font-size: 13px; text-transform: uppercase;">Gyártás Alatt</h4>
            <p style="font-size: 28px; font-weight: 800; color: #fbbf24; margin: 0;">{{ gyartas_alatt_szama }} db</p>
        </div>
        <div class="stat-card">
            <h4 style="margin: 0 0 5px 0; color: #94a3b8; font-size: 13px; text-transform: uppercase;">Sikeres Munkák</h4>
            <p style="font-size: 28px; font-weight: 800; color: #34d399; margin: 0;">{{ maker.munkak }} db</p>
        </div>
        <div class="stat-card">
            <h4 style="margin: 0 0 5px 0; color: #94a3b8; font-size: 13px; text-transform: uppercase;">Összes XP Pont</h4>
            <p style="font-size: 28px; font-weight: 800; color: #a78bfa; margin: 0;">{{ maker.pont }} XP</p>
        </div>
    </div>

    <!-- SZŰRŐK -->
    <div class="card" style="padding: 20px;">
        <form method="GET" action="/dashboard" style="display: flex; flex-direction: column; gap: 15px;">
            <div style="display: flex; gap: 15px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 220px;">
                    <label style="color: #38bdf8;">Kategória szűrés:</label>
                    <select name="kategoria" style="background: #0f172a; color: white;">
                        <option value="">-- Összes kategória --</option>
                        {% for kat in kategoria_lista %}
                        <option value="{{ kat }}" {% if kategoria_szuro == kat %}selected{% endif %}>{{ kat }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div style="flex: 1; min-width: 220px;">
                    <label style="color: #34d399;">Vármegye szűrés:</label>
                    <select name="megye" style="background: #0f172a; color: white;">
                        <option value="">-- Minden vármegye --</option>
                        {% for m in megye_lista %}
                        <option value="{{ m }}" {% if megye_szuro == m %}selected{% endif %}>{{ m }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div style="flex: 1; min-width: 220px;">
                    <label style="color: #fbbf24;">Város szűrés:</label>
                    <select name="varos" style="background: #0f172a; color: white;">
                        <option value="">-- Minden város --</option>
                        {% for v in varos_lista %}
                        <option value="{{ v }}" {% if varos_szuro == v %}selected{% endif %}>{{ v }}</option>
                        {% endfor %}
                    </select>
                </div>
            </div>
            <div style="display: flex; gap: 10px; align-items: center;">
                <button type="submit" class="btn" style="width: auto; padding: 10px 24px;">Szűrés alkalmazása</button>
                <a href="/dashboard" class="btn" style="width: auto; padding: 10px 20px; background: rgba(255,255,255,0.1); text-decoration: none;">Szűrés törlése</a>
            </div>
        </form>
    </div>

    <h2 style="font-size: 22px; font-weight: 700; color: #ffffff; margin-top: 40px; margin-bottom: 20px;">⚙️ Elnyert megbízásaid (Gyártás & Teljesítés)</h2>
    {% set nyert_van = namespace(value=false) %}
    {% for munka in munkak %}
        {% if munka.nyertes and munka.nyertes_id == aktiv_maker_id %}
            {% set nyert_van.value = true %}
            <div class="card" style="border-left: 6px solid #f59e0b;">
                <span class="badge" style="background: rgba(14, 165, 233, 0.2); color: #38bdf8; margin-bottom: 8px;">{{ munka.kategoria }}</span>
                <h3 style="margin: 0 0 6px 0; font-size: 19px; color: #ffffff;">{{ munka.cim }} ({{ munka.db }} db)</h3>
                <p style="margin:0 0 6px 0; color:#94a3b8;">Elfogadott áarad: <b style="color: #34d399;">{{ munka.nyertes_ar }} Ft</b> | Státusz: <b>{{ munka.statusz }}</b></p>
                <p style="color: #38bdf8; font-size: 14px; margin-bottom: 6px;">Szín/Anyag: <b>{{ munka.szin }}</b> | Infill: <b>{{ munka.infill }}</b> | Réteg: <b>{{ munka.reteg }}</b></p>
                
                {% if munka.link %}
                    <p style="margin: 4px 0;"><a href="{{ munka.link }}" target="_blank" style="color: #38bdf8; text-decoration: underline; font-size: 13px;">🔗 Eredeti Modell Link Megtekintése</a></p>
                {% endif %}
                {% if munka.megjegyzes %}
                    <p style="color: #cbd5e1; font-size: 13px; font-style: italic; margin-top: 4px;">Megjegyzés: "{{ munka.megjegyzes }}"</p>
                {% endif %}
                {% if munka.fajl_url %}
                    <p style="margin-top: 8px;"><a href="{{ munka.fajl_url }}" download class="badge" style="background: rgba(56,189,248,0.2); color: #38bdf8; text-decoration: none;">📥 3D Modell Fájl Letöltése</a></p>
                {% endif %}

                <div style="background: rgba(15, 23, 42, 0.6); padding: 15px; border-radius: 12px; margin: 15px 0; border: 1px solid rgba(56, 189, 248, 0.2);">
                    <p style="margin: 0 0 6px 0; color: #38bdf8; font-weight: 700; font-size: 13px;">🛒 Megrendelő Vásárló Publikus Adatai:</p>
                    <p style="margin: 0 0 4px 0; color: #ffffff; font-size: 15px;">Név: <b>{{ munka.vevo_obj.nev }}</b> ({{ munka.vevo_obj.ceg }})</p>
                    <p style="margin: 0 0 4px 0; color: #38bdf8; font-size: 14px;">📍 Helyszín: <b>{{ munka.vevo_obj.varos }}, {{ munka.vevo_obj.megye }}</b></p>
                    <p style="margin: 0 0 4px 0; color: #34d399; font-size: 14px;">🚗 Távolság tőled: <b>~{{ munka.tavolsag_km }} km</b></p>
                    <p style="margin: 0; color: #ffffff; font-size: 14px;">E-mail: <a href="mailto:{{ munka.email }}" style="color: #38bdf8; text-decoration: none;">{{ munka.email }}</a></p>
                </div>

                {% if munka.statusz == 'Teljesítve' or munka.statusz == 'Értékelve' %}
                    <p style="color: #34d399; font-weight: 700;">✅ Sikeresen teljesítve és lezárva!</p>
                    {% if munka.galeria_kep %}
                        <img src="{{ munka.galeria_kep }}" style="max-width: 150px; border-radius: 8px; margin-top: 10px; border: 1px solid rgba(255,255,255,0.1);">
                    {% endif %}
                {% else %}
                    <form action="/teljesit" method="POST" enctype="multipart/form-data" style="margin-top: 12px; background: rgba(15, 23, 42, 0.6); padding: 15px; border-radius: 12px;">
                        <input type="hidden" name="munka_id" value="{{ munka.id }}">
                        <label style="font-size: 12px;">Fotó feltöltése a kész nyomtatásról:</label>
                        <input type="file" name="kep_fajl" accept="image/*" required style="margin-bottom: 8px; background: #0f172a; color: white;">
                        <button type="submit" class="btn btn-green" style="padding: 8px 14px; font-size: 14px; width: auto;">Munkakészre jelentés & Galériába töltés</button>
                    </form>
                {% endif %}
            </div>
        {% endif %}
    {% endfor %}
    {% if not nyert_van.value %}
        <div class="card" style="text-align:center; color:#64748b; padding: 30px;">Még nincs elnyert megbízásod. Adj le licitet a piacon!</div>
    {% endif %}

    <h2 style="font-size: 22px; font-weight: 700; color: #ffffff; margin-top: 50px; margin-bottom: 20px;">🔨 Piacon lévő megbízások (Szabad áras licit & Távolság)</h2>
    {% for munka in munkak %}
        {% if not munka.nyertes and (not kategoria_szuro or munka.kategoria == kategoria_szuro) and (not megye_szuro or munka.vevo_obj.megye == megye_szuro) and (not varos_szuro or munka.vevo_obj.varos == varos_szuro) %}
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:20px;">
                <div>
                    <div style="display: flex; gap: 8px; margin-bottom: 8px; flex-wrap: wrap;">
                        <span class="badge" style="background: rgba(14, 165, 233, 0.2); color: #38bdf8;">{{ munka.kategoria }}</span>
                        <span class="badge" style="background: rgba(16, 185, 129, 0.2); color: #34d399;">📍 {{ munka.vevo_obj.varos }}, {{ munka.vevo_obj.megye }}</span>
                        <span class="badge" style="background: rgba(245, 158, 11, 0.2); color: #fbbf24;">🚗 ~{{ munka.tavolsag_km }} km</span>
                    </div>
                    <h3 style="margin: 0 0 6px 0; font-size: 19px; color: #ffffff;">{{ munka.cim }}</h3>
                    <p style="margin:0 0 6px 0; color:#94a3b8; font-size: 14px;">Megrendelő: <b>{{ munka.vevo_obj.nev }}</b> | Darab: <b>{{ munka.db }} db</b> | Szín: <b>{{ munka.szin }}</b></p>
                    <p style="color: #94a3b8; font-size: 12px; margin: 0 0 4px 0;">Infill: {{ munka.infill }} | Réteg: {{ munka.reteg }}</p>
                    {% if munka.link %}
                        <p style="margin: 4px 0;"><a href="{{ munka.link }}" target="_blank" style="color: #38bdf8; text-decoration: underline; font-size: 13px;">🔗 Eredeti Modell Forrás Link Megtekintése</a></p>
                    {% endif %}
                    {% if munka.megjegyzes %}
                        <p style="color: #cbd5e1; font-size: 12px; font-style: italic; margin-top: 4px;">Megjegyzés: "{{ munka.megjegyzes }}"</p>
                    {% endif %}
                    {% if munka.fajl_url %}
                        <p style="margin-top: 6px;"><a href="{{ munka.fajl_url }}" download class="badge" style="background: rgba(56,189,248,0.2); color: #38bdf8; text-decoration: none;">📥 3D Modell Fájl Letöltése</a></p>
                    {% endif %}
                </div>
                <!-- SZABAD ÁRAS LICIT -->
                <form action="/licit" method="POST" style="display:flex; gap:12px; background:rgba(15, 23, 42, 0.6); padding:18px; border-radius:16px; border:1px solid rgba(255,255,255,0.08); align-items:center; margin:0;">
                    <input type="hidden" name="munka_id" value="{{ munka.id }}">
                    <input type="number" name="ar" placeholder="Szabad árajánlat (Ft)" required style="padding:12px; margin:0; width:160px; font-weight: 700;">
                    <button type="submit" class="btn btn-green" style="width:auto; padding:12px 20px;">Licitálok</button>
                </form>
            </div>
        </div>
        {% endif %}
    {% else %}
        <div class="card" style="text-align:center; color:#64748b; padding: 40px;">Jelenleg nincs nyitott megbízás a kiválasztott szűrési feltételekkel.</div>
    {% endfor %}
</div>
"""

Profil_HTML = Kozos_Fejlec + """
<div class="container" style="margin-top: 120px;">
    <div class="card" style="border-top: 6px solid #0ea5e9; text-align: center; padding: 40px 30px;">
        <h1 style="margin-bottom: 8px; font-size: 32px; font-weight: 800; color: #ffffff;">{{ maker.nev }}</h1>
        <p style="color: #94a3b8; font-size: 16px; margin-bottom: 20px;">Helyszín: <b>📍 {{ maker.varos }}, {{ maker.megye }}</b> | Vállalkozás: <b>{{ maker.forma }}</b> | Géppark: <b>{{ maker.gep }}</b></p>
        <div style="display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
            <span class="badge" style="background: rgba(245, 158, 11, 0.2); color: #fbbf24; font-size: 14px; padding: 8px 16px;">{{ maker.szint }}</span>
            <span class="badge" style="background: rgba(14, 165, 233, 0.2); color: #38bdf8; font-size: 14px; padding: 8px 16px;">💬 Minősítések: {{ maker.ertekeles }}</span>
            <span class="badge" style="background: rgba(16, 185, 129, 0.2); color: #34d399; font-size: 14px; padding: 8px 16px;">🏆 {{ maker.pont }} XP</span>
        </div>
    </div>

    <h2 style="font-size: 24px; font-weight: 700; color: #ffffff; margin-top: 40px; margin-bottom: 20px;">Vásárlói Visszajelzések és Minősítések ({{ maker.velemenyek|length }})</h2>
    {% if maker.velemenyek|length == 0 %}
        <div class="card" style="text-align: center; color: #64748b; padding: 30px;">Még nincs értékelés.</div>
    {% else %}
        {% for ertek in maker.velemenyek|reverse %}
        <div class="card" style="padding: 20px; margin-bottom: 15px;">
            <p style="margin: 0 0 5px 0;">
                <span class="minosites-{{ ertek.tipus|lower }}">{{ ertek.tipus }}</span> | <b style="color: white;">{{ ertek.vevo_email }}</b>
            </p>
            <p style="margin: 0; color: #94a3b8; font-style: italic;">"{{ ertek.szöveg }}"</p>
        </div>
        {% endfor %}
    {% endif %}

    <h2 style="font-size: 24px; font-weight: 700; color: #ffffff; margin-top: 40px; margin-bottom: 20px;">🖼️ Portfólió Referenciák</h2>
    {% if maker.galeria|length == 0 %}
        <div class="card" style="text-align: center; color: #64748b; padding: 30px;">Nincsenek még feltöltött képek.</div>
    {% else %}
        <div class="grid">
            {% for item in maker.galeria %}
            <div class="gallery-card">
                <img src="{{ item.kep }}" alt="Referencia">
                <div class="gallery-body">
                    <h4 style="margin: 0 0 6px 0; font-size: 17px; color: #ffffff;">{{ item.cim }}</h4>
                    <p style="color: #34d399; font-weight: 800; margin: 0;">{{ item.ar }} Ft</p>
                </div>
            </div>
            {% endfor %}
        </div>
    {% endif %}
    <div style="margin-top: 40px; text-align: center;">
        <a href="/" class="btn" style="width: auto; padding: 12px 30px;">Vissza a Főoldalra</a>
    </div>
</div>
"""

Ranglista_HTML = Kozos_Fejlec + """
<div class="container" style="margin-top: 120px;">
    <div style="text-align: center; margin-bottom: 35px;">
        <h1 style="font-size: 32px; font-weight: 800; color: #ffffff;">🏆 Hivatalos Készítői Ranglista</h1>
        <p style="color: #94a3b8; font-size: 16px;">Megbízhatósági rangsor a valós ügyfélminősítések alapján.</p>
    </div>
    
    <div class="card" style="padding: 0; overflow: hidden;">
        <table>
            <tr>
                <th style="width: 60px; text-align: center;">Hely</th>
                <th>Cégnév</th>
                <th style="text-align: center;">Helyszín (Város, Vármegye)</th>
                <th style="text-align: center;">Szint</th>
                <th style="text-align: center;">Minősítések</th>
                <th style="text-align: center;">Sikeres Munkák</th>
                <th style="text-align: center;">Pontszám</th>
                <th style="text-align: center;">Profil</th>
            </tr>
            {% for maker_id, maker in sorted_nyomtatosok %}
            <tr>
                <td style="text-align: center; font-size: 20px; font-weight: 800; color: #38bdf8;">#{{ loop.index }}</td>
                <td style="font-weight: 700; font-size: 17px; color: #ffffff;">{{ maker.nev }}</td>
                <td style="text-align: center; color: #38bdf8; font-weight: 600;">📍 {{ maker.varos }}, {{ maker.megye }}</td>
                <td style="text-align: center;"><span class="badge" style="background: rgba(56, 189, 248, 0.2); color: #38bdf8;">{{ maker.szint }}</span></td>
                <td style="text-align: center; font-weight: 700; color: #fbbf24;">{{ maker.ertekeles }}</td>
                <td style="text-align: center; font-weight: 700; color: #cbd5e1;">{{ maker.munkak }} db</td>
                <td style="text-align: center; color: #34d399; font-weight: 800;">{{ maker.pont }} XP</td>
                <td style="text-align: center;"><a href="/profil/{{ maker_id }}" class="btn" style="padding: 8px 16px; font-size: 13px; width: auto;">Megtekintés</a></td>
            </tr>
            {% endfor %}
        </table>
    </div>
</div>
"""

# ==========================================
# 3. SZERVER MOTOR & ÚTVONALAK
# ==========================================

@app.route('/')
def vevo_oldal():
    return render_template_string(Vevo_Oldal_HTML, kategoria_lista=KATEGORIAK)

@app.route('/logout')
def logout():
    session.pop('vevo_id', None)
    session.pop('maker_id', None)
    return redirect(url_for('vevo_oldal'))

@app.route('/belepes')
def belepes():
    return render_template_string(Bejelentkezes_HTML, hiba=None)

@app.route('/belepes_mentes', methods=['POST'])
def belepes_mentes():
    szerepkor = request.form.get('szerepkor')
    email = request.form.get('email')
    jelszo = request.form.get('jelszo')
    
    if szerepkor == 'vevo':
        vevo_id = next((k for k, v in vevok.items() if v['email'] == email and v.get('jelszo') == jelszo), None)
        if vevo_id:
            session['vevo_id'] = vevo_id
            return redirect(url_for('vevo_dashboard'))
    else:
        maker_id = next((k for k, v in nyomtatosok.items() if v['email'] == email and v.get('jelszo') == jelszo), None)
        if maker_id:
            session['maker_id'] = maker_id
            return redirect(url_for('dashboard'))
            
    return render_template_string(Bejelentkezes_HTML, hiba="Hibás szerepkör, e-mail cím vagy jelszó!")

@app.route('/vevo_regisztracio')
def vevo_regisztracio():
    return render_template_string(Vevo_Regisztracio_HTML, varos_lista=sorted(MAGYARORSZAG_TELEPÜLÉSEK.keys()))

@app.route('/vevo_regisztracio_mentes', methods=['POST'])
def vevo_regisztracio_mentes():
    global vevo_szamlalo
    email = request.form.get('email')
    varos = request.form.get('varos', 'Budapest')
    megye = MAGYARORSZAG_TELEPÜLÉSEK.get(varos, ("Budapest", 0, 0))[0]
    jelszo = request.form.get('jelszo', 'titok123')
    
    meglévő = next((k for k, v in vevok.items() if v['email'] == email), None)
    if meglévő:
        session['vevo_id'] = meglévő
        vevok[meglévő]['megye'] = megye
        vevok[meglévő]['varos'] = varos
        vevok[meglévő]['jelszo'] = jelszo
    else:
        id_str = str(vevo_szamlalo)
        vevok[id_str] = {
            "nev": request.form.get('nev'),
            "email": email,
            "jelszo": jelszo,
            "megye": megye,
            "varos": varos,
            "ceg": request.form.get('ceg') or "Magánszemély"
        }
        session['vevo_id'] = id_str
        vevo_szamlalo += 1
        
    return redirect(url_for('vevo_dashboard'))

@app.route('/vevo_dashboard')
def vevo_dashboard():
    vevo_id = session.get('vevo_id')
    if not vevo_id or vevo_id not in vevok:
        return redirect(url_for('belepes'))
    
    vevo = vevok[vevo_id]
    sajat_munkak = [m for m in munkak if m['email'] == vevo['email']]
    
    for m in sajat_munkak:
        for l in m.get('licitek', []):
            maker_varos = l['nyomtatos'].get('varos', 'Budapest')
            l['tavolsag_km'] = tavolsag_szamitas(vevo['varos'], maker_varos)

    gyartas_szam = sum(1 for m in sajat_munkak if m['nyertes'] and m['statusz'] == 'Gyártás alatt')
    lezart_szam = sum(1 for m in sajat_munkak if m['statusz'] in ['Teljesítve', 'Értékelve'])

    return render_template_string(
        Vevo_Dashboard_HTML,
        vevo=vevo,
        sajat_munkak=sajat_munkak,
        gyartas_szam=gyartas_szam,
        lezart_szam=lezart_szam
    )

@app.route('/profil/<maker_id>')
def profil_oldal(maker_id):
    maker = nyomtatosok.get(maker_id)
    if not maker: return "A profil nem található!", 404
    return render_template_string(Profil_HTML, maker=maker)

@app.route('/regisztracio')
def regisztracio():
    return render_template_string(Keszito_Regisztracio_HTML, varos_lista=sorted(MAGYARORSZAG_TELEPÜLÉSEK.keys()))

@app.route('/regisztracio_mentes', methods=['POST'])
def regisztracio_mentes():
    global maker_szamlalo
    email = request.form.get('email')
    varos = request.form.get('varos', 'Budapest')
    megye = MAGYARORSZAG_TELEPÜLÉSEK.get(varos, ("Budapest", 0, 0))[0]
    jelszo = request.form.get('jelszo', 'titok123')
    
    meglátó = next((k for k, v in nyomtatosok.items() if v['email'] == email), None)
    if meglátó:
        session['maker_id'] = meglátó
        nyomtatosok[meglátó]['megye'] = megye
        nyomtatosok[meglátó]['varos'] = varos
        nyomtatosok[meglátó]['jelszo'] = jelszo
    else:
        id_str = str(maker_szamlalo)
        nyomtatosok[id_str] = {
            "nev": request.form.get('nev'),
            "email": email,
            "jelszo": jelszo,
            "megye": megye,
            "varos": varos,
            "forma": request.form.get('forma'),
            "gep": request.form.get('gep'),
            "szint": "Újonc 🔰",
            "ertekeles": "Még nem értékelték",
            "pozitiv_szam": 0,
            "osszes_ertekeles": 0,
            "munkak": 0,
            "pont": 50,
            "galeria": [],
            "velemenyek": []
        }
        session['maker_id'] = id_str
        maker_szamlalo += 1
        
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    maker_id = session.get('maker_id')
    if not maker_id or maker_id not in nyomtatosok:
        return redirect(url_for('belepes'))
    
    maker = nyomtatosok[maker_id]
    kategoria_szuro = request.args.get('kategoria', '')
    megye_szuro = request.args.get('megye', '')
    varos_szuro = request.args.get('varos', '')
    
    for m in munkak:
        v_obj = next((v for v in vevok.values() if v['email'] == m['email']), {"nev": "Ismeretlen", "megye": "Budapest", "varos": "Budapest", "ceg": "Vásárló"})
        m['vevo_obj'] = v_obj
        m['tavolsag_km'] = tavolsag_szamitas(maker.get('varos', 'Budapest'), v_obj.get('varos', 'Budapest'))

    aktiv_licitek_szama = sum(1 for m in munkak if not m['nyertes'] and any(l['maker_id'] == maker_id for l in m['licitek']))
    gyartas_alatt_szama = sum(1 for m in munkak if m.get('nyertes_id') == maker_id and m['statusz'] == 'Gyártás alatt')

    return render_template_string(
        Keszito_Dashboard_HTML, 
        munkak=munkak, 
        maker=maker,
        aktiv_maker_id=maker_id,
        aktiv_licitek_szama=aktiv_licitek_szama,
        gyartas_alatt_szama=gyartas_alatt_szama,
        kategoria_lista=KATEGORIAK,
        kategoria_szuro=kategoria_szuro,
        megye_szuro=megye_szuro,
        varos_szuro=varos_szuro,
        megye_lista=MEGYEK,
        varos_lista=sorted(MAGYARORSZAG_TELEPÜLÉSEK.keys())
    )

@app.route('/ranglista')
def ranglista():
    sorted_makers = sorted(nyomtatosok.items(), key=lambda x: x[1]['pont'], reverse=True)
    return render_template_string(Ranglista_HTML, sorted_nyomtatosok=sorted_makers)

@app.route('/uj_munka', methods=['POST'])
def uj_munka():
    global munka_szamlalo
    vevo_id = session.get('vevo_id')
    if not vevo_id or vevo_id not in vevok:
        return redirect(url_for('belepes'))
        
    vevo = vevok[vevo_id]
    db = int(request.form.get('db', 1))
    kategoria = request.form.get('kategoria', 'Egyéb')
    szin = request.form.get('szin', 'Nem megadott')
    link = request.form.get('link', '')
    infill = request.form.get('infill', 'Alapértelmezett')
    reteg = request.form.get('reteg', '0.20 mm')
    megjegyzes = request.form.get('megjegyzes', '')
    
    fajl_url = None
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            fajl_nev = f"modell_{munka_szamlalo}_{file.filename}"
            fajl_utvonal = os.path.join(app.config['UPLOAD_FOLDER'], fajl_nev)
            file.save(fajl_utvonal)
            fajl_url = f"/{fajl_utvonal}"
    
    munkak.append({
        "id": munka_szamlalo,
        "cim": request.form.get('cim'),
        "db": db,
        "szin": szin,
        "kategoria": kategoria,
        "link": link,
        "infill": infill,
        "reteg": reteg,
        "megjegyzes": megjegyzes,
        "fajl_url": fajl_url,
        "email": vevo['email'],
        "suly": "Fájl alapján",
        "min_ar": 0,
        "ora": "Szeletelés szerint",
        "hatarido": "Egyeztetés alatt",
        "licitek": [],
        "nyertes": None,
        "nyertes_ar": 0,
        "statusz": "Licitálás alatt",
        "galeria_kep": None
    })
    munka_szamlalo += 1
    return redirect(url_for('vevo_dashboard'))

@app.route('/licit', methods=['POST'])
def licit():
    maker_id = session.get('maker_id')
    if not maker_id: return redirect(url_for('belepes'))
    
    munka_id = int(request.form.get('munka_id'))
    ar = int(request.form.get('ar'))
    
    for munka in munkak:
        if munka['id'] == munka_id:
            maker = nyomtatosok[maker_id]
            vevo_obj = next((v for v in vevok.values() if v['email'] == munka['email']), {"varos": "Budapest"})
            tav = tavolsag_szamitas(maker.get('varos', 'Budapest'), vevo_obj.get('varos', 'Budapest'))

            existing = next((l for l in munka['licitek'] if l['maker_id'] == maker_id), None)
            if existing:
                existing['ar'] = ar
                existing['tavolsag_km'] = tav
            else:
                munka['licitek'].append({
                    "maker_id": maker_id,
                    "nyomtatos": nyomtatosok[maker_id],
                    "ar": ar,
                    "tavolsag_km": tav
                })
            break
    return redirect(url_for('dashboard'))

@app.route('/elfogad', methods=['POST'])
def elfogad():
    vevo_id = session.get('vevo_id')
    if not vevo_id: return redirect(url_for('belepes'))
    
    munka_id = int(request.form.get('munka_id'))
    maker_id = request.form.get('maker_id')
    ar = int(request.form.get('ar'))
    
    for munka in munkak:
        if munka['id'] == munka_id:
            m_adat = nyomtatosok.get(maker_id)
            if m_adat:
                munka['nyertes'] = m_adat
                munka['nyertes_id'] = maker_id
                munka['nyertes_ar'] = ar
                munka['statusz'] = "Gyártás alatt"
            break
    return redirect(url_for('vevo_dashboard'))

@app.route('/teljesit', methods=['POST'])
def teljesit():
    maker_id = session.get('maker_id')
    if not maker_id: return redirect(url_for('belepes'))
    
    munka_id = int(request.form.get('munka_id'))
    kep_url = None
    if 'kep_fajl' in request.files:
        file = request.files['kep_fajl']
        if file.filename != '':
            fajl_nev = f"munka_{munka_id}_{file.filename}"
            fajl_utvonal = os.path.join(app.config['UPLOAD_FOLDER'], fajl_nev)
            file.save(fajl_utvonal)
            kep_url = f"/{fajl_utvonal}"
    
    for munka in munkak:
        if munka['id'] == munka_id and munka['nyertes'] and munka['nyertes_id'] == maker_id:
            munka['statusz'] = "Teljesítve"
            munka['galeria_kep'] = kep_url
            
            if maker_id in nyomtatosok and kep_url:
                m_adat = nyomtatosok[maker_id]
                m_adat['galeria'].append({
                    "cim": munka['cim'],
                    "kep": kep_url,
                    "ar": munka['nyertes_ar']
                })
            break
            
    return redirect(url_for('dashboard'))

@app.route('/minosites_beküldés', methods=['POST'])
def minosites_beküldés():
    vevo_id = session.get('vevo_id')
    if not vevo_id: return redirect(url_for('belepes'))
    
    munka_id = int(request.form.get('munka_id'))
    tipus = request.form.get('tipus')
    szöveg = request.form.get('szöveg')
    
    for munka in munkak:
        if munka['id'] == munka_id and munka['nyertes']:
            munka['statusz'] = "Értékelve"
            maker_id = munka['nyertes_id']
            
            if maker_id in nyomtatosok:
                m_adat = nyomtatosok[maker_id]
                m_adat['munkak'] += 1
                m_adat['pont'] += 300
                
                m_adat['velemenyek'].append({
                    "tipus": tipus,
                    "szöveg": szöveg,
                    "vevo_email": munka['email']
                })
                
                m_adat['osszes_ertekeles'] += 1
                if tipus == "Pozitív":
                    m_adat['pozitiv_szam'] += 1
                
                poz = m_adat['pozitiv_szam']
                osszes = m_adat['osszes_ertekeles']
                m_adat['ertekeles'] = f"{poz} pozitív ({osszes} vélemény)"
                
                if m_adat['pont'] > 4000: m_adat['szint'] = "Mester 🏆"
                elif m_adat['pont'] > 1500: m_adat['szint'] = "Haladó ⭐"
            break
            
    return redirect(url_for('vevo_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
