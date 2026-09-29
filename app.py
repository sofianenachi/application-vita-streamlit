import urllib.parse

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# CONFIGURATION : modifiez ces informations avec celles de votre magasin
# ---------------------------------------------------------------------------
CONFIG = {
    "nom": "Boulonnerie Pro",
    "slogan": "Boulons, tiges d'ancrage et accessoires de coffrage pour vos chantiers",
    "telephone": "+213 555 00 00 00",
    "whatsapp": "213555000000",  # format international, sans + ni espaces
    "email": "contact@exemple.dz",
    "adresse": "Oran, Algérie",
    "horaires": "Samedi - Jeudi : 08h00 - 18h00",
}

# ---------------------------------------------------------------------------
# CATALOGUE : ajoutez / modifiez vos produits ici
# ---------------------------------------------------------------------------
CATALOGUE = {
    "Boulons": {
        "icone": "🔩",
        "description": "Boulons hexagonaux, à tête ronde et à tête marteau, en acier zingué ou galvanisé.",
        "produits": [
            {
                "nom": "Boulon hexagonal TH - Acier zingué",
                "dimensions": "M8 à M24",
                "matiere": "Acier classe 8.8, zingué",
                "usage": "Assemblages métalliques, charpente légère, machines.",
            },
            {
                "nom": "Boulon hexagonal TH - Galvanisé à chaud",
                "dimensions": "M10 à M30",
                "matiere": "Acier classe 8.8, galvanisé à chaud",
                "usage": "Charpente extérieure, pylônes, milieux corrosifs.",
            },
            {
                "nom": "Boulon à tête ronde collet carré",
                "dimensions": "M6 à M16",
                "matiere": "Acier classe 4.6, zingué",
                "usage": "Assemblages bois / métal, portails, clôtures.",
            },
            {
                "nom": "Boulon à tête marteau",
                "dimensions": "M12 à M24",
                "matiere": "Acier classe 8.8",
                "usage": "Fixation dans rails et profilés à rainure.",
            },
            {
                "nom": "Boulon haute résistance HR",
                "dimensions": "M16 à M30",
                "matiere": "Acier classe 10.9",
                "usage": "Structures métalliques précontraintes.",
            },
        ],
    },
    "Tiges d'ancrage": {
        "icone": "⚓",
        "description": "Tiges d'ancrage droites, coudées ou à plaque pour fondations et poteaux métalliques.",
        "produits": [
            {
                "nom": "Tige d'ancrage droite filetée",
                "dimensions": "M12 à M36 - longueur sur demande",
                "matiere": "Acier classe 5.8 / 8.8",
                "usage": "Scellement de platines de poteaux dans le béton.",
            },
            {
                "nom": "Tige d'ancrage coudée en L",
                "dimensions": "M12 à M30",
                "matiere": "Acier classe 5.8, zingué ou brut",
                "usage": "Fondations, semelles isolées, ancrage de charpente.",
            },
            {
                "nom": "Tige d'ancrage à crosse (J)",
                "dimensions": "M12 à M30",
                "matiere": "Acier classe 5.8 / 8.8",
                "usage": "Ancrage de poteaux, machines et équipements lourds.",
            },
            {
                "nom": "Tige d'ancrage avec plaque",
                "dimensions": "M16 à M42",
                "matiere": "Acier S355 + plaque soudée",
                "usage": "Charges importantes, ponts, bâtiments industriels.",
            },
            {
                "nom": "Kit tige + écrous + rondelles",
                "dimensions": "M16 à M30",
                "matiere": "Acier galvanisé",
                "usage": "Kit complet prêt à sceller.",
            },
        ],
    },
    "Accessoires de coffrage": {
        "icone": "🏗️",
        "description": "Tout le nécessaire pour vos coffrages : tiges, écrous, cônes, entretoises et plus.",
        "produits": [
            {
                "nom": "Tige de coffrage (type DW 15 / DW 20)",
                "dimensions": "Ø 15 mm / Ø 20 mm - 1 m, 2 m, 3 m",
                "matiere": "Acier haute résistance",
                "usage": "Liaison des banches et panneaux de coffrage.",
            },
            {
                "nom": "Écrou papillon",
                "dimensions": "Ø 15 / Ø 20",
                "matiere": "Fonte malléable",
                "usage": "Serrage manuel rapide des tiges de coffrage.",
            },
            {
                "nom": "Écrou à platine (plaque d'appui)",
                "dimensions": "Ø 15 / Ø 20",
                "matiere": "Acier forgé",
                "usage": "Reprise des efforts sur les panneaux.",
            },
            {
                "nom": "Cône de coffrage",
                "dimensions": "Ø 22 / Ø 26 / Ø 32",
                "matiere": "Plastique PVC",
                "usage": "Réservation autour de la tige, finition des voiles.",
            },
            {
                "nom": "Entretoise (tube PVC)",
                "dimensions": "Ø 22 - longueur sur demande",
                "matiere": "PVC",
                "usage": "Maintien de l'épaisseur du voile béton.",
            },
            {
                "nom": "Serre-joint / clameau de coffrage",
                "dimensions": "Standard",
                "matiere": "Acier",
                "usage": "Assemblage rapide des panneaux.",
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# PAGE
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title=f"{CONFIG['nom']} - Boulons, tiges d'ancrage, coffrage",
    page_icon="🔩",
    layout="wide",
)

if "devis" not in st.session_state:
    st.session_state.devis = []  # liste de dicts : produit, categorie, quantite, precision


def ajouter_au_devis(categorie, produit, quantite, precision):
    st.session_state.devis.append(
        {
            "Catégorie": categorie,
            "Produit": produit,
            "Quantité": quantite,
            "Précision (diamètre, longueur...)": precision,
        }
    )
    st.toast(f"Ajouté à la demande de devis : {produit}", icon="✅")


# ---------------------------------------------------------------------------
# BARRE LATÉRALE
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title(f"🔩 {CONFIG['nom']}")
    page = st.radio(
        "Navigation",
        ["🏠 Accueil", "📦 Catalogue", "📝 Demande de devis", "📞 Contact"],
    )
    st.divider()
    st.caption(f"🛒 Produits dans le devis : **{len(st.session_state.devis)}**")
    st.link_button(
        "💬 WhatsApp",
        f"https://wa.me/{CONFIG['whatsapp']}",
        use_container_width=True,
    )


# ---------------------------------------------------------------------------
# PAGE : ACCUEIL
# ---------------------------------------------------------------------------
def page_accueil():
    st.title(CONFIG["nom"])
    st.subheader(CONFIG["slogan"])
    st.write(
        "Nous fournissons les professionnels du bâtiment, les entreprises de "
        "construction métallique et les particuliers : qualité contrôlée, "
        "stock permanent, livraison possible et prix compétitifs."
    )

    st.markdown("### Nos gammes")
    cols = st.columns(len(CATALOGUE))
    for col, (nom, data) in zip(cols, CATALOGUE.items()):
        with col:
            with st.container(border=True):
                st.markdown(f"## {data['icone']}")
                st.markdown(f"**{nom}**")
                st.write(data["description"])
                st.caption(f"{len(data['produits'])} références")

    st.markdown("### Pourquoi nous choisir ?")
    a, b, c, d = st.columns(4)
    a.metric("Stock", "Permanent")
    b.metric("Classes", "4.6 à 10.9")
    c.metric("Finitions", "Zingué / Galvanisé")
    d.metric("Devis", "Rapide")

    st.info(
        "💡 Vous avez une liste de besoins ? Rendez-vous dans **Demande de devis** "
        "et envoyez-la nous en un clic par WhatsApp ou e-mail."
    )


# ---------------------------------------------------------------------------
# PAGE : CATALOGUE
# ---------------------------------------------------------------------------
def page_catalogue():
    st.title("📦 Catalogue produits")
    recherche = st.text_input("🔎 Rechercher un produit (ex : M16, galvanisé, cône...)")

    onglets = st.tabs([f"{d['icone']} {nom}" for nom, d in CATALOGUE.items()])
    for onglet, (categorie, data) in zip(onglets, CATALOGUE.items()):
        with onglet:
            st.write(data["description"])
            produits = [
                p
                for p in data["produits"]
                if recherche.lower() in " ".join(p.values()).lower()
            ]
            if not produits:
                st.warning("Aucun produit ne correspond à votre recherche.")
                continue

            for i, p in enumerate(produits):
                with st.container(border=True):
                    c1, c2 = st.columns([3, 2])
                    with c1:
                        st.markdown(f"#### {p['nom']}")
                        st.markdown(f"**Dimensions :** {p['dimensions']}")
                        st.markdown(f"**Matière :** {p['matiere']}")
                        st.markdown(f"**Utilisation :** {p['usage']}")
                    with c2:
                        cle = f"{categorie}_{i}_{p['nom']}"
                        qte = st.number_input(
                            "Quantité", min_value=1, value=100, step=10, key=f"q_{cle}"
                        )
                        prec = st.text_input(
                            "Précision (ex : M16 x 300 mm)", key=f"p_{cle}"
                        )
                        st.button(
                            "➕ Ajouter au devis",
                            key=f"b_{cle}",
                            on_click=ajouter_au_devis,
                            args=(categorie, p["nom"], qte, prec),
                            use_container_width=True,
                        )


# ---------------------------------------------------------------------------
# PAGE : DEMANDE DE DEVIS
# ---------------------------------------------------------------------------
def page_devis():
    st.title("📝 Demande de devis")

    if not st.session_state.devis:
        st.info("Votre liste est vide. Ajoutez des produits depuis le **Catalogue**.")
        return

    df = pd.DataFrame(st.session_state.devis)
    st.dataframe(df, use_container_width=True, hide_index=True)

    if st.button("🗑️ Vider la liste"):
        st.session_state.devis = []
        st.rerun()

    st.markdown("### Vos coordonnées")
    c1, c2 = st.columns(2)
    nom = c1.text_input("Nom / Société")
    tel = c2.text_input("Téléphone")
    message = st.text_area("Message complémentaire (chantier, délai de livraison...)")

    lignes = [
        f"- {r['Produit']} | Qté : {r['Quantité']} | {r['Précision (diamètre, longueur...)'] or '-'}"
        for r in st.session_state.devis
    ]
    texte = (
        f"Bonjour {CONFIG['nom']},\n"
        f"Je souhaite un devis pour :\n" + "\n".join(lignes) + "\n\n"
        f"Nom : {nom or '-'}\nTéléphone : {tel or '-'}\n"
        f"Message : {message or '-'}"
    )

    st.markdown("### Envoyer la demande")
    b1, b2 = st.columns(2)
    b1.link_button(
        "💬 Envoyer par WhatsApp",
        f"https://wa.me/{CONFIG['whatsapp']}?text={urllib.parse.quote(texte)}",
        use_container_width=True,
    )
    b2.link_button(
        "✉️ Envoyer par e-mail",
        f"mailto:{CONFIG['email']}?subject={urllib.parse.quote('Demande de devis')}"
        f"&body={urllib.parse.quote(texte)}",
        use_container_width=True,
    )

    st.download_button(
        "⬇️ Télécharger la liste (CSV)",
        df.to_csv(index=False).encode("utf-8-sig"),
        file_name="demande_devis.csv",
        mime="text/csv",
    )


# ---------------------------------------------------------------------------
# PAGE : CONTACT
# ---------------------------------------------------------------------------
def page_contact():
    st.title("📞 Contact")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**📍 Adresse :** {CONFIG['adresse']}")
        st.markdown(f"**☎️ Téléphone :** {CONFIG['telephone']}")
        st.markdown(f"**✉️ E-mail :** {CONFIG['email']}")
        st.markdown(f"**🕗 Horaires :** {CONFIG['horaires']}")
    with c2:
        st.link_button(
            "💬 Nous écrire sur WhatsApp",
            f"https://wa.me/{CONFIG['whatsapp']}",
            use_container_width=True,
        )
        st.link_button(
            "📍 Voir sur Google Maps",
            f"https://www.google.com/maps/search/{urllib.parse.quote(CONFIG['adresse'])}",
            use_container_width=True,
        )


# ---------------------------------------------------------------------------
# ROUTAGE
# ---------------------------------------------------------------------------
if page == "🏠 Accueil":
    page_accueil()
elif page == "📦 Catalogue":
    page_catalogue()
elif page == "📝 Demande de devis":
    page_devis()
else:
    page_contact()

st.divider()
st.caption(f"© {CONFIG['nom']} - Tous droits réservés.")
