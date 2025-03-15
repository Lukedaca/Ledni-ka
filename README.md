# 🥕 Lednička

Aplikace **Lednička** slouží k evidenci potravin v lednici. Umožňuje sledovat datum nákupu, minimální trvanlivost a spotřebu potravin, a upozorňuje na blížící se expiraci pomocí barevného zvýraznění.

---

## 📋 Funkce

- **Evidence potravin**: Ukládání informací o potravinách (název, datum nákupu, minimální trvanlivost, spotřeba, fotografie).
- **Výpočet poločasu spotřeby (PS)**: Automatický výpočet středu mezi datem nákupu/výroby a datem spotřeby/trvanlivosti.
- **Barevné zvýraznění**:
  - **Červená**: Potraviny, které již prošly (`end_date < now.date()`).
  - **Oranžová**: Potraviny, které se blíží expiraci (`ps_date < now.date()`).
- **Editace a mazání**: Možnost upravit nebo smazat existující záznamy.
- **Nahrávání fotografií**: Uživatelé mohou nahrát fotografie potravin.

---

## 📸 Náhled aplikace

![Náhled aplikace](https://via.placeholder.com/800x600/4CAF50/FFFFFF?text=Lednička+-+Demo)

---

## 🛠️ Použité technologie

- **Backend**: Python (Flask)
- **Databáze**: SQLite
- **Frontend**: HTML, CSS, Jinja2 (šablony)
- **Další nástroje**: SQLAlchemy (pro práci s databází), datetime (pro práci s daty)

---

## 🚀 Instalace a spuštění

1. **Stažení projektu**:
   - Stáhněte si složku s projektem (např. jako ZIP).

2. **Instalace závislostí**:
   - Otevřete terminál a nainstalujte Flask:
     ```bash
     pip install flask
     ```

3. **Spuštění aplikace**:
   - Přejděte do složky s projektem a spusťte aplikaci:
     ```bash
     python app.py
     ```

4. **Otevření v prohlížeči**:
   - Navštivte `http://localhost:5000`.

---

## 📝 Popis funkcí z obrázku

### 1. Přidání nové potraviny
- Uživatel vyplní:
  - **Název potraviny**
  - **Datum nákupu (DN)**
  - **Datum minimální trvanlivosti (DMT)**
  - **Datum výroby (DV)** (volitelné)
  - **Datum spotřeby (DS)** (volitelné)
  - **Fotografie** (volitelné)

### 2. Seznam potravin
- Tabulka zobrazuje:
  - **Název potraviny**
  - **Datum výroby (DV)**
  - **Datum nákupu (DN)**
  - **Datum minimální trvanlivosti (DMT)**
  - **Datum spotřeby (DS)**
  - **Poločas spotřeby (PS)**
  - **Fotografie**
  - **Akce** (editace/smazání)

---

## 📊 Příklad dat z obrázku

| Název     | DV         | DN         | DMT        | DS         | PS         | Foto | Akce |
|-----------|------------|------------|------------|------------|------------|------|------|
| Hranolky  | 2025-03-07 | 2025-03-10 | 2025-03-13 | 2025-03-20 | 2025-03-13 | ✔️   | ✏️🗑️ |
| Mléko     | 2025-03-09 | 2025-03-10 | 2025-03-03 | 2025-03-10 | 2025-03-09 | ✔️   | ✏️🗑️ |


Update verze


## 🚀 Novinky a opravy

- **✅ Validace dat**: Kontrola, že datum nákupu není dřívější než datum výroby.  
- **✅ Oprava zobrazování fotek**: Fotografie se nyní správně načítají ze složky `uploads`.  
- **✅ Funkční editace**: Formulář se předvyplní daty při editaci položky.  
- **✅ Moderní design**: Vzhled vylepšen pomocí Bootstrapu a Font Awesome ikon.  
- **✅ Bezpečnostní ikony**: Emoji nahrazeny profesionálními ikonami.  
