"""
Module pour manipuler les cartes Compact Flash (disques) qui comportent des fichiers de pistes d'enregistrements sonores effectués sur les Nagra Ares-C Ares-B et RCX220
Auteur: Claude Eldet (eldet@wanadoo.fr) Version 1.0 Janvier 2026.
"""

import platform
import subprocess
import xmltodict
import datetime

# Constantes
SECTOR = 512
SEEK = SECTOR * 12
RESERVE = SECTOR * 16
BUFFER = SECTOR
FORMAT_NFS = 24830
HEAD = 96
MARQUE = "NAGRA"
MACHINE = [0, 0, 0, 0, 78, 65, 71, 82, 65, 0, 0, 0, 195, 11, 34, 43]
VERS = "1.0"
BANNER = "#909090"
SCREEN = "#DFE8BE"
BUTTON = "#CCCCCC"
CAUTION = "#F9B0B0"
COLOR = {"A": "#CCCCCC", "B": "#ADADAD"}
NAMESEGT = "segtAudio.mp2"
LANG = {
    "title": {
        "FR": "Format NAGRA File System",
        "UK": "Format NAGRA File System",
    },
    "sector_err": {
        "FR": "Tentative d'écrire des données qui ne sont pas un multiple de 512 octets",
        "UK": "Attempting to write data that is not a multiple of 512 bytes",
    },
    "format_tit": {
        "FR": "Lecture carte CF impossible",
        "UK": "CF card reading impossible",
    },
    "format_cont": {
        "FR": "Nagra File system absent, voulez-vous formater cette carte?",
        "UK": "Nagra File system is missing, do you want to format this card?",
    },
    "format_sta": {
        "FR": "FORMAT PAR ADMINNFS V." + VERS,
        "UK": "FORMAT BY ADMINNFS V." + VERS,
    },
    "physicDisk": {
        "FR": "AFFICHER DISQUES PHYSIQUES ACCESSIBLES",
        "UK": "SHOW ACCESSIBLE PHYSICAL DISCS",
    },
    "endDisk": {
        "FR": "Fin du disque atteinte",
        "UK": "End of disc reached",
    },
    "examDisk_tit": {"FR": "Disques amovibles", "UK": "Removables Drives"},
    "examDisk_cont": {
        "FR": "Disques amovibles inacessibles ou lancer en mode administrateur",
        "UK": "Inaccessible removable drives or launch in administrator mode",
    },
    "doubleClic": {
        "FR": "Double-cliquer sur un disque",
        "UK": "Double-click on a disk",
    },
    "select_err": {"FR": "Défaut de sélection", "UK": "Selection error"},
    "edit_tit": {"FR": "Modifier le titre >", "UK": "Edit title >"},
    "open_track": {"FR": "Ouvrir fichier de prise de son", "UK": "Open Sound Track"},
    "open_NFS": {
        "FR": "Ouvrir piste formatée en Nagra File System (NFS)",
        "UK": "Open Sound Track Nagra File System (NFS)",
    },
    "too_big": {
        "FR": "Fichier trop grand pour la capacité du disque",
        "UK": "File too large for disk capacity",
    },
    "import_ok": {
        "FR": "Fichier importé avec succès",
        "UK": "File imported successfully",
    },
    "export_ok": {
        "FR": "Fichier exporté avec succès",
        "UK": "File exported successfully",
    },
    "export_no": {"FR": "Export du fichier impossible", "UK": "File export failed"},
    "import_no": {
        "FR": "Fichier impossible à importer",
        "UK": "File could not be imported",
    },
    "export_mp3": {"FR": "Exporter en MP3 >", "UK": "Export to MP3 >"},
    "day_head": {
        "FR": "Le mois ne peut avoir plus de 31 jours!",
        "UK": "A month cannot have more than 31 days!",
    },
    "month_head": {
        "FR": "L'année ne peut avoir plus de 12 mois!",
        "UK": "A year cannot have more than 12 months!",
    },
    "hour_head": {
        "FR": "La journée ne peut avoir plus de 24 heures!",
        "UK": "A day cannot have more than 24 hours!",
    },
    "minute_head": {
        "FR": "L'heure ne peut avoir plus de 59 minutes!",
        "UK": "The hour cannot be longer than 59 minutes!",
    },
    "details_track": {"FR": "Détails de la prise de son >", "UK": "Details of track >"},
    "import_track": {"FR": "Importer piste Audio >", "UK": "Import Audio track >"},
    "sizeFrame_no": {
        "FR": "Impossible de trouver la taille de la trame audio",
        "UK": "Unable to find the audio frame size",
    },
    "frameHeader_no": {"FR": "Aucune trame audio connue", "UK": "No known audio track"},
    "track": {"FR": "Piste ", "UK": "Track "},
    "add_track": {"FR": "Ajouter une piste NFS >", "UK": "Add a track NFS >"},
    "title_track": {"FR": "Titre de la prise de son", "UK": "Track title"},
    "edit_head": {"FR": "Modifier en-tête de la prise >", "UK": "Edit Track Header >"},
    "day_track": {"FR": "dd mm yy", "UK": "dd mm yy"},
    "time_track": {"FR": "hh mm", "UK": "hh mm"},
    "duration_track": {"FR": "dur ", "UK": "dur "},
    "exportNFS_track": {"FR": "Exporter en NFS >", "UK": "Export via NFS >"},
    "analysis_track": {"FR": "< Analyse de la piste", "UK": "< Track Analysis"},
    "gapOK_track": {
        "FR": "- aucun octet inutile avant la piste audio",
        "UK": "- no unnecessary bytes before the audio track",
    },
    "gapNO_track": {
        "FR": "- trop d'octets inutiles avant la piste audio",
        "UK": "- too many unnecessary bytes before the audio track",
    },
    "remainOK_track": {
        "FR": "- aucun octet inutile après la piste audio",
        "UK": "- no unnecessary bytes after the audio track",
    },
    "remainNO_track": {
        "FR": "- trop d'octets inutiles après la piste audio",
        "UK": "- too many unnecessary bytes after the audio track",
    },
    "octets_bytes": {"FR": "octets", "UK": "bytes"},
    "sizeOK_track": {"FR": "- taille de la piste audio ", "UK": "- audio track size "},
    "sizeNO_track": {
        "FR": "- correction taille de la piste audio ",
        "UK": "- correction audio track ",
    },
    "durOK_track": {
        "FR": "- durée de la piste audio ",
        "UK": "- Audio track duration ",
    },
    "durNO_track": {
        "FR": "- correction durée piste audio ",
        "UK": "- correction audio track duration ",
    },
    "shorten_track": {
        "FR": "Un trop grand nombre d'octets après la dernière trame audio sont inutiles, la piste a été scindée",
        "UK": "Too many bytes after the last audio frame are unnecessary; the track has been split.",
    },
    "checkOK_track": {"FR": "Piste audio CONFORME", "UK": "Audio track CONFORMS"},
    "checkNO_track": {
        "FR": "Piste audio NON CONFORME",
        "UK": "NON-COMPLIANT audio track",
    },
    "cut_track": {
        "FR": "Voulez-vous couper cette piste audio trop longue?",
        "UK": "Do you want to cut this audio track that's too long?",
    },
    "gap_track": {
        "FR": "Cette piste présente un décalage entre l'entête et la piste audio, il est conseillé de faire un export avant montage",
        "UK": "This track has a misalignment between the header and the audio track; it is recommended to export it before editing.",
    },
    "remain_track": {"FR": "RELIQUAT PISTE AUDIO", "UK": "REMAINDER AUDIO TRACK"},
    "number_frame": {"FR": " trames audio trouvées", "UK": " audio frames found"},
    "cursor_cut": {"FR": "Couper au droit du curseur", "UK": "Cut at the cursor"},
    "save_cut": {"FR": "< Annuler coupure de piste", "UK": "< Cancel the track cut"},
    "no_audio": {
        "FR": "La piste ne contient aucune trame MPEG audio",
        "UK": "The track contains no MPEG audio streams",
    },
    "no_mpeg": {"FR": "Trame audio non MPEG", "UK": "Non-MPEG audio stream"},
    "erase_track": {
        "FR": "Effacer piste et suivantes >",
        "UK": "Clear track and following >",
    },
    "cancel_erase": {"FR": "Annuler effacement piste", "UK": "Cancel track deletion"},
    "recovery_track": {
        "FR": "Récupération piste au-delà",
        "UK": "Track recovery beyond",
    },
    "track_recovered": {"FR": "PISTE RECUPEREE", "UK": "TRACK RECOVERED"},
    "assembly_track": {"FR": "PISTE DE MONTAGE", "UK": "ASSEMBLY TRACK"},
    "assembly_set": {"FR": "Faire un montage", "UK": "Make assembly"},
    "copy_toA": {"FR": "< Copier piste vers A", "UK": "< Copy track to A"},
    "copy_toB": {"FR": "Copier piste vers B >", "UK": "Copy track to B >"},
    "listen": {"FR": "|►| Ecouter", "UK": "|►| Play"},
    "segment_set": {"FR": "Faire un montage >", "UK": "Edit audio segment >"},
    "segment_in": {"FR": "IN", "UK": "IN"},
    "segment_out": {"FR": "OUT", "UK": "OUT"},
    "segment_add": {"FR": "ajouter segment audio", "UK": "add audio segment"},
    "segment_del": {"FR": "effacer dernier segment", "UK": "delete last audio segment"},
    "segment_add_no": {
        "FR": "Ajout de cette piste impossible en raion de son format différent.",
        "UK": "Adding this track is not possible due to its different format.",
    },
    "listen_point": {"FR": " durée (secondes): ", "UK": " duration (seconds): "},
    "duration_point": {
        "FR": " durée écoute (secondes): ",
        "UK": " duration play (seconds): ",
    },
    "quit": {"FR": "QUITTER", "UK": "QUIT"},
    "listen_no": {
        "FR": "Ecoute impossible, c'est une piste de montage",
        "UK": "Listen, impossible, it's an editing track",
    },
}
FORMAT_AUDIO = {
    24704: ["  G711-a", 0, 0, 0, 0, "n"],
    24705: ["xG711-a", 0, 0, 0, 0, "na"],
    24708: ["  G711-mu", 0, 0, 0, 0, "n"],
    24709: ["xG711-mu", 0, 0, 0, 0, "na"],
    24712: ["  G722", 0, 0, 0, 0, "n"],
    24713: ["xG722", 0, 0, 0, 0, "na"],
    24748: ["  MPEG 64/16 m", 576, 72, 62719, 49288, "m"],
    24749: ["xMPEG 64/16 m", 0, 0, 0, 0, "ma"],
    24740: ["  MPEG 64/24 m", 384, 48, 62719, 49284, "m"],
    24741: ["xMPEG 64/24", 0, 0, 0, 0, "ma"],
    24744: ["  MPEG 64/32 m", 288, 36, 64767, 49224, "m"],
    24745: ["xMPEG 64/32", 0, 0, 0, 0, "ma"],
    24736: ["  MPEG 64/48 m", 192, 24, 64767, 49220, "m"],
    24737: ["xMPEG 64/48", 0, 0, 0, 0, "ma"],
    24764: ["  MPEG 128/16 m", 1152, 72, 62719, 49352, "m"],
    24765: ["xMPEG 128/16 m", 0, 0, 0, 0, "ma"],
    24756: ["  MPEG 128/24 m", 768, 48, 62719, 49348, "m"],
    24757: ["xMPEG 128/24 m", 0, 0, 0, 0, "ma"],
    24760: ["  MPEG 128/32 m", 576, 36, 64767, 49288, "m"],
    24761: ["xMPEG 128/32 m", 0, 0, 0, 0, "ma"],
    24752: ["  MPEG 128/48 m", 384, 24, 64767, 49284, "m"],
    24753: ["xMPEG 128/48 m", 0, 0, 0, 0, "ma"],
    24766: ["  MPEG 128/16 st", 1152, 72, 62719, 200, "m"],
    24767: ["xMPEG 128/16 st", 0, 0, 0, 0, "ma"],
    24758: ["  MPEG 128/24 st", 768, 36, 62719, 196, "m"],
    24759: ["xMPEG 128/24 st", 0, 0, 0, 0, "ma"],
    24762: ["  MPEG 128/32 st", 576, 24, 64767, 136, "m"],
    24763: ["xMPEG 128/32 st", 0, 0, 0, 0, "ma"],
    24754: ["  MPEG 128/48 st", 384, 36, 64767, 132, "m"],
    24755: ["xMPEG 128/48 st", 0, 0, 0, 0, "ma"],
    24776: ["  MPEG 192/32 m", 864, 36, 64767, 49320, "m"],
    24777: ["xMPEG 192/32 m", 0, 0, 0, 0, "ma"],
    24768: ["  MPEG 192/48 m", 576, 24, 64767, 49316, "m"],
    24769: ["xMPEG 192/48 m", 0, 0, 0, 0, "ma"],
    24778: ["  MPEG 192/32 st", 864, 24, 64767, 168, "m"],
    24779: ["xMPEG 192/32 st", 0, 0, 0, 0, "ma"],
    24770: ["  MPEG 192/48 st", 576, 24, 64767, 164, "m"],
    24771: ["xMPEG 192/48 st", 0, 0, 0, 0, "ma"],
    65535: ["  END", 0, 0, 0, 0, "e"],
}
MPEG1L2 = {
    0: [65535, "MPEG1 L2 end of track"],
    1: [64767, "MPEG1 L2 (with protect)"],
    2: [65023, "MPEG1 L2 (without protect)"],
    3: [62719, "MPEG2 L2 (with protect)"],
    3: [62975, "MPEG2 L2 (without protect)"],
}
MPEG = {
    1: "MPEG",
}
FILTER = {0: 65279, 1: 49404}
VERSION = {
    0: "version 2.5",
    1: "reserved",
    2: "version 2",
    3: "version 1",
}
LAYER = {
    0: "reserved",
    1: "layer 3",
    2: "layer 2",
    3: "layer 1",
}
PROTECT = {
    0: "protected",
    1: "not protected",
}
BITRATE_V1 = {
    0: "Free",
    1: "32 Kbit/s",
    2: "48 Kbit/s",
    3: "56 Kbit/s",
    4: "64 Kbit/s",
    5: "80 Kbit/s",
    6: "96 Kbit/s",
    7: "112 Kbit/s",
    8: "128 Kbit/s",
    9: "160 Kbit/s",
    10: "192 Kbit/s",
    11: "224 Kbit/s",
    12: "256 Kbit/s",
    13: "320 Kbit/s",
    14: "384 Kbit/s",
    15: "Error",
}
BITRATE_V2 = {
    0: "Free",
    1: "8 Kbit/s",
    2: "16 Kbit/s",
    3: "24 Kbit/s",
    4: "32 Kbit/s",
    5: "40 Kbit/s",
    6: "48 Kbit/s",
    7: "56 Kbit/s",
    8: "64 Kbit/s",
    9: "80 Kbit/s",
    10: "96 Kbit/s",
    11: "112 Kbit/s",
    12: "128 Kbit/s",
    13: "144 Kbit/s",
    14: "160 Kbit/s",
    15: "Error",
}
FREQUENCY_V1 = {
    0: "44.1 KHz",
    1: "48 KHz",
    2: "32 KHz",
    3: "None",
}
FREQUENCY_V2 = {
    0: "22.05 KHz",
    1: "24 KHz",
    2: "16 KHz",
    3: "None",
}
CHANNEL = {
    0: "Stereo",
    1: "Join stereo",
    2: "Dual mono",
    3: "Mono",
}
COPYRIGHT = {
    0: "no copyright",
    1: "copyright",
}
ORIGINAL = {
    0: "copy of media",
    1: "original media",
}


