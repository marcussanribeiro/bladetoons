import zipfile
import xml.etree.ElementTree as ET
import tempfile
import os

from backend.model.model_anime import Anime, Volume, Capitulo, Pagina, Genero


def importar_anime_zip(file):
    """
    Estrutura esperada no ZIP:

    anime/
        info.xml
        volume_1/
            capitulo_1/
                001.webp
                002.webp
    """

    with tempfile.TemporaryDirectory() as tmp:

        # 🔥 extrai zip
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(tmp)

        base_path = os.path.join(tmp)

        # 🔥 localizar XML
        xml_path = None
        for root, dirs, files in os.walk(base_path):
            for f in files:
                if f.endswith(".xml"):
                    xml_path = os.path.join(root, f)
                    break

        if not xml_path:
            raise Exception("XML não encontrado no ZIP")

        tree = ET.parse(xml_path)
        root = tree.getroot()

        # =========================
        # 🎬 ANIME
        # =========================
        titulo = root.findtext("titulo")
        anime = Anime.objects.create(
            titulo=titulo
        )

        # gêneros
        for g in root.findall("generos/genero"):
            genero, _ = Genero.objects.get_or_create(nome=g.text)
            anime.generos.add(genero)

        # =========================
        # 📚 VOLUMES
        # =========================
        volumes_xml = root.findall("volumes/volume")

        for v in volumes_xml:
            vol_num = int(v.findtext("numero"))

            volume = Volume.objects.create(
                anime=anime,
                numero=vol_num
            )

            # =========================
            # 📖 CAPÍTULOS
            # =========================
            for c in v.findall("capitulos/capitulo"):

                cap_num = int(c.findtext("numero"))
                titulo_cap = c.findtext("titulo")

                capitulo = Capitulo.objects.create(
                    volume=volume,
                    numero=cap_num,
                    titulo=titulo_cap
                )

                # =========================
                # 🖼 PÁGINAS
                # =========================
                cap_path = c.findtext("pasta")

                cap_dir = None

                # localizar pasta real no zip extraído
                for root_dir, dirs, files in os.walk(base_path):
                    if cap_path in root_dir:
                        cap_dir = root_dir
                        break

                if cap_dir:
                    imagens = sorted([
                        f for f in os.listdir(cap_dir)
                        if f.endswith(".webp")
                    ])

                    for i, img in enumerate(imagens, start=1):
                        Pagina.objects.create(
                            capitulo=capitulo,
                            numero=i,
                            imagem=os.path.join(cap_dir, img)
                        )

        return anime