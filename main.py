import flet as ft
import json
import os
import random
import asyncio  # Nový pomocník pro plynulé asynchronní odpočítávání

# ---------------------------------------------------------------------------
# Barevná paleta hry
# ---------------------------------------------------------------------------
BARVA_POZADI_1 = "#0F172A"   # tmavě námořnická
BARVA_POZADI_2 = "#1E293B"   # o odstín světlejší
BARVA_KARTA = "#1E293B"
BARVA_KARTA_SVETLA = "#334155"
BARVA_AKCENT = "#38BDF8"     # nebeská modrá
BARVA_AKCENT_2 = "#818CF8"   # indigová
BARVA_ZLATA = "#FBBF24"
BARVA_TEXT = "#F1F5F9"
BARVA_TEXT_TLUMENA = "#94A3B8"
BARVA_ZELENA = "#22C55E"
BARVA_ORANZOVA = "#F59E0B"
BARVA_CERVENA = "#EF4444"

IKONY_TEMAT = ["📜", "🚗", "⛵", "🌅", "🥋", "🐾", "🎵", "🎨", "🧩", "🌍", "🚀", "🧠"]


def nacti_nebo_vytvor_slovnik():
    soubor_slovniku = "slova.json"

    vychozi_slovnik = {
        "1": {"nazev": "Příroda a vesmír", "slova": ["galaxie", "ekosystém", "mikroklima", "krystalizace", "fotosyntéza", "evoluce", "biosféra", "gejzír", "tektonika", "meteorolog", "tsunami", "gravitace", "eroze", "vakuum", "supernova", "kometa", "stalaktit", "fotosféra", "chlorofyl", "mutace"]},
        "2": {"nazev": "Věda a technika", "slova": ["algoritmus", "procesor", "kyberbezpečnost", "nanotechnologie", "mikrobiologie", "genetika", "server", "kryptoměna", "databáze", "inovace", "prototyp", "simulace", "frekvence", "kvantum", "spektrometr", "laser", "holografie", "robotika", "termodynamika", "izolátor"]},
        "3": {"nazev": "Umění a kultura", "slova": ["renesance", "avantgarda", "symfonie", "choreografie", "kaligrafie", "surrealismus", "monolog", "expozice", "vernisáž", "perspektiva", "abstrakce", "harmonie", "mozaika", "inspirace", "metafora", "kurátor", "partitura", "pantomima", "freska", "akustika"]},
        "4": {"nazev": "Společnost a vztahy", "slova": ["demokracie", "diplomacie", "tolerance", "kompromis", "hierarchie", "filantropie", "generace", "solidarita", "loajalita", "egoismus", "flegmatik", "empatie", "altruismus", "manipulace", "předsudek", "tradice", "komunita", "asimilace", "integrace", "neutralita"]},
        "5": {"nazev": "Cestování a geografie", "slova": ["metropole", "souřadnice", "rovnoběžka", "průplav", "navigace", "poloostrov", "kontinent", "expedice", "infrastruktura", "nomád", "destinace", "itinerář", "imigrace", "migrace", "průzkumník", "karavana", "pohraničí", "globus", "nadmořská", "topografie"]},
        "6": {"nazev": "Abstraktní pojmy", "slova": ["paradigma", "paradox", "utopie", "cynismus", "skepse", "euforie", "ironie", "kognitivní", "intuice", "synergie", "variabilita", "kontinuita", "hypotéza", "dogma", "fenomén", "dilema", "priorita", "alibi", "kontext", "melancholie"]},
        "7": {"nazev": "Lidské tělo a zdraví", "slova": ["metabolismus", "imunita", "neurologie", "anatomie", "ortopedie", "rehabilitace", "diagnóza", "prevence", "terapie", "placebo", "endorfin", "krevní", "dýchací", "lymfatický", "chirurgie", "symptom", "vakcína", "kardiolog", "hormon", "protilátka"]},
        "8": {"nazev": "Ekonomika a práce", "slova": ["investice", "inflace", "monopol", "hypotéka", "dividenda", "prosperita", "management", "marketing", "logistika", "podnikatel", "byrokracie", "konkurence", "kapitál", "rozpočet", "komodita", "korporace", "produkce", "certifikát", "auditor", "úrok"]}
    }

    try:
        if not os.path.exists(soubor_slovniku):
            with open(soubor_slovniku, 'w', encoding='utf-8') as f:
                json.dump(vychozi_slovnik, f, ensure_ascii=False, indent=4)
            return vychozi_slovnik
        else:
            with open(soubor_slovniku, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        return vychozi_slovnik


sady_slov = nacti_nebo_vytvor_slovnik()


def zjisti_rekord():
    nejvyssi = 0
    try:
        if os.path.exists("vysledky.txt"):
            with open("vysledky.txt", "r", encoding="utf-8") as f:
                for radek in f:
                    casti = radek.strip().split(" | ")
                    if len(casti) == 2:
                        body = int(casti[1])
                        if body > nejvyssi:
                            nejvyssi = body
    except Exception:
        pass
    return nejvyssi


def uloz_vysledek(tema, skore):
    try:
        with open("vysledky.txt", "a", encoding="utf-8") as f:
            f.write(f"{tema} | {skore}\n")
    except Exception:
        pass


def nacti_pouzita_slova():
    """Načte seznam už použitých slov pro každé téma (aby se neopakovala brzy)."""
    soubor = "pouzita_slova.json"
    try:
        if os.path.exists(soubor):
            with open(soubor, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def uloz_pouzita_slova(data):
    try:
        with open("pouzita_slova.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception:
        pass


pouzita_slova = nacti_pouzita_slova()


def barva_casu(cas, celkem=180):
    """Vrátí barvu pro časomíru podle zbývajícího času."""
    if cas <= 30:
        return BARVA_CERVENA
    elif cas <= 60:
        return BARVA_ORANZOVA
    return BARVA_ZELENA


# Hlavní funkce je nyní označena jako 'async'
async def main(page: ft.Page):
    page.title = "LexiGo 🐬"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed=BARVA_AKCENT)

    try:
        page.window.width = 960
        page.window.height = 740
        page.window.min_width = 760
        page.window.min_height = 600
    except AttributeError:
        page.window_width = 960
        page.window_height = 740

    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = BARVA_POZADI_1

    # Zvuk je na této webové verzi vypnutý – ovládací prvek Audio vyžaduje
    # vlastní sestavení webového klienta, které tu zatím nepoužíváme.
    zvuky_zapnuty = False

    CELKOVY_CAS = 180
    POCET_SLOV_NA_KOLO = 20

    hra = {
        "bezi": False,
        "skore": 0,
        "cas": CELKOVY_CAS,
        "slova": [],
        "tema": "",
        "cilovy_rekord": 0,
        "rekord_oslaven": False,
    }

    # ------------------------------------------------------------------
    # Prvky menu
    # ------------------------------------------------------------------
    nadpis_menu = ft.Text("LexiGo", size=56, weight="bold", color=BARVA_TEXT)
    podnadpis_menu = ft.Text("Hádej co nejvíc slov, dokud neuteče čas ⏱️",
                              size=16, color=BARVA_TEXT_TLUMENA)

    rekord_text = ft.Text(f"Rekord: {zjisti_rekord()} bodů", size=15,
                           color=BARVA_POZADI_1, weight="w600")
    rekord_chip = ft.Container(
        content=ft.Row(
            [ft.Text("🏆", size=16), rekord_text],
            spacing=8, alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=BARVA_ZLATA,
        padding=ft.Padding(18, 10, 18, 10),
        border_radius=30,
    )

    tlacitka_menu = ft.GridView(
        expand=True,
        runs_count=2,
        max_extent=340,
        child_aspect_ratio=2.4,
        spacing=14,
        run_spacing=14,
    )

    # ------------------------------------------------------------------
    # Prvky herní obrazovky
    # ------------------------------------------------------------------
    bar_cas = ft.ProgressBar(value=1.0, color=BARVA_ZELENA, bgcolor=BARVA_KARTA_SVETLA,
                              bar_height=14, border_radius=10)
    bar_cas_obal = ft.Container(
        content=bar_cas, width=760, border_radius=10,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    text_cas = ft.Text(f"⏳ {CELKOVY_CAS} s", size=22, weight="bold", color=BARVA_ZELENA)
    text_skore = ft.Text("0", size=22, weight="bold", color=BARVA_AKCENT)
    text_tema_hry = ft.Text("", size=16, color=BARVA_TEXT_TLUMENA, weight="w600")

    chip_cas = ft.Container(
        content=text_cas, bgcolor=BARVA_KARTA_SVETLA,
        padding=ft.Padding(20, 10, 20, 10), border_radius=14,
    )
    chip_skore = ft.Container(
        content=ft.Row([ft.Text("🏆", size=18), text_skore], spacing=6),
        bgcolor=BARVA_KARTA_SVETLA,
        padding=ft.Padding(20, 10, 20, 10), border_radius=14,
    )
    horni_panel = ft.Row([chip_cas, chip_skore], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=760)

    text_slovo = ft.Text("SLOVO", size=58, weight="bold", color=BARVA_TEXT, text_align=ft.TextAlign.CENTER)
    karta_slova = ft.Container(
        content=ft.Column(
            [text_tema_hry, text_slovo],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
        ),
        bgcolor=BARVA_KARTA,
        border=ft.Border.all(1, BARVA_KARTA_SVETLA),
        border_radius=24,
        padding=ft.Padding(50, 50, 50, 50),
        width=760,
        alignment=ft.Alignment.CENTER,
        shadow=ft.BoxShadow(
            spread_radius=1, blur_radius=25,
            color=ft.Colors.with_opacity(0.35, "#000000"),
            offset=ft.Offset(0, 10),
        ),
    )

    banner_rekord = ft.Container(
        content=ft.Text("🎉 Nový rekord! 🎉", size=30, weight="bold", color=BARVA_POZADI_1,
                         text_align=ft.TextAlign.CENTER),
        bgcolor=BARVA_ZLATA,
        padding=ft.Padding(34, 18, 34, 18),
        border_radius=20,
        opacity=0,
        scale=ft.Scale(0.6),
        animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        animate_scale=ft.Animation(350, ft.AnimationCurve.EASE_OUT_BACK),
        shadow=ft.BoxShadow(
            spread_radius=2, blur_radius=30,
            color=ft.Colors.with_opacity(0.5, "#000000"),
            offset=ft.Offset(0, 8),
        ),
    )
    karta_slova_s_oslavou = ft.Stack(
        controls=[karta_slova, banner_rekord],
        alignment=ft.Alignment.CENTER,
    )

    async def oslav_rekord():
        banner_rekord.opacity = 1
        banner_rekord.scale = ft.Scale(1)
        page.update()
        await asyncio.sleep(1.6)
        banner_rekord.opacity = 0
        banner_rekord.scale = ft.Scale(0.6)
        page.update()

    # ------------------------------------------------------------------
    # Obrazovky
    # ------------------------------------------------------------------
    async def ukaz_menu():
        hra["bezi"] = False
        rekord_text.value = f"Rekord: {zjisti_rekord()} bodů"
        page.controls.clear()
        page.add(
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.TOP_CENTER,
                    end=ft.Alignment.BOTTOM_CENTER,
                    colors=[BARVA_POZADI_1, BARVA_POZADI_2],
                ),
                padding=40,
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        ft.Text("🐬", size=54),
                        nadpis_menu,
                        podnadpis_menu,
                        ft.Container(height=6),
                        rekord_chip,
                        ft.Container(height=26),
                        ft.Container(content=tlacitka_menu, width=720, height=430),
                    ],
                ),
            )
        )
        page.update()

    # Odpočet nyní plynule tiká díky asynchronnímu spánku
    async def odpocet():
        while hra["bezi"] and hra["cas"] > 0:
            await asyncio.sleep(1)  # Asynchronní čekání, které nezmrazí obrazovku
            if not hra["bezi"]:
                break
            hra["cas"] -= 1

            barva = barva_casu(hra["cas"], CELKOVY_CAS)
            text_cas.value = f"⏳ {hra['cas']} s"
            text_cas.color = barva
            bar_cas.value = hra["cas"] / CELKOVY_CAS
            bar_cas.color = barva

            page.update()  # Plynulé překreslení každou vteřinu!

        if hra["cas"] <= 0 and hra["bezi"]:
            await konec_hry("Čas vypršel!")

    async def dalsi_slovo():
        if hra["slova"]:
            nove_slovo = hra["slova"].pop(0)
            text_slovo.value = nove_slovo.upper()
            page.update()
        else:
            await konec_hry("Došla vám všechna slova!")

    async def uhodnuto(e):
        if hra["bezi"]:
            hra["skore"] += 1
            text_skore.value = str(hra["skore"])

            if (not hra["rekord_oslaven"]
                    and hra["cilovy_rekord"] > 0
                    and hra["skore"] == hra["cilovy_rekord"]):
                hra["rekord_oslaven"] = True
                page.run_task(oslav_rekord)

            await dalsi_slovo()

    async def preskocit(e):
        if hra["bezi"]:
            await dalsi_slovo()

    async def konec_hry(duvod):
        # Pojistka: kolo se může pokusit ukončit jak časovač, tak dojití slov současně
        if not hra["bezi"]:
            return
        hra["bezi"] = False
        uloz_vysledek(hra["tema"], hra["skore"])

        novy_rekord = hra["skore"] > 0 and hra["skore"] >= zjisti_rekord()

        dlg = ft.AlertDialog(
            bgcolor=BARVA_KARTA,
            title=ft.Row(
                [ft.Text("🎉" if novy_rekord else "⏱️", size=26),
                 ft.Text("Konec kola!", color=BARVA_TEXT, weight="bold")],
                spacing=10,
            ),
            content=ft.Column(
                [
                    ft.Text(duvod, color=BARVA_TEXT_TLUMENA, size=15),
                    ft.Container(height=8),
                    ft.Text(f"Skóre: {hra['skore']} bodů", color=BARVA_AKCENT, size=22, weight="bold"),
                    ft.Text("🏆 Nový rekord!", color=BARVA_ZLATA, weight="bold") if novy_rekord else ft.Container(),
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton(
                    content=ft.Text("Zpět do menu", weight="bold", color=BARVA_AKCENT),
                    on_click=zavri_dialog,
                )
            ],
        )
        page.show_dialog(dlg)

    async def zavri_dialog(e):
        page.pop_dialog()
        await ukaz_menu()

    async def spustit_hru(klic):
        hra["tema"] = sady_slov[klic]["nazev"]

        vsechna_slova = sady_slov[klic]["slova"]
        jiz_pouzita = set(pouzita_slova.get(klic, []))
        nepouzita = [s for s in vsechna_slova if s not in jiz_pouzita]

        # Když už moc nepoužitých slov nezbylo, začínáme čerpat zásobu znovu od začátku
        if len(nepouzita) < min(POCET_SLOV_NA_KOLO, len(vsechna_slova)):
            jiz_pouzita = set()
            nepouzita = vsechna_slova.copy()

        pocet_k_vyberu = min(POCET_SLOV_NA_KOLO, len(nepouzita))
        vybrana_slova = random.sample(nepouzita, pocet_k_vyberu)

        jiz_pouzita.update(vybrana_slova)
        pouzita_slova[klic] = list(jiz_pouzita)
        uloz_pouzita_slova(pouzita_slova)

        hra["slova"] = vybrana_slova
        random.shuffle(hra["slova"])
        hra["skore"] = 0
        hra["cas"] = CELKOVY_CAS
        hra["bezi"] = True
        hra["cilovy_rekord"] = zjisti_rekord()
        hra["rekord_oslaven"] = False
        banner_rekord.opacity = 0
        banner_rekord.scale = ft.Scale(0.6)

        text_skore.value = "0"
        text_cas.value = f"⏳ {CELKOVY_CAS} s"
        text_cas.color = BARVA_ZELENA
        bar_cas.value = 1.0
        bar_cas.color = BARVA_ZELENA
        text_tema_hry.value = hra["tema"].upper()

        btn_uhodnuto = ft.ElevatedButton(
            content=ft.Row(
                [ft.Text("✅", size=18), ft.Text("Uhodnuto", size=16, weight="bold")],
                spacing=8, alignment=ft.MainAxisAlignment.CENTER,
            ),
            color=ft.Colors.WHITE,
            on_click=uhodnuto,
            style=ft.ButtonStyle(
                bgcolor=BARVA_ZELENA,
                padding=ft.Padding(30, 24, 30, 24),
                shape=ft.RoundedRectangleBorder(radius=14),
                elevation=6,
            ),
        )
        btn_preskocit = ft.ElevatedButton(
            content=ft.Row(
                [ft.Text("❌", size=18), ft.Text("Přeskočit", size=16, weight="bold")],
                spacing=8, alignment=ft.MainAxisAlignment.CENTER,
            ),
            color=ft.Colors.WHITE,
            on_click=preskocit,
            style=ft.ButtonStyle(
                bgcolor=BARVA_ORANZOVA,
                padding=ft.Padding(30, 24, 30, 24),
                shape=ft.RoundedRectangleBorder(radius=14),
                elevation=6,
            ),
        )

        napoveda = ft.Text("Enter = uhodnuto   ·   Mezerník = přeskočit",
                            size=13, color=BARVA_TEXT_TLUMENA)

        spodni_panel = ft.Column(
            [
                ft.Row([btn_uhodnuto, btn_preskocit], alignment=ft.MainAxisAlignment.CENTER, spacing=24),
                napoveda,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

        page.controls.clear()
        page.add(
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.Alignment.TOP_CENTER,
                    end=ft.Alignment.BOTTOM_CENTER,
                    colors=[BARVA_POZADI_1, BARVA_POZADI_2],
                ),
                padding=40,
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=34,
                    controls=[
                        ft.Column([bar_cas_obal, horni_panel], spacing=16,
                                  horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        karta_slova_s_oslavou,
                        spodni_panel,
                    ],
                ),
            )
        )
        await dalsi_slovo()

        # Bezpečné spuštění odpočtu na pozadí pomocí Flet asistenta
        page.run_task(odpocet)

    # Pomocná funkce pro bezpečné předání kliknutí v asynchronním režimu
    def vytvor_klik_handler(klic):
        async def handler(e):
            await spustit_hru(klic)
        return handler

    for i, (klic, data) in enumerate(sady_slov.items()):
        ikona = IKONY_TEMAT[i % len(IKONY_TEMAT)]
        pocet_slov = len(data["slova"])
        tlacitko = ft.Container(
            content=ft.Row(
                [
                    ft.Text(ikona, size=26),
                    ft.Column(
                        [
                            ft.Text(data["nazev"], size=16, weight="bold", color=BARVA_TEXT,
                                     max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                            ft.Text(f"{pocet_slov} slov", size=12, color=BARVA_TEXT_TLUMENA),
                        ],
                        spacing=2, tight=True, expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                spacing=14, alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=BARVA_KARTA,
            border=ft.Border.all(1, BARVA_KARTA_SVETLA),
            border_radius=16,
            padding=ft.Padding(18, 14, 18, 14),
            ink=True,
            on_click=vytvor_klik_handler(klic),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        )
        tlacitka_menu.controls.append(tlacitko)

    async def on_keyboard(e: ft.KeyboardEvent):
        if hra["bezi"]:
            if e.key == "Enter":
                await uhodnuto(None)
            elif e.key == " ":
                await preskocit(None)

    page.on_keyboard_event = on_keyboard
    await ukaz_menu()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8550))
    ft.run(main, host="0.0.0.0", port=port)