class Disk:
    """Classe qui manage les informations sur les disques physiques amovibles avec le format Nagra File System"""

    # Plateforme Operating System
    platfrm: str = ""
    # Liste de tous les disques amovibles accessibles
    listDisk: list = []
    # Affichage du disque en cours
    view: str = "A"
    # Langue de l'interface
    lang: str = "FR"

    def __init__(self, lettre):
        # lettre du disque choisi
        self.lettre: str = lettre
        # chemin physique pour accéder au disque choisi
        self.chemin: str = ""
        # index dans la liste du disque choisi
        self.indDisk: int = -1
        # taille du disque physique choisi
        self.sizeDisk: int = 0
        # adresse prochaine adresse sur le disque
        self.nextAddr: int = 0
        # suite d'octets du premier secteur du disque
        self.data_1: int = []
        # titre du disque choisi
        self.title_1: int = ""
        # date et heure du formatage du disque choisi
        self.stamp1: int = ""
        # liste des adresses et des détails des prises de son du disque en cours
        self.listTrack: dict = {}
        # index dans la liste du disque choisi
        self.indTrack: int = -1
        # valeur du curseur de lecture de piste
        self.cursorTrack: float = 0
        # valeur du curseur de durée de lecture de piste
        self.cursorSegment: float = 0
        # un montage est en cours et index de la piste de montage
        self.assembly = False
        self.indAssembly = -1
        # liste des segments d'assemblage
        self.listAssembly = []
        # mode de lecture à partir du curseur
        self.outPlay = False

    def findDisk():
        """construit la liste des disques disponibles avec leur chemin physique que se soit sur Windows ou sur Linux, vous devez avoir les droits administrateur pour exécuter cette méthode

        Returns:
            liste des disques avec leur nom, capacité et chemin
        """
        collectDisk = []
        Disk.platfrm = platform.system()
        try:
            if Disk.platfrm == "Linux":
                # lecture des disques amovibles sous linux
                presult = subprocess.run(
                    "lshw -C disk -xml", shell=True, capture_output=True, text=True
                )
                liste = xmltodict.parse(presult.stdout)
                for item in liste["list"]["node"]:
                    description = item["description"]
                    if description == "SCSI Disk":
                        capability = item["capabilities"]["capability"]
                        if capability["@id"] == "removable":
                            product = item["product"]
                            vendor = item["vendor"]
                            logicalname = item["logicalname"]
                            if "size" in item.keys():
                                size = item["size"]["#text"]
                                collectDisk.append(
                                    [vendor + " " + product, size, logicalname]
                                )

            elif Disk.platfrm == "Windows":
                import wmi
                import struct
                import win32file  # pip install pywin32
                import winioctlcon  # pip install pywin32

                c = wmi.WMI().Win32_DiskDrive(MediaType="Removable Media")
                for d in c:
                    f = win32file.CreateFile(
                        d.DeviceID,
                        win32file.GENERIC_READ,
                        0,
                        None,
                        win32file.OPEN_EXISTING,
                        win32file.FILE_ATTRIBUTE_NORMAL,
                        0,
                    )
                    size = win32file.DeviceIoControl(
                        f, winioctlcon.IOCTL_DISK_GET_LENGTH_INFO, None, 512, None
                    )  # returns bytes
                    size = struct.unpack("q", size)[
                        0
                    ]  # convert 64 bit int from bytes to int -> first element of returned tuple
                    collectDisk.append([d.Caption, str(size), d.DeviceID])
            if len(collectDisk) > 0:
                Disk.listDisk = collectDisk
                return True
            else:
                return False
        except:
            return False

    def findTrack(self):
        """findTrack construit la liste des pistes audio et pistes de montage contenues sur le disque physique avec un formatage Nagra File System

        Returns:
            True pour liste terminée, False pour liste absente
        """
        try:
            tracks = {}
            track = True
            index = 0
            self.nextAddr = 0
            while track:
                oldAddr = self.nextAddr
                data, code, long, nbBytes, stamp, durTrack = self.readHead(
                    self.nextAddr
                )
                if code in FORMAT_AUDIO.keys() and code != MPEG1L2[0][0]:
                    format = FORMAT_AUDIO[code][0]
                    title = Disk.decText("title", data)
                    tracks[index] = [
                        oldAddr,
                        code,
                        long,
                        format,
                        stamp,
                        title,
                        nbBytes,
                        durTrack,
                    ]
                    index += 1
                elif code == MPEG1L2[0][0]:
                    tracks[index] = [oldAddr, code]
                    track = False
            self.listTrack = tracks
            return True
        except Exception as err:
            print(
                err,
                "index track: ",
                index,
                "patch address: ",
                tracks[index - 1][0] + tracks[index - 1][2],
            )
            print(tracks[index - 1])
            return False

    def readHex(self, begin, long):
        """readHex lit une suite d'octets sur le disque physique

        Args:
            deb: numéro de l'octet du début de la lecture (deb)
            long: longueur en nombre d'octets à lire (long)

        Returns:
            tableau des octets lus (data)
        """
        with open(self.chemin, "rb", buffering=BUFFER) as fb:
            fb.seek(begin)
            data = bytearray(fb.read(long))
        fb.close()
        return data

    def writHex(self, begin, data):
        """writHex écrit sur disque par secteur des données présentées en liste qui vont être converties en bytearray

        Args:
            deb: adresse physique (numéro d'octet) début de l'écriture
            data: données sous forme de tableau bytearray à écrire

        Returns:
            valeur booléenne du résultat de l'écriture
        """
        long = len(data)
        if (long % SECTOR) != 0:
            print(LANG["sector_err"][Disk.lang])
            return False
        else:
            self.begin = begin
            with open(self.chemin, "rb+") as fb:
                fb.seek(self.begin)
                datarray = bytearray(data)
                fb.write(datarray)
            fb.close()
            return True

    def writeToAB(self, data):
        """writeToAB permet de copier la piste audio de l'onglet A vers l'onglet B et vice-versa

        Args:
            data: octets formatés de la piste audio, dans le cas d'une piste de montage, le montage est d'abord réalisé pour copier la piste montée.

        Returns:
            True si la copie a été réalisée, False dans le cas contraire
        """
        if self.chemin == "":
            return False
        if (
            self.listTrack[len(self.listTrack) - 1][0] + len(data) + (16 * SECTOR)
            > self.sizeDisk
        ):
            return False
        if len(data) <= SECTOR:
            return False
        begin = self.listTrack[len(self.listTrack) - 1][0]
        status = self.writHex(begin, data)
        self.indTrack = len(self.listTrack) - 1
        dataEnd = self.readHex(begin + len(data), SECTOR)
        dataEnd = Disk.replace(dataEnd, 0, [255] * HEAD)
        self.writHex(begin + len(data), dataEnd)
        return status

    def decText(type, data):
        """decText décode le texte d'une suite d'octets sous forme de liste, les octets qui ont pour valeur 'ff' sont éliminés du décodage.

        Args:
            data: suite d'octets sous forme de liste

        Returns:
            texte décodé
        """
        chaine = ""
        if type == "title":
            deb = 64
            long = 31
        elif type == "brand":
            deb = 20
            long = 5
        else:
            print("The text decoding type is not recognized")
            return chaine
        for i in range(long):
            if data[i + deb] != 255:
                chaine += chr(data[i + deb])
        return chaine

    def codText(txt):
        """codText code un texte après l'avoir transformé en lettres majuscules et limité en longueur à 31 caractères. Le codage est fait sur 32 octets qui sont initialement remplis de 'ff'.

        Args:
            txt: texte

        Returns:
            liste des codes représentant les codes ascii du texte formaté
        """
        data = [255] * 32
        nT = txt.upper().encode("ascii", "replace")[0:31]
        ind = 0
        for c in nT:
            data[ind] = c
            ind += 1
        return data

    def decNbBytes(data):
        """decNbOct décode une suite d'octets pour en faire un nombre

        Args:
            data: suite d'octets sous forme de liste

        Returns:
            nombre résultat du décodage
        """
        val = 0
        for i in range(len(data)):
            val += 256**i * data[i]
        return val

    def codNbBytes(val, nbOct):
        codVal = []
        for i in range(nbOct):
            codVal.append(val % 256)
            val = val // 256
        return codVal

    def decStamp(data):
        """decStamp décode la date et l'heure d'un timbre d'un formattage ou d'une prise de son
        Attention ces octets représentent des valeurs décimales bien qu'ils soient enregistrés en hexadécimal

        Args:
            data: suite d'octets qui représentent la date et l'heure

        Returns:
            _texte formaté de la date et de l'heure
        """
        day = Disk.hexInt(data[13])
        month = Disk.hexInt(data[14])
        year = Disk.hexInt(data[15])
        hour = Disk.hexInt(data[12])
        minute = Disk.hexInt(data[11])
        # second = Disk.hexInt(data[10])
        return day, month, year, hour, minute

    def readHead(self, address):
        """readHead lit le code de l'entête de disque ou de la piste audio et l'adresse de la prochaine piste audio dans un seul secteur dont l'adresse est donnée.

        Args:
            address: du secteur à examiner (en nombre d'octets)

        Returns:
            les données hexadécimales du secteur lu ainsi que la prochaine adresse de piste audio
        """
        data = self.readHex(address, SECTOR)
        code = Disk.decNbBytes(data[0:2])
        long = Disk.decNbBytes(data[2:6])
        nbBytes = Disk.decNbBytes(data[6:10])
        stamp = Disk.decStamp(data)
        durTrack = Disk.decNbBytes(data[16:20])
        self.nextAddr = long + address
        return data, code, long, nbBytes, stamp, durTrack

    def readSaveCut(self, index):
        data = self.readHex(0, SECTOR)
        indCutTrack = Disk.decNbBytes(data[400:402])
        if index == indCutTrack - 1:
            return True
        else:
            return False

    def readFormat(self):
        """readFormat permet de reconnaitre sur le disque la présence d'un format Nagra File System (NFS), il trouve aussi l'adresse en octets de la prochaine occurence de piste sonore.

        Returns:
            Valeur booléenne de la présence du format le premier secteur est enregistré en attribut de l'instance
        """
        data, code, long, nbBytes, stamp, durTrack = self.readHead(0)
        self.data_1 = data
        brand = Disk.decText("brand", self.data_1)
        if code == FORMAT_NFS and brand == MARQUE:
            D, M, Y, h, m = stamp
            self.stamp1 = "{:02d}-{:02d}-{:02d} {:02d}:{:02d}".format(D, M, Y, h, m)
            self.title_1 = Disk.decText("title", self.data_1)
            return True
        else:
            self.stamp1 = ""
            self.title_1 = ""
            self.nextAddr = 0
            return False

    def intHex(nb):
        """intHex convertit un entier decimal vers un hexadecimal sans changer les chiffres

        Args:
            nb: entier decimal

        Returns:
            entier hexadecimal
        """
        diz = int(nb / 10)
        unit = nb % 10
        hexa = diz * 16 + unit
        return hexa

    def hexInt(nb):
        """hexInt convertit un entier hexadecimal en entier decimal sans changer les chiffres

        Args:
            nb: entier hexadecimal

        Returns:
            entier decimal
        """
        diz = int(nb / 16)
        unit = nb % 16
        ent = diz * 10 + unit
        return ent

    def codStamp(smhDMY):
        """codStamp crée une liste de nombres hexadécimaux dont les chiffres reflètent les nombres décimaux de la date et de l'heure
        par exemple 15(j) 4(m) 25(y) est converti en [21,04,37]

        Args:
            dt: 'now' convertit la date et l'heure courante
            dt: 'ssmmhhDDMMYY' convertit les secondes, minutes, heures, jour, mois et millésime

        Returns:
            Liste des nombres hexadécimaux représentant la date et l'heure
        """
        chrono = []
        if len(smhDMY) == 12:
            chrono.append(Disk.intHex(int(smhDMY[0, 2])))
            chrono.append(Disk.intHex(int(smhDMY[2, 4])))
            chrono.append(Disk.intHex(int(smhDMY[4, 6])))
            chrono.append(Disk.intHex(int(smhDMY[6, 8])))
            chrono.append(Disk.intHex(int(smhDMY[8, 10])))
            chrono.append(Disk.intHex(int(smhDMY[10, 12])))
        elif smhDMY == "now":
            dat = datetime.datetime.now()
            chrono.append(Disk.intHex(dat.second))
            chrono.append(Disk.intHex(dat.minute))
            chrono.append(Disk.intHex(dat.hour))
            chrono.append(Disk.intHex(dat.day))
            chrono.append(Disk.intHex(dat.month))
            chrono.append(Disk.intHex(dat.year - 2000))
        elif smhDMY == "NOW":
            dat = datetime.datetime.now()
            chrono.append(Disk.intHex(dat.minute))
            chrono.append(Disk.intHex(dat.hour))
            chrono.append(Disk.intHex(dat.day))
            chrono.append(Disk.intHex(dat.month))
            chrono.append(Disk.intHex(dat.year - 2000))
        return chrono

    def replace(data, pos, ndata):
        """remplace permet de remplacer une partie des octets d'un tableau d'octets

        Args:
            data: tableau d'octets initial
            pos: position en octet du début du remplacement
            ndata: nouveau tableau d'octets

        Returns:
            _dtableau d'octets modifié
        """
        if len(data) >= pos + len(ndata):
            ind = 0
            for c in ndata:
                data[ind + pos] = c
                ind += 1
        return data

    def contDisk(self):
        """contDisk affiche le contenu du disque choisi

        Returns:
            _En cas d'erreur retourne un False
        """
        self.chemin = Disk.listDisk[self.indDisk][2]
        self.sizeDisk = int(Disk.listDisk[self.indDisk][1])
        viewTrackList = []
        if self.readFormat():
            self.findTrack()
            compt = 0
            totTrack = SECTOR
            for v in self.listTrack.values():
                if v[1] != MPEG1L2[0][0]:
                    compt += 1
                    x = list(v[4])
                    stamp = "{:02d}-{:02d}-{:02d} {:02d}:{:02d}".format(
                        x[0], x[1], x[2], x[3], x[4]
                    )
                    viewTrackList.append(
                        "{:03d}{} {} {}".format(compt, v[3], stamp, v[5])
                    )
                    totTrack += v[2]
            percent = int((totTrack * 100) / self.sizeDisk)
            return True, percent, viewTrackList
        return False, 0, []

    def modifHead(self, item, offset, val):
        """modifHead permet de modifier l'entête d'un disque ou d'une piste audio

        Args:
            item: nom de l'action souhaitée
            offset: décalaga par rapport à l'adresse de la piste courante
            val: nouvelle valeur pour cette modification

        Returns:
            booléen de l'écriture de la modification
        """
        if item == "title_disk" or item == "format_disk" or item == "erase_backup":
            address = 0
        else:
            address = self.listTrack[self.indTrack][0] + offset
        data = self.readHex(address, SECTOR)
        match item:
            case "format_disk":
                datam = []
                datam += Disk.codNbBytes(FORMAT_NFS, 2)
                datam += Disk.codNbBytes(SECTOR, 4)
                datam += Disk.codNbBytes(0, 4)
                datam += Disk.codStamp("now")
                datam += MACHINE
                datam += [255] * 32
                datam += Disk.codText(LANG["format_sta"][Disk.lang])
                datam += [255] * 32
                datam += [0] * 384
                datam += [255] * 128
                datam += [0] * 384
            case "code_track":
                datam = Disk.replace(data, 0, Disk.codNbBytes(val, 2))
            case "size_track":
                datam = Disk.replace(data, 2, Disk.codNbBytes(val, 4))
            case "nbBytes_track":
                datam = Disk.replace(data, 6, Disk.codNbBytes(val, 4))
            case "timeDate_track":
                datam = Disk.replace(data, 10, [0])
                datam = Disk.replace(data, 11, val)
            case "dur_track":
                datam = Disk.replace(data, 16, Disk.codNbBytes(val, 4))
            case "title_disk":
                datam = Disk.replace(data, 64, val)
            case "title_track":
                datam = Disk.replace(data, 64, val)
            case "fill_head":
                datam = Disk.replace(data, 0, val * HEAD)
            case "erase_backup":
                datam = Disk.replace(data, 288, [0] * 224)
        result = self.writHex(address, datam)
        return result

    def nbBytesMilliSec(self, indTrack, nbBytes):
        code = self.listTrack[indTrack][1]
        sizeFrame = FORMAT_AUDIO[code][1]
        durFrame = FORMAT_AUDIO[code][2]
        milliSec = int((nbBytes * durFrame) / sizeFrame)
        return milliSec

    def durFormTrack(millisecond):
        second = int(millisecond / 1000)
        heure = int(second / 3600)
        second %= 3600
        minute = int(second / 60)
        second %= 60
        second = int(second)
        hms = "{:01d}h {:02d}:{:02d}".format(heure, minute, second)
        return hms

    def detailTrackAudio(data):
        frameFound = []
        sizeFrameList = []
        first = True
        equal = False
        sizeFrame = 0
        codeFound = 0
        gap = 0
        message = ""
        try:
            for i in range(0, len(data) - 1, 16):
                mpegFound = Disk.decNbBytes(data[i : i + 2])
                if (mpegFound & 57599) / 57599 in MPEG.keys() and mpegFound != 65535 and first:
                    versionFound = (mpegFound & 6144) / 2048
                    message += (
                        "MPEG "
                        + VERSION[versionFound]
                        + " "
                        + LAYER[(mpegFound & 1536) / 512]
                        + "\n"
                    )
                    message += PROTECT[(mpegFound & 256) / 256] + "\n"
                    if versionFound == 3:  # MPEG version 1
                        message += BITRATE_V1[(data[i + 2] & 240) / 16] + "\n"
                        message += FREQUENCY_V1[(data[i + 2] & 12) / 4] + "\n"
                    if versionFound == 2:  # MPEG version 1
                        message += BITRATE_V2[(data[i + 2] & 240) / 16] + "\n"
                        message += FREQUENCY_V2[(data[i + 2] & 12) / 4] + "\n"
                    message += CHANNEL[(data[i + 3] & 192) / 64] + "\n"
                    message += COPYRIGHT[(data[i + 3] & 8) / 8] + "\n"
                    message += ORIGINAL[(data[i + 3] & 4) / 4] + "\n"
                    frameFound = mpegFound
                    first = False
                    sizeFrameList.append(i)
                    gap = i
                    code1 = mpegFound
                    code2 = Disk.decNbBytes(data[i + 2 : i + 4])
                else:
                    cd2 = Disk.decNbBytes(data[i + 2 : i + 4])
                    if mpegFound == frameFound and cd2 == code2:
                        sizeFrameList.append(i)
            if len(sizeFrameList) > 2:
                first = True
                equal = True
                for d in range(1, len(sizeFrameList)):
                    if first:
                        sizeFrame = sizeFrameList[d] - sizeFrameList[d - 1]
                        first = False
                    else:
                        if sizeFrame == sizeFrameList[d] - sizeFrameList[d - 1]:
                            equal = equal and True
                        else:
                            equal = equal and False
                message += "Bytes per frame: " + str(sizeFrame) + "\n"
                message += (
                    "Filtered codes: "
                    + str(code1)
                    + "->"
                    + str(code1 & FILTER[0])
                    + " - "
                    + str(code2)
                    + "->"
                    + str(code2 & FILTER[1])
                    + "\n"
                )
                found = False
                for key, value in FORMAT_AUDIO.items():
                    if (
                        value[3] == (code1 & FILTER[0])
                        and value[4] == (code2 & FILTER[1])
                        and value[1] == sizeFrame
                    ):
                        message += "Code " + str(key) + " match in NFS Format"
                        found = True
                        code = key
                if found:
                    return True, message, gap, sizeFrame, code
                else:
                    message += LANG["frameHeader_no"][Disk.lang]
                    return False, message, 0, 0, 0
            else:
                message = LANG["frameHeader_no"][Disk.lang]
                return False, message, 0, 0, 0
        except KeyError:
            message = LANG["frameHeader_no"][Disk.lang]
            return False, message, 0, 0, 0

    def createNewTrack(self, code, sizeFrame, title, stamp, dataImport):
        nbFrame = Disk.searchFrame(0, sizeFrame, dataImport)
        nbBytesTrack = nbFrame * sizeFrame
        size = HEAD + nbBytesTrack
        if size % SECTOR > 0:
            sizeNewTrack = size // SECTOR + 1
        else:
            sizeNewTrack = size // SECTOR
        sizeNewTrack = sizeNewTrack * SECTOR
        self.indTrack = len(self.listTrack) - 1
        if (
            self.listTrack[self.indTrack][0] + sizeNewTrack + (16 * SECTOR)
            > self.sizeDisk
        ):
            return False, LANG["too_big"][Disk.lang]
        self.modifHead("erase_backup", 0, [255])
        self.modifHead("fill_head", 0, [255])
        self.modifHead("code_track", 0, code)
        self.modifHead("timeDate_track", 0, stamp)
        self.modifHead("nbBytes_track", 0, nbBytesTrack)
        durTrack = nbFrame * FORMAT_AUDIO[code][2]
        self.modifHead("dur_track", 0, durTrack)
        self.modifHead("title_track", 0, Disk.codText(title))
        data = self.readHex(self.listTrack[self.indTrack][0], sizeNewTrack)
        datam = Disk.replace(data, HEAD, dataImport[0:nbBytesTrack])
        datam = Disk.replace(
            data, HEAD + nbBytesTrack, [0] * (sizeNewTrack - HEAD - nbBytesTrack)
        )
        result = self.writHex(self.listTrack[self.indTrack][0], datam)
        self.modifHead("size_track", 0, sizeNewTrack)
        self.modifHead("fill_head", sizeNewTrack, [255])
        return True, LANG["import_ok"][Disk.lang]

    def offsetSecStamp(offsetSec, chrono):
        day = chrono[0]
        month = chrono[1]
        year = chrono[2]
        hour = chrono[3]
        minute = chrono[4]
        stamp = [minute, hour, day, month, year]
        newSecond = offsetSec + Disk.dateTimeToSec(stamp)
        newStamp = Disk.secToDateTime(newSecond)
        return newStamp

    def exportTrackNFS(self):
        try:
            if self.assembly == False:
                title = self.listTrack[self.indTrack][5]
                data = self.readHex(
                    self.listTrack[self.indTrack][0], self.listTrack[self.indTrack][2]
                )
                result, gap, remain, commentType = self.typeTrack()
                if title == "":
                    title = self.listTrack[self.indTrack][3]
                    chrono = self.listTrack[self.indTrack][4]
                    title += "-{:02d}{:02d}{:02d}_{:02d}{:02d}".format(
                        chrono[2], chrono[1], chrono[0], chrono[3], chrono[4]
                    )
                if gap > 0:
                    datam = data[0:HEAD]
                    datam += data[HEAD + gap : -remain]
                    datam += bytearray([0] * (gap + remain))
                    return True, title, datam
                else:
                    datam = data[0:-remain]
                    datam += bytearray([0] * remain)
                    return True, title, datam
            else:
                title = self.listTrack[self.indAssembly][5]
                self.indTrack = self.indAssembly
                arrayInOut = self.segmentAssembly()
                dataAssembly = bytearray([255] * HEAD)
                first = True
                for i in arrayInOut:
                    begin, gap = Disk.sectorBefore(i[1])
                    end, remain = Disk.sectorAfter(i[2])
                    if begin + gap >= end - remain:  # case begin > end
                        continue
                    if first:
                        first = False
                        trackInitial = self.listTrack[i[0]]
                        code = trackInitial[1]
                        chrono = trackInitial[4]
                        sizeFrame = FORMAT_AUDIO[code][1]
                        durFrame = FORMAT_AUDIO[code][2]
                        offset = i[1] - (trackInitial[0] + HEAD)
                        offsetSec = int((offset / sizeFrame) / (durFrame * 1000))
                        newStamp = Disk.offsetSecStamp(offsetSec, chrono)
                    data = self.readHex(begin, (end - begin))
                    dataAssembly += data[gap:-remain]
                nbBytesAudio = len(dataAssembly) - HEAD
                durTrack = int((nbBytesAudio / sizeFrame) * durFrame)
                Disk.replace(dataAssembly, 0, Disk.codNbBytes(code, 2))  # code
                Disk.replace(
                    dataAssembly, 6, Disk.codNbBytes(nbBytesAudio, 4)
                )  # nb Bytes Audio
                Disk.replace(
                    dataAssembly, 16, Disk.codNbBytes(durTrack, 4)
                )  # duration in mSec
                Disk.replace(dataAssembly, 10, newStamp)
                if title == "":
                    title = self.listTrack[self.indTrack][3][1:]
                    title += "-{:02d}{:02d}{:02d}_{:02d}{:02d}".format(
                        chrono[2], chrono[1], chrono[0], chrono[3], chrono[4]
                    )
                Disk.replace(dataAssembly, 64, Disk.codText(title))
                dataAssembly += bytearray(
                    [0] * (SECTOR - (len(dataAssembly) % SECTOR))
                )  # Add zero to find multiple SECTOR
                Disk.replace(
                    dataAssembly, 2, Disk.codNbBytes(len(dataAssembly), 4)
                )  # nb Bytes Track
                return True, title, dataAssembly
        except:
            return False, "", []

    def segmentAssembly(self):
        arrayInOut = []
        data = self.readHex(self.listTrack[self.indTrack][0], SECTOR)
        durTrack = 0
        for i in range(HEAD, len(data) - 1, 14):
            nbBytes = Disk.decNbBytes(data[i : i + 4])
            if nbBytes < 4294967295:  # FF FF FF FF?
                inSegment = Disk.decNbBytes(data[i + 4 : i + 8])
                outSegment = Disk.decNbBytes(data[i + 8 : i + 12])
                indTrack = Disk.decNbBytes(data[i + 12 : i + 14]) - 1
                beginTrack = self.listTrack[indTrack][0]
                inForm = round(
                    self.nbBytesMilliSec(indTrack, (inSegment - beginTrack)) / 1000, 1
                )
                outForm = round(
                    self.nbBytesMilliSec(indTrack, (outSegment - beginTrack)) / 1000, 1
                )
                if inSegment < outSegment:
                    durTrack += self.nbBytesMilliSec(indTrack, (outSegment - inSegment))
                durForm = round(durTrack / 1000, 1)
                comment = f"{indTrack + 1:03d} - in:{inForm:0.1f}s   out:{outForm:0.1f}s   Σ={durForm:0.1f}s"
                arrayInOut.append((indTrack, inSegment, outSegment, nbBytes, comment))
            else:
                self.modifHead("dur_track", 0, durTrack)
                return arrayInOut
        return arrayInOut

    def cursorAssembly(self, index, inOut):
        indTrack = self.listAssembly[index][0]
        self.indTrack = indTrack
        match inOut:
            case "in":
                address = self.listAssembly[index][1]
            case "out":
                address = self.listAssembly[index][2]
        begin = self.listTrack[indTrack][0] + HEAD
        sizeFrame = FORMAT_AUDIO[self.listTrack[indTrack][1]][1]
        durFrame = FORMAT_AUDIO[self.listTrack[indTrack][1]][2]
        cursor = round(((address - begin) * durFrame) / (sizeFrame * 1000), 1)
        title = self.listTrack[indTrack][5]
        duration = int(self.listTrack[indTrack][7] / 1000)
        return cursor, title, duration

    def copyTrackNFS(self, sizeTrack, data):
        self.indTrack = len(self.listTrack) - 1
        if self.listTrack[self.indTrack][0] + sizeTrack + (16 * SECTOR) > self.sizeDisk:
            return False, LANG["too_big"][Disk.lang]
        result = self.writHex(self.listTrack[self.indTrack][0], data)
        status = self.modifHead("fill_head", sizeTrack, [255])
        return True, LANG["import_ok"][Disk.lang]

    def recovery(self):
        try:
            endOfSearch = self.sizeDisk - (RESERVE + SEEK)
            beginOfSearch = self.listTrack[len(self.listTrack) - 1][0]
            self.indTrack += 1
            lineFF = bytearray([255] * 4)  # test on "FF FF FF FF"
            if beginOfSearch < endOfSearch:
                data = self.readHex(beginOfSearch, (endOfSearch - beginOfSearch))
                for i in range(SECTOR, len(data), SECTOR):
                    if lineFF == data[i : i + 4] or lineFF == data[i + 32 : i + 36]:
                        self.modifHead("code_track", 0, 24770)
                        self.modifHead("size_track", 0, i)
                        self.modifHead(
                            "title_track",
                            0,
                            Disk.codText(LANG["track_recovered"][Disk.lang]),
                        )
                        self.modifHead("timeDate_track", 0, Disk.codStamp("NOW"))
                        return True
                return False
            return False
        except KeyError:
            return False

    def typeTrack(self):
        if len(self.listTrack) - 2 == self.indTrack:  # For cutting only the last track
            noLastTrack = False
        else:
            noLastTrack = True
        data = self.readHex(self.listTrack[self.indTrack][0], SEEK)
        codeFound = Disk.decNbBytes(data[0:2])
        if codeFound in FORMAT_AUDIO.keys():
            if FORMAT_AUDIO[codeFound][5] == "m":  # Audio MPEG track
                result, message, gap, sizeFrame, code = Disk.detailTrackAudio(
                    data[HEAD:]
                )
                if result:
                    if code != codeFound and code != 0:
                        self.listTrack[self.indTrack][1] = code
                        self.modifHead("code_track", 0, code)
                    if gap > 0:
                        message += "\n" + LANG["gapNO_track"][Disk.lang]
                    else:
                        message += "\n" + LANG["gapOK_track"][Disk.lang]
                    check, remain, comment = self.checkFrameAudio(gap)
                    message += comment
                    check = check or noLastTrack
                    return check, gap, remain, message
                else:
                    return True, 0, 0, message
            elif FORMAT_AUDIO[codeFound][5] == "ma":  # Assembly MPEG track
                listAssembly = self.segmentAssembly()
                comment = LANG["assembly_track"][Disk.lang] + "\n\n"
                for p in listAssembly:
                    comment += p[4] + "\n"
                return True, 0, 0, comment
            else:
                return True, 0, 0, LANG["no_mpeg"][Disk.lang]
        else:
            return True, 0, 0, LANG["no_audio"][Disk.lang]

    def searchFrame(gap, sizeFrame, data):
        if sizeFrame == 0:
            return 0
        nbFrame = 1
        first = True
        for i in range(gap, len(data) - 1, sizeFrame):
            mpegFound = Disk.decNbBytes(data[i : i + 4])
            if first:
                first = False
                codeTrack = mpegFound
            else:
                if mpegFound == codeTrack:
                    nbFrame += 1
                else:
                    break
        return nbFrame

    def checkFrameAudio(self, gap):
        ind = self.indTrack
        sizeFrame = FORMAT_AUDIO[self.listTrack[ind][1]][1]
        durFrame = FORMAT_AUDIO[self.listTrack[ind][1]][2]
        begin = self.listTrack[ind][0]
        long = self.listTrack[ind][2]
        data = self.readHex(begin, long)
        nbFrame = Disk.searchFrame(HEAD + gap, sizeFrame, data)
        remain = self.listTrack[ind][2] - (HEAD + gap + nbFrame * sizeFrame)
        nbBytes = self.listTrack[ind][6]
        durTrack = self.listTrack[ind][7]
        message = ""
        if remain > sizeFrame:
            message += "\n" + LANG["remainNO_track"][Disk.lang]
            check = False
        else:
            message += "\n" + LANG["remainOK_track"][Disk.lang]
            check = True
        if nbFrame * durFrame != durTrack:
            self.modifHead("dur_track", 0, (nbFrame * durFrame))
            message += (
                "\n"
                + LANG["durNO_track"][Disk.lang]
                + str(nbFrame * durFrame)
                + " mSec"
            )
        else:
            message += (
                "\n"
                + LANG["durOK_track"][Disk.lang]
                + str(nbFrame * durFrame)
                + " mSec"
            )
        if nbFrame * sizeFrame != nbBytes:
            self.modifHead("nbBytes_track", 0, (nbFrame * sizeFrame))
            message += (
                "\n"
                + LANG["sizeNO_track"][Disk.lang]
                + str(nbFrame * sizeFrame)
                + " Bytes"
            )
        else:
            message += (
                "\n"
                + LANG["sizeOK_track"][Disk.lang]
                + str(nbFrame * sizeFrame)
                + " Bytes"
            )
        self.findTrack()
        return check, remain, message

    def delTrack(self):
        if self.assembly:
            self.indTrack = self.indAssembly
        self.saveDelTrack()
        data = self.readHex(self.listTrack[self.indTrack][0], SECTOR)
        datam = Disk.replace(data, 0, [255] * 32)
        status = self.writHex(self.listTrack[self.indTrack][0], datam)
        return status

    def saveDelTrack(self):
        data = Disk.codNbBytes(self.indTrack + 1, 2)  # save index track
        data += [0] * 14
        headDel = self.readHex(self.listTrack[self.indTrack][0], SECTOR)
        data += headDel[0:HEAD]
        head = self.readHex(0, SECTOR)
        datam = Disk.replace(head, 288, data)
        status = self.writHex(0, datam)
        return status

    def cancelDelTrack(self):
        head = self.readHex(0, SECTOR)
        data = self.readHex(self.listTrack[len(self.listTrack) - 1][0], SECTOR)
        datam = Disk.replace(data, 0, head[304:400])
        status1 = self.writHex(self.listTrack[len(self.listTrack) - 1][0], datam)
        dataX = Disk.replace(head, 288, [0] * 224)
        status2 = self.writHex(0, dataX)
        return status1 and status2

    def cutTrack(self, remain):
        stop = (
            self.listTrack[self.indTrack][0] + self.listTrack[self.indTrack][2] - remain
        )
        chrono = self.listTrack[self.indTrack][4]
        durFrame, sizeFrame = self.getFrame(self.indTrack)
        cutAddress, noUsed = Disk.sectorAfter(stop)
        sizeCutTrack = cutAddress - self.listTrack[self.indTrack][0]
        sizeNewTrack = self.listTrack[self.indTrack][2] - sizeCutTrack
        self.saveCutTrack(cutAddress)
        self.modifHead("fill_head", sizeCutTrack, [255])
        self.modifHead("size_track", 0, sizeCutTrack)
        self.modifHead("code_track", sizeCutTrack, self.listTrack[self.indTrack][1])
        self.modifHead("size_track", sizeCutTrack, sizeNewTrack)
        self.modifHead(
            "title_track", sizeCutTrack, Disk.codText(LANG["remain_track"][Disk.lang])
        )
        nbFrame = int((sizeCutTrack - HEAD) / sizeFrame)
        offsetSec = int(nbFrame * durFrame / 1000)
        newStamp = Disk.offsetSecStamp(offsetSec, chrono)
        self.modifHead("timeDate_track", sizeCutTrack, newStamp[1:])
        newNbFrame = int((sizeNewTrack - HEAD) / sizeFrame)
        nbBytesNewTrack = newNbFrame * sizeFrame
        self.modifHead("nbBytes_track", sizeCutTrack, nbBytesNewTrack)
        durNewTrack = newNbFrame * durFrame
        self.modifHead("dur_track", sizeCutTrack, durNewTrack)
        return True

    def saveCutTrack(self, cutAddress):
        data = Disk.codNbBytes(self.indTrack + 1, 2)  # save index of listBox
        data += Disk.codNbBytes(
            self.listTrack[self.indTrack][2], 4
        )  # save initial size track
        data += Disk.codNbBytes(cutAddress, 4)  # save address cutting
        data += [0] * 6
        headCut = self.readHex(cutAddress, SECTOR)
        data += headCut[0:HEAD]
        head = self.readHex(0, SECTOR)
        datam = Disk.replace(head, 400, data)
        status = self.writHex(0, datam)
        return status

    def cancelCutTrack(
        self,
    ):
        if not self.backupCut():
            return False
        data = self.readHex(0, SECTOR)
        cutAddress = Disk.decNbBytes(data[406:410])
        if cutAddress == 0:
            return
        dataCutAddress = self.readHex(cutAddress, SECTOR)
        datam = Disk.replace(dataCutAddress, 0, data[416:])
        status1 = self.writHex(cutAddress, datam)
        dataC = self.readHex(self.listTrack[self.indTrack][0], SECTOR)
        dataX = Disk.replace(dataC, 2, data[402:406])
        status2 = self.writHex(self.listTrack[self.indTrack][0], dataX)
        dataH = Disk.replace(data, 288, [0] * 224)  # cancel backup
        status3 = self.writHex(0, dataH)
        return status3

    def dateTimeToSec(stamp):
        day = stamp[2]
        month = stamp[3]
        year = stamp[4]
        if year < 70:
            Year = 2000 + year
        else:
            Year = 1900 + year
        hour = stamp[1]
        minute = stamp[0]
        date = "{:02d}-{:02d}-{:02d} {:02d}:{:02d}".format(
            Year, month, day, hour, minute
        )
        nbSec = datetime.datetime.fromisoformat(date).timestamp()
        return nbSec

    def secToDateTime(nbSec):
        chrono = str(datetime.datetime.fromtimestamp(nbSec))
        day = Disk.intHex(int(chrono[8:10]))
        month = Disk.intHex(int(chrono[5:7]))
        year = Disk.intHex(int(chrono[2:4]))
        hour = Disk.intHex(int(chrono[11:13]))
        minute = Disk.intHex(int(chrono[14:16]))
        stamp = [0, minute, hour, day, month, year]
        return stamp

    def sectorBefore(address):
        numSect = address // SECTOR
        newAddress = (numSect) * SECTOR
        gap = address - newAddress
        return newAddress, gap

    def sectorAfter(address):
        numSect = address // SECTOR
        newAddress = (numSect + 1) * SECTOR
        remain = newAddress - address
        return newAddress, remain

    def backupDel(self):
        data = self.readHex(0, SECTOR)
        code = Disk.decNbBytes(data[288:290])
        if code != 0:
            return True
        return False

    def backupCut(self):
        data = self.readHex(0, SECTOR)
        code = Disk.decNbBytes(data[400:402])
        if code != 0:
            return True
        return False

    def playSegment(self, track):
        cursor = self.cursorTrack
        duration = self.cursorSegment
        assembly = FORMAT_AUDIO[track[1]][5]
        if assembly == "ma" or assembly == "na":
            return False, track[5]
        else:
            sizeFrame = FORMAT_AUDIO[track[1]][1]
            durFrame = FORMAT_AUDIO[track[1]][2]
            endTrack = track[0] + track[2]
            beginTrack = track[0] + HEAD
            nbFrame = int((cursor * 1000) / durFrame)
            if self.assembly & self.outPlay:
                longSegment = Disk.sectorAfter(
                    int(3000 / durFrame) * sizeFrame
                )  # Default listening length in out 3 sec
                endSegment = Disk.sectorAfter(beginTrack + (nbFrame * sizeFrame))
                beginSegment = Disk.sectorBefore(endSegment[0] - longSegment[0])
            else:
                beginSegment = Disk.sectorBefore(beginTrack + (nbFrame * sizeFrame))
                long = int((duration * 1000) / durFrame) * sizeFrame
                longSegment = Disk.sectorAfter(long)
            if beginSegment[0] + longSegment[0] > endTrack:
                lSegt = list(longSegment)
                lSegt[0] = endTrack - beginSegment[0]
                longSegment = tuple(lSegt)
            data = self.readHex(beginSegment[0], longSegment[0])
            remain = (longSegment[0] - beginSegment[1]) % sizeFrame
            fw = open(NAMESEGT, "w+b")
            fw.write(data[beginSegment[1] : -remain])
            fw.close()
            title = track[5]
            sub = subprocess.run(
                [
                    "ffplay",
                    "-window_title",
                    title,
                    "-loglevel",
                    "-8",
                    "-x",
                    "400",
                    "-y",
                    "200",
                    "-seek_interval",
                    "5",
                    "-showmode",
                    "2",
                    "-autoexit",
                    NAMESEGT,
                ],
            )
            return True, title

    def getFrame(self, indTrack):
        sizeFrame = FORMAT_AUDIO[self.listTrack[indTrack][1]][1]
        durFrame = FORMAT_AUDIO[self.listTrack[indTrack][1]][2]
        return durFrame, sizeFrame

    def setAssembly(self, indTrack, mode):
        match mode:
            case "add":
                indFirstSegment = self.listAssembly[0][0]
                codeFirstSegment = self.listTrack[indFirstSegment][1]
                codeNewSegment = self.listTrack[indTrack][1]
                addressAssembly = self.listTrack[self.indAssembly][0]
                if codeFirstSegment == codeNewSegment:
                    indNextSegment = len(self.listAssembly)
                    inSegment = self.listTrack[indTrack][0] + HEAD
                    durFrame, sizeFrame = self.getFrame(indTrack)
                    nbFrame = int(self.listTrack[indTrack][6] / sizeFrame) - 1
                    outSegment = inSegment + (nbFrame * sizeFrame)
                    data = self.readHex(addressAssembly, SECTOR)
                    i = (indNextSegment * 14) + HEAD
                    cumulNbBytes = Disk.decNbBytes(data[i - 14 : i - 10])
                    cumulNbBytes += Disk.decNbBytes(data[i - 6 : i - 2])
                    cumulNbBytes -= Disk.decNbBytes(data[i - 10 : i - 6])
                    dataModif = Disk.codNbBytes(indNextSegment + 1, 4)
                    nbFrame = self.listTrack[indTrack][6] // sizeFrame
                    beginSegment = self.listTrack[indTrack][0] + HEAD
                    endSegment = beginSegment + (nbFrame * sizeFrame)
                    cumulNbBytes += endSegment
                    cumulNbBytes -= beginSegment
                    durTrack = (cumulNbBytes // sizeFrame) * durFrame
                    Disk.replace(data, 16, Disk.codNbBytes(durTrack, 4))
                    dataModif += Disk.codNbBytes(beginSegment, 4)
                    dataModif += Disk.codNbBytes(endSegment, 4)
                    dataModif += Disk.codNbBytes(indTrack + 1, 2)
                    dataModif += [255] * ((len(dataModif) + i) % 16 + 16)
                    Disk.replace(data, i, dataModif)
                    status = self.writHex(addressAssembly, data)
                    return status
                else:
                    return False
            case "del":
                indLastSegment = len(self.listAssembly) - 1
                addressAssembly = self.listTrack[self.indAssembly][0]
                if indLastSegment == 0:  # erase impossible for first segment
                    return False
                durFrame, sizeFrame = self.getFrame(indTrack)
                data = self.readHex(addressAssembly, SECTOR)
                i = HEAD + indLastSegment * 14
                cumulNbBytes = Disk.decNbBytes(data[i - 14 : i - 10])
                cumulNbBytes += Disk.decNbBytes(data[i - 6 : i - 2])
                cumulNbBytes -= Disk.decNbBytes(data[i - 10 : i - 6])
                dataModif = [255] * ((i % 16) + 16)
                dataModif += [0] * (SECTOR - (len(dataModif) + i))
                Disk.replace(data, i, dataModif)
                durTrack = (cumulNbBytes // sizeFrame) * durFrame
                Disk.replace(data, 6, Disk.codNbBytes(indLastSegment + 1, 4))
                Disk.replace(data, 16, Disk.codNbBytes(durTrack, 4))
                status = self.writHex(addressAssembly, data)
                return status
            case "make":
                self.assembly = True
                self.indAssembly = len(self.listTrack) - 1
                addressAssembly = self.listTrack[self.indAssembly][0]
                inSegment = self.listTrack[indTrack][0] + HEAD
                outSegment = inSegment + self.listTrack[indTrack][6]
                title = self.listTrack[indTrack][5]
                code = self.listTrack[indTrack][1] + 1
                durTrack = self.listTrack[indTrack][7]
                dataModif = Disk.codNbBytes(code, 2)
                dataModif += Disk.codNbBytes(SECTOR, 4)
                dataModif += Disk.codNbBytes(14, 4)
                dataModif += Disk.codStamp("now")
                dataModif += Disk.codNbBytes(durTrack, 4)
                dataModif += [255] * 44
                dataModif += Disk.codText(title)
                dataModif += [0] * 4
                dataModif += Disk.codNbBytes(inSegment, 4)
                dataModif += Disk.codNbBytes(outSegment, 4)
                dataModif += Disk.codNbBytes(indTrack + 1, 2)
                dataModif += [255] * 18
                dataModif += [0] * (SECTOR - len(dataModif))
                dataModif += [255] * 32
                data = self.readHex(addressAssembly, SECTOR * 2)
                Disk.replace(data, 0, dataModif)
                status = self.writHex(addressAssembly, data)
                self.indTrack = self.indAssembly
                return True
            case "setIn":
                index = indTrack
                addressAssembly = self.listTrack[self.indAssembly][0]
                begin = self.listTrack[self.listAssembly[index][0]][0]
                code = self.listTrack[self.indAssembly][1] - 1  # code audio
                sizeFrame = FORMAT_AUDIO[code][1]
                durFrame = FORMAT_AUDIO[code][2]
                inSegment = (
                    begin + int((self.cursorTrack * 1000) / durFrame) * sizeFrame
                )
                i = HEAD + (index * 14) + 4
                data = self.readHex(addressAssembly, SECTOR)
                dataModif = Disk.codNbBytes(inSegment, 4)
                Disk.replace(data, i, dataModif)
                status = self.writHex(addressAssembly, data)
                self.indTrack = self.indAssembly
                return True
            case "setOut":
                index = indTrack
                addressAssembly = self.listTrack[self.indAssembly][0]
                begin = self.listTrack[self.listAssembly[index][0]][0]
                code = self.listTrack[self.indAssembly][1] - 1
                sizeFrame = FORMAT_AUDIO[code][1]
                durFrame = FORMAT_AUDIO[code][2]
                outSegment = (
                    begin + int((self.cursorTrack * 1000) / durFrame) * sizeFrame
                )
                i = HEAD + (index * 14) + 8
                data = self.readHex(addressAssembly, SECTOR)
                dataModif = Disk.codNbBytes(outSegment, 4)
                Disk.replace(data, i, dataModif)
                status = self.writHex(addressAssembly, data)
                self.indTrack = self.indAssembly
                return True
