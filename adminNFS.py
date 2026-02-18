"""
Auteur: Claude Eldet (eldet@wanadoo.fr) Version 1.0 Janvier 2026.
"""

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os
from os.path import expanduser
import subprocess
from subprocess import PIPE, STDOUT
from cardCfNFS import *

script_dir = os.path.dirname(os.path.abspath(__file__))
home_folder = expanduser("~")


def langFR():
    Disk.lang = "FR"
    updateLang()


def langUK():
    Disk.lang = "UK"
    updateLang()


def updateLang():
    cellB0.config(text=LANG["physicDisk"][Disk.lang])
    cellA2.config(text=LANG["edit_tit"][Disk.lang])
    cellA3.config(text=LANG["details_track"][Disk.lang])
    cellG3.config(text=LANG["exportNFS_track"][Disk.lang])
    cellA4.config(text=LANG["add_track"][Disk.lang])
    if Disk.view == "A":
        cellG4.config(text=LANG["copy_toB"][Disk.lang], bg=COLOR["B"])
    elif Disk.view == "B":
        cellG4.config(text=LANG["copy_toA"][Disk.lang], bg=COLOR["A"])
    cellA5.config(text=LANG["import_track"][Disk.lang])
    cellG5.config(text=LANG["export_mp3"][Disk.lang])
    cellA6.config(text=LANG["erase_track"][Disk.lang])
    cellG6.config(text=LANG["cancel_erase"][Disk.lang])
    cellB7.config(text=LANG["title_track"][Disk.lang])
    cellC7.config(text=LANG["time_track"][Disk.lang])
    cellG7.config(text=LANG["analysis_track"][Disk.lang])
    cellA8.config(text=LANG["edit_head"][Disk.lang])
    cellC8.config(text=LANG["day_track"][Disk.lang])
    cellC10.config(text=LANG["segment_in"][Disk.lang])
    cellF10.config(text=LANG["segment_out"][Disk.lang])
    cellG9.config(text=LANG["segment_add"][Disk.lang])
    cellA9.config(text=LANG["segment_set"][Disk.lang])
    cellG10.config(text=LANG["segment_del"][Disk.lang])
    cellA12.config(text=LANG["listen"][Disk.lang])
    cellB13.config(text=LANG["cursor_cut"][Disk.lang])
    cellC13.config(text=LANG["save_cut"][Disk.lang])
    cellA13.config(text=LANG["quit"][Disk.lang])
    cellG13.config(text=LANG["recovery_track"][Disk.lang])
    if Disk.view == "A":
        diskA()
    elif Disk.view == "B":
        diskB()


def resetDisk():
    """actualiseDisque permet de lister tous les disques physiques amovibles du système"""
    clearNiv0()
    if Disk.findDisk():
        for d in Disk.listDisk:
            cellB1.insert(END, d[0] + " - " + d[1] + " octets")
        return True
    else:
        messagebox.showinfo(
            LANG["examDisk_tit"][Disk.lang], LANG["examDisk_cont"][Disk.lang]
        )
        return False


def clearNiv0():
    Disk.listDisk = []
    cardA.__init__("A")
    cardB.__init__("B")
    cellB1.delete(0, END)
    clearNiv1()


def clearNiv1():
    bay.configure(background=COLOR[Disk.view])
    cellB1.selection_clear(0, END)
    cellA2.config(state="disabled")
    titDisk.set(LANG["doubleClic"][Disk.lang])  # cellB2W
    cellC2.config(text="", bg=COLOR[Disk.view])
    cellG2["value"] = 0  # ProgressBar
    cellA3.config(state="disabled")
    cellB3.delete(0, END)
    cellG3.config(state="disabled")
    cellA4.config(state="disabled")
    cellG4.config(state="disabled", bg=BUTTON)
    cellA5.config(state="disabled")
    cellG5.config(state="disabled")
    cellG7.config(state="disabled")
    cellB9.delete(0, END)
    clearNiv2()


def clearNiv2():
    cellB3.selection_clear(0, END)  # on efface la sélection de la liste de prises
    cellG3.config(state="disabled")
    cellG4.config(state="disabled", bg=BUTTON)
    cellG5.config(state="disabled")
    cellB7.config(bg=COLOR[Disk.view])
    cellA6.config(state="disabled")
    cellG7.config(state="disabled")
    trackTitle.set("")
    trackDay.set("")
    cellC8.config(bg=COLOR[Disk.view])
    cellC7.config(bg=COLOR[Disk.view])
    trackHour.set("")
    trackMonth.set("")
    trackMin.set("")
    trackYear.set("")
    cellF7.config(text="")
    cellF7.config(bg=COLOR[Disk.view])
    cellA8.config(state="disabled")
    cellC10.config(state="disabled")
    cellG9.config(state="disabled")
    cellF10.config(state="disabled")
    cellA9.config(state="disabled")
    cellC9.config(state="disabled")
    cellD9.config(state="disabled")
    cellF9.config(state="disabled")
    cellD10.config(state="disabled")
    cellG10.config(state="disabled")
    cellA12.config(state="disabled")
    cursor.set(0)
    cellB12.config(label=LANG["listen_point"][Disk.lang], bg=COLOR[Disk.view])
    cellB12.config(state="disabled")
    cursorSegment.set(30)
    cellG12.config(label=LANG["duration_point"][Disk.lang], bg=COLOR[Disk.view])
    cellG12.config(state="disabled")


def affectAB(event):
    """affect un disque physique au disque courant A ou B

    Args:
        event: sur un double clic de souris sur le disque physique
    """
    if Disk.view == "A":
        cardA.indDisk = cellB1.curselection()[0]
        cardA.diskSize = int(Disk.listDisk[cellB1.curselection()[0]][1])
        diskA()
        cardA.modifHead(
            "erase_backup", 0, 0
        )  # effacement préalable des sauvegardes en entête
    elif Disk.view == "B":
        cardB.indDisk = cellB1.curselection()[0]
        cardB.diskSize = int(Disk.listDisk[cellB1.curselection()[0]][1])
        diskB()
        cardB.modifHead(
            "erase_backup", 0, 0
        )  # effacement préalable des sauvegardes en entête
    cellG6.config(state="disabled")


def askFormat():
    result = messagebox.askyesno(
        LANG["format_tit"][Disk.lang],
        LANG["format_cont"][Disk.lang],
    )
    return result


def diskA():
    """diskA rend le disque A courant pour affectation ou affichage des données qu'il comporte"""
    Disk.view = "A"
    cellA10.config(bg=COLOR[Disk.view])
    clearNiv1()
    if cardA.indDisk < 0:
        return
    cellB1.selection_set(cardA.indDisk)
    cellB1.see(cardA.indDisk)
    status, percent, viewTrackList = cardA.contDisk()
    if status:
        if cardA.backupDel():
            cellG6.config(state="normal")
        else:
            cellG6.config(state="disabled")
        cellG2["value"] = percent
        cellA2.config(state="normal")
        for p in viewTrackList:
            cellB3.insert(END, p)
        titDisk.set(cardA.title_1)
        cellC2.config(text="Date format: " + cardA.stamp1, bg=COLOR[Disk.view])
        cellA4.config(state="normal")
        cellG4.config(text=LANG["copy_toB"][Disk.lang], bg=COLOR["B"])
        cellG4.config(state="disabled")
        cellA5.config(state="normal")
        cellG5.config(state="disabled")
        if len(viewTrackList) > 0:
            cellA3.config(state="normal")
            if cardA.indTrack >= 0:
                if len(viewTrackList) > cardA.indTrack:
                    cellB3.selection_set(cardA.indTrack)
                    cellB3.see(cardA.indTrack)
                    lookTrack()
        return True
    else:
        if askFormat():
            cardA.chemin = Disk.listDisk[cardA.indDisk][2]
            if cardA.modifHead("format_disk", 0, 0):
                diskA()
                return
            return
        return


def diskB():
    """diskB rend le disque B courant pour affectation ou affichage des données qu'il comporte"""
    Disk.view = "B"
    cellA10.config(bg=COLOR[Disk.view])
    clearNiv1()
    if cardB.indDisk < 0:
        return
    cellB1.selection_set(cardB.indDisk)
    cellB1.see(cardB.indDisk)
    status, percent, viewTrackList = cardB.contDisk()
    if status:
        if cardB.backupDel():
            cellG6.config(state="normal")
        else:
            cellG6.config(state="disabled")
        cellG2["value"] = percent
        cellA2.config(state="normal")
        for p in viewTrackList:
            cellB3.insert(END, p)
        titDisk.set(cardB.title_1)
        cellC2.config(text="Date format: " + cardB.stamp1, bg=COLOR[Disk.view])
        cellA4.config(state="normal")
        cellG4.config(text=LANG["copy_toA"][Disk.lang], bg=COLOR["A"])
        cellG4.config(state="disabled")
        cellA5.config(state="normal")
        cellG5.config(state="normal")
        if len(viewTrackList) > 0:
            cellA3.config(state="normal")
            if cardB.indTrack >= 0:
                if len(viewTrackList) > cardB.indTrack:
                    cellB3.selection_set(cardB.indTrack)
                    cellB3.see(cardB.indTrack)
                    lookTrack()
        return True
    else:
        if askFormat():
            cardB.chemin = Disk.listDisk[cardB.indDisk][2]
            if cardB.modifHead("format_disk", 0, 0):
                diskB()
                return
            return
        return


def editHeadDisk():
    title = Disk.codText(cellB2.get())
    if Disk.view == "A":
        if cardA.modifHead("title_disk", 0, title):
            diskA()
    elif Disk.view == "B":
        if cardB.modifHead("title_disk", 0, title):
            diskB()


def editHeadTrack():
    title = Disk.codText(cellB8.get())
    if int(cellD8.get()[0:2]) > 31:
        messagebox.showinfo(LANG["title"][Disk.lang], LANG["day_head"][Disk.lang])
        return
    day = Disk.intHex(int(cellD8.get()[0:2]))
    if int(cellE8.get()[0:2]) > 12:
        messagebox.showinfo(LANG["title"][Disk.lang], LANG["month_head"][Disk.lang])
        return
    month = Disk.intHex(int(cellE8.get()[0:2]))
    year = Disk.intHex(int(cellF8.get()[0:2]))
    if int(cellD7.get()[0:2]) > 24:
        messagebox.showinfo(LANG["title"][Disk.lang], LANG["hour_head"][Disk.lang])
        return
    hour = Disk.intHex(int(cellD7.get()[0:2]))
    if int(cellE7.get()[0:2]) > 59:
        messagebox.showinfo(LANG["title"][Disk.lang], LANG["minute_head"][Disk.lang])
        return
    minute = Disk.intHex(int(cellE7.get()[0:2]))
    stamp = [minute, hour, day, month, year]
    if Disk.view == "A":
        if cardA.assembly:
            cardA.indTrack = cardA.indAssembly
        if cardA.modifHead("title_track", 0, title):
            if cardA.modifHead("timeDate_track", 0, stamp):
                diskA()
    elif Disk.view == "B":
        if cardB.assembly:
            cardB.indTrack = cardB.indAssembly
        if cardB.modifHead("title_track", 0, title):
            if cardB.modifHead("timeDate_track", 0, stamp):
                diskB()


def lookTrack():
    try:
        ind = int(cellB3.curselection()[0])
        cellG3.config(state="normal")
        cellG4.config(state="normal")
        cellG5.config(state="normal")
        cellA6.config(state="normal")
        cellG7.config(state="normal")
        cellA8.config(state="normal")
        cellC10.config(state="disabled")
        cellG9.config(state="disabled")
        cellF10.config(state="disabled")
        cellA9.config(state="normal")
        cellC9.config(state="disabled")
        cellD9.config(state="disabled")
        cellF9.config(state="disabled")
        cellD10.config(state="disabled")
        cellG10.config(state="disabled")
        cellA12.config(state="normal")
        cellB12.config(state="normal")
        cellG12.config(state="normal")
        cellB13.config(state="disabled")
        cellC13.config(state="disabled")
        if Disk.view == "A":
            if ind == cardA.indTrack:  # same track looking
                cursor.set(cardA.cursorTrack)
                cursorSegment.set(cardA.cursorSegment)
            else:
                cursor.set(0)
                cardA.cursorTrack = 0
                cursorSegment.set(30)
                cardA.cursorSegment = 30
                cardA.indTrack = ind
            if len(cardA.listTrack) - cardA.indTrack == 2:
                cellG13.config(state="normal")
            else:
                cellG13.config(state="disabled")
            title = cardA.listTrack[ind][5]
            trackTitle.set(title)
            trackDay.set(cardA.listTrack[ind][4][0])
            trackMonth.set(cardA.listTrack[ind][4][1])
            trackYear.set(cardA.listTrack[ind][4][2])
            trackHour.set(cardA.listTrack[ind][4][3])
            trackMin.set(cardA.listTrack[ind][4][4])
            duration = cardA.listTrack[ind][7]
            trackDur = Disk.durFormTrack(duration)
            labelPlay = (
                title + LANG["listen_point"][Disk.lang] + str(int(duration / 1000))
            )
            cellB12.config(to=int(duration / 1000), label=labelPlay)
            cursor.set(cardA.cursorTrack)
            cursorSegment.set(cardA.cursorSegment)
            cellB9.delete(0, END)
            typeTrack = FORMAT_AUDIO[cardA.listTrack[ind][1]][5]
            if typeTrack == "ma" or typeTrack == "na":  # case assembly
                cardA.assembly = True
                cardA.indAssembly = ind
                cellC10.config(state="normal")
                cellG9.config(state="normal")
                cellF10.config(state="normal")
                cellC9.config(state="normal")
                cellD9.config(state="normal")
                cellA9.config(state="disabled")
                cellF9.config(state="normal")
                cellD10.config(state="normal")
                cellG10.config(state="normal")
                listAssembly = cardA.segmentAssembly()
                cardA.listAssembly = listAssembly
                cardA.assembly = True
                cardA.indAssembly = ind
                for p in listAssembly:
                    cellB9.insert(END, p[4])
                cellB9.selection_set(0)
                cellB9.see(0)
                inSegment()
            else:
                cardA.assembly = False
                cardA.indAssembly = -1
            if cardA.readSaveCut(ind):
                cellC13.config(state="normal")
            else:
                cellC13.config(state="disabled")
        elif Disk.view == "B":
            if ind == cardB.indTrack:  # same track looking
                cursor.set(cardB.cursorTrack)
                cursorSegment.set(cardB.cursorSegment)
            else:
                cursor.set(0)
                cardB.cursorTrack = 0
                cursorSegment.set(30)
                cardB.cursorSegment = 30
                cardB.indTrack = ind
            if len(cardB.listTrack) - cardB.indTrack == 2:
                cellG13.config(state="normal")
            else:
                cellG13.config(state="disabled")
            title = cardB.listTrack[ind][5]
            trackTitle.set(title)
            trackDay.set(cardB.listTrack[ind][4][0])
            trackMonth.set(cardB.listTrack[ind][4][1])
            trackYear.set(cardB.listTrack[ind][4][2])
            trackHour.set(cardB.listTrack[ind][4][3])
            trackMin.set(cardB.listTrack[ind][4][4])
            duration = cardB.listTrack[ind][7]
            trackDur = Disk.durFormTrack(duration)
            labelPlay = (
                title + LANG["listen_point"][Disk.lang] + str(int(duration / 1000))
            )
            cellB12.config(to=int(duration / 1000), label=labelPlay)
            cursor.set(cardB.cursorTrack)
            cursorSegment.set(cardB.cursorSegment)
            cellB9.delete(0, END)
            typeTrack = FORMAT_AUDIO[cardB.listTrack[ind][1]][5]
            if typeTrack == "ma" or typeTrack == "na":  # case assembly
                cardB.assembly = True
                cardB.indAssembly = ind
                cellC10.config(state="normal")
                cellF10.config(state="normal")
                cellG9.config(state="normal")
                cellC9.config(state="normal")
                cellD9.config(state="normal")
                cellA9.config(state="disabled")
                cellF9.config(state="normal")
                cellD10.config(state="normal")
                cellG10.config(state="normal")
                listAssembly = cardB.segmentAssembly()
                cardB.listAssembly = listAssembly
                cardB.assembly = True
                cardB.indAssembly = ind
                for p in listAssembly:
                    cellB9.insert(END, p[4])
                cellB9.selection_set(0)
                cellB9.see(0)
                inSegment()
            else:
                cardB.assembly = False
                cardB.indAssembly = -1
            if cardB.readSaveCut(ind):
                cellC13.config(state="normal")
            else:
                cellC13.config(state="disabled")
        cellF7.config(text=LANG["duration_track"][Disk.lang] + trackDur)
    except IndexError:
        messagebox.showinfo(LANG["title"][Disk.lang], LANG["select_err"][Disk.lang])
        return False


def exportNFS():
    try:
        if Disk.view == "A":
            result, title, data = cardA.exportTrackNFS()
        elif Disk.view == "B":
            result, title, data = cardB.exportTrackNFS()
        if result:
            pathExport = filedialog.askdirectory()
            os.chdir(pathExport)
            nameFile = title + ".nfs"
            fw = open(nameFile, "w+b")
            fw.write(data)
            fw.close
            messagebox.showinfo(LANG["title"][Disk.lang], LANG["export_ok"][Disk.lang])
        else:
            messagebox.showinfo(LANG["title"][Disk.lang], LANG["export_no"][Disk.lang])
    except IndexError:
        messagebox.showinfo(LANG["title"][Disk.lang], LANG["select_err"][Disk.lang])
        return False


def exportMp3():
    try:
        if Disk.view == "A":
            result, title, data = cardA.exportTrackNFS()
        elif Disk.view == "B":
            result, title, data = cardB.exportTrackNFS()
        if result:
            pathExport = filedialog.askdirectory()
            os.chdir(pathExport)
            nameFile = title + ".mp2"
            fw = open(nameFile, "w+b")
            fw.write(data[HEAD:])
            fw.close()
            nameFileMp3 = title + ".mp3"
            createMp3 = [
                "ffmpeg",
                "-loglevel",
                "-8",
                "-i",
                nameFile,
                "-acodec",
                "libmp3lame",
                "-b:a",
                "192k",
                "-y",
                nameFileMp3,
            ]
            sub = subprocess.run(createMp3, stdout=PIPE, stderr=STDOUT)
            os.remove(nameFile)
            messagebox.showinfo(LANG["title"][Disk.lang], LANG["export_ok"][Disk.lang])
        else:
            messagebox.showinfo(LANG["title"][Disk.lang], LANG["export_no"][Disk.lang])
    except IndexError:
        messagebox.showinfo(LANG["title"][Disk.lang], LANG["select_err"][Disk.lang])
        return False


def copyNFS():
    try:
        if Disk.view == "A":
            result, title, data = cardA.exportTrackNFS()
            if result:
                status = cardB.writeToAB(data)
            else:
                status = False
        elif Disk.view == "B":
            result, title, data = cardB.exportTrackNFS()
            if result:
                status = cardA.writeToAB(data)
            else:
                status = False
        if status:
            messagebox.showinfo(LANG["title"][Disk.lang], LANG["export_ok"][Disk.lang])
        else:
            messagebox.showinfo(LANG["title"][Disk.lang], LANG["export_no"][Disk.lang])
    except IndexError:
        messagebox.showinfo(LANG["title"][Disk.lang], LANG["select_err"][Disk.lang])
        return False


def analysisTrack():
    if Disk.view == "A":
        if cardA.assembly:
            cardA.indTrack = cardA.indAssembly
        message = cardA.listTrack[cardA.indTrack][5] + "\n\n"  # title
        result, gap, remain, commentType = cardA.typeTrack()
    elif Disk.view == "B":
        if cardB.assembly:
            cardB.indTrack = cardB.indAssembly
        message = cardB.listTrack[cardB.indTrack][5] + "\n\n"
        result, gap, remain, commentType = cardB.typeTrack()
    message += commentType
    if result:
        messagebox.showinfo(LANG["analysis_track"][Disk.lang], message)
        if gap > 0:
            messagebox.showinfo(LANG["gap_track"][Disk.lang], message)
    else:
        message += "\n" + LANG["cut_track"][Disk.lang]
        cuttingTrack = messagebox.askyesno(LANG["analysis_track"][Disk.lang], message)
        if cuttingTrack:
            if Disk.view == "A":
                cardA.cutTrack(remain)
            if Disk.view == "B":
                cardB.cutTrack(remain)
        if Disk.view == "A":
            diskA()
        if Disk.view == "B":
            diskB()


def importNFS():
    try:
        trackSound = filedialog.askopenfilename(
            title=LANG["open_NFS"][Disk.lang],
            filetypes=[("nfs", ".nfs"), ("NFS", ".NFS")],
        )
        chemin = os.path.dirname(trackSound)
        os.chdir(chemin)
        with open(trackSound, "rb", buffering=0) as fr:
            fr.seek(0)
            data = bytearray(fr.read(SECTOR))
            long = Disk.decNbBytes(data[2:6])
            fr.seek(0)
            data = bytearray(fr.read(long))
            if Disk.view == "A":
                status, message = cardA.copyTrackNFS(long, data)
                if status:
                    diskA()
                else:
                    messagebox.showinfo(
                        LANG["import_track"][Disk.lang],
                        trackSound
                        + "\n\n"
                        + message
                        + "\n\n"
                        + LANG["import_no"][Disk.lang],
                    )
            elif Disk.view == "B":
                status, message = cardB.copyTrackNFS(long, data)
                if status:
                    diskB()
                else:
                    messagebox.showinfo(
                        LANG["import_track"][Disk.lang],
                        trackSound
                        + "\n\n"
                        + message
                        + "\n\n"
                        + LANG["import_no"][Disk.lang],
                    )

    except:
        return


def importAudio():
    trackSound = filedialog.askopenfilename(
        title=LANG["open_track"][Disk.lang],
        filetypes=[
            ("All Files", ".*"),
            ("mp2", ".mp2"),
            ("MP2", ".MP2"),
            ("mp3", ".mp3"),
            ("MP3", ".MP3"),
            ("wav", ".wav"),
            ("WAV", ".WAV"),
        ],
    )
    pathSound = os.path.dirname(trackSound)
    stampNewTrack = str(datetime.datetime.fromtimestamp(os.stat(trackSound).st_mtime))
    os.chdir(home_folder)
    trackSoundMP2 = "FileConverted.mp2"
    createMp2 = [
        "ffmpeg",
        "-loglevel",
        "-8",
        "-i",
        trackSound,
        "-ar",
        "48000",
        "-b:",
        "192k",
        "-y",
        trackSoundMP2,
    ]
    sub = subprocess.run(createMp2, stdout=PIPE, stderr=STDOUT)
    titleNewTrack = (os.path.splitext(trackSound)[0]).upper().rsplit("/", 1)[1]
    status = importTrack(trackSoundMP2, titleNewTrack, stampNewTrack)
    os.remove(trackSoundMP2)
    os.chdir(pathSound)
    return


def importTrack(trackSound, titleNewTrack, stampNewTrack):
    try:
        with open(trackSound, "rb", buffering=0) as fr:
            year = Disk.intHex(int(stampNewTrack[2:4]))
            month = Disk.intHex(int(stampNewTrack[5:7]))
            day = Disk.intHex(int(stampNewTrack[8:10]))
            hour = Disk.intHex(int(stampNewTrack[11:13]))
            minute = Disk.intHex(int(stampNewTrack[14:16]))
            stamp = [minute, hour, day, month, year]
            fr.seek(0)
            data = bytearray(fr.read(SECTOR * SEEK))
            result, message, gap, sizeFrame, codeFound = Disk.detailTrackAudio(data)
            sizeFile = os.path.getsize(trackSound)
            fr.seek(0)
            dataImport = bytearray(fr.read(sizeFile))
            if result:
                if Disk.view == "A":
                    status, message = cardA.createNewTrack(
                        codeFound, sizeFrame, titleNewTrack, stamp, dataImport[gap:]
                    )
                    if status:
                        diskA()
                elif Disk.view == "B":
                    status, message = cardB.createNewTrack(
                        codeFound, sizeFrame, titleNewTrack, stamp, dataImport
                    )
                    if status:
                        diskB()
            else:
                messagebox.showinfo(
                    LANG["import_track"][Disk.lang],
                    trackSound
                    + "\n\n"
                    + message
                    + "\n\n"
                    + LANG["import_no"][Disk.lang],
                )
            fr.close()
        return True
    except:
        return False


def cancelCut():
    if Disk.view == "A":
        if cardA.cancelCutTrack():
            diskA()
            analysisTrack()
    elif Disk.view == "B":
        if cardB.cancelCutTrack():
            diskB()
            analysisTrack()


def eraseTrack():
    if Disk.view == "A":
        cardA.delTrack()
        cardA.indTrack -= 1
        diskA()
    elif Disk.view == "B":
        cardB.delTrack()
        cardB.indTrack -= 1
        diskB()


def cancelErase():
    if Disk.view == "A":
        cardA.cancelDelTrack()
        diskA()
    elif Disk.view == "B":
        cardB.cancelDelTrack()
        diskB()


def recoveryTrack():
    if Disk.view == "A":
        if cardA.recovery():
            diskA()
            analysisTrack()
        else:
            messagebox.showinfo(LANG["title"][Disk.lang], LANG["endDisk"][Disk.lang])
    elif Disk.view == "B":
        if cardB.recovery():
            diskB()
            analysisTrack()
        else:
            messagebox.showinfo(LANG["title"][Disk.lang], LANG["endDisk"][Disk.lang])


def cursorCut():
    if Disk.view == "A":
        ind = cardA.indTrack
        track = cardA.listTrack[ind]
        point = cursor.get()
        if point == 0 or point == int(track[7] / 1000):
            return False
        remainTrack = track[2] - (HEAD + track[6])
        durFrame = FORMAT_AUDIO[track[1]][2]
        sizeFrame = FORMAT_AUDIO[track[1]][1]
        remainMilliSeconds = track[7] - point * 1000
        remain = int(remainMilliSeconds / durFrame) * sizeFrame + remainTrack
        status = cardA.cutTrack(remain)
        diskA()
        analysisTrack()
        return status
    elif Disk.view == "B":
        ind = cardB.indTrack
        track = cardB.listTrack[ind]
        point = cursor.get()
        if point == 0 or point == int(track[7] / 1000):
            return False
        remainTrack = track[2] - (HEAD + track[6])
        durFrame = FORMAT_AUDIO[track[1]][2]
        sizeFrame = FORMAT_AUDIO[track[1]][1]
        remainMilliSeconds = track[7] - point * 1000
        remain = int(remainMilliSeconds / durFrame) * sizeFrame + remainTrack
        status = cardB.cutTrack(remain)
        diskB()
        analysisTrack()
        return status


def play():
    os.chdir(home_folder)
    if Disk.view == "A":
        track = cardA.listTrack[cardA.indTrack]
        cardA.cursorTrack = cursor.get()
        cardA.cursorSegment = cursorSegment.get()
        status, title = cardA.playSegment(track)
    elif Disk.view == "B":
        cardB.cursorTrack = cursor.get()
        cardB.cursorSegment = cursorSegment.get()
        track = cardB.listTrack[cardB.indTrack]
        status, title = cardB.playSegment(track)
    if status:
        return True
    else:
        messagebox.showinfo(title, LANG["listen_no"][Disk.lang])


def updateCursorTrack(event):
    if Disk.view == "A":
        cardA.cursorTrack = cursor.get()
        if cardA.assembly:
            cellB13.config(state="disabled")
            cellC13.config(state="disabled")
        else:
            cellB13.config(state="normal")
            cellC13.config(state="normal")
    elif Disk.view == "B":
        cardB.cursorTrack = cursor.get()
        if cardB.assembly:
            cellB13.config(state="disabled")
            cellC13.config(state="disabled")
        else:
            cellB13.config(state="normal")
            cellC13.config(state="normal")


def updateDurSegment(event):
    if Disk.view == "A":
        cardA.cursorSegment = cursorSegment.get()
    elif Disk.view == "B":
        cardB.cursorSegment = cursorSegment.get()


def inSegment():
    try:
        index = cellB9.curselection()[0]
        if Disk.view == "A":
            curTrack, title, duration = cardA.cursorAssembly(index, "in")
            cardA.outPlay = False
        elif Disk.view == "B":
            curTrack, title, duration = cardB.cursorAssembly(index, "in")
            cardB.outPlay = False
        labelPlay = title + LANG["listen_point"][Disk.lang] + str(duration)
        cellB12.config(to=duration, label=labelPlay)
        cursor.set(curTrack)
    except:
        return False


def inSetSegment():
    try:
        index = cellB9.curselection()[0]
        if Disk.view == "A":
            cardA.cursorTrack = cursor.get()
            cardA.cursorSegment = cursorSegment.get()
            cardA.setAssembly(index, "setIn")
            cardA.segmentAssembly()
            diskA()
        elif Disk.view == "B":
            cardB.cursorTrack = cursor.get()
            cardB.cursorSegment = cursorSegment.get()
            cardB.setAssembly(index, "setIn")
            cardB.segmentAssembly()
            diskB()
        cellB9.selection_clear(0, END)
        cellB9.selection_set(index)
        cellB9.see(index)
        inSegment()
    except IndexError:
        messagebox.showinfo(LANG["title"][Disk.lang], LANG["select_err"][Disk.lang])
        return False


def outSegment():
    try:
        index = cellB9.curselection()[0]
        if Disk.view == "A":
            curTrack, title, duration = cardA.cursorAssembly(index, "out")
            cardA.outPlay = True
        elif Disk.view == "B":
            curTrack, title, duration = cardB.cursorAssembly(index, "out")
            cardB.outPlay = True
        labelPlay = title + LANG["listen_point"][Disk.lang] + str(duration)
        cellB12.config(to=duration, label=labelPlay)
        cursor.set(curTrack)
    except:
        return False


def outSetSegment():
    try:
        index = cellB9.curselection()[0]
        if Disk.view == "A":
            cardA.cursorTrack = cursor.get()
            cardA.cursorSegment = cursorSegment.get()
            cardA.setAssembly(index, "setOut")
            cardA.segmentAssembly()
            diskA()
        elif Disk.view == "B":
            cardB.cursorTrack = cursor.get()
            cardB.cursorSegment = cursorSegment.get()
            cardB.setAssembly(index, "setOut")
            cardB.segmentAssembly()
            diskB()
        cellB9.selection_clear(0, END)
        cellB9.selection_set(index)
        cellB9.see(index)
        outSegment()
    except IndexError:
        messagebox.showinfo(LANG["title"][Disk.lang], LANG["select_err"][Disk.lang])
        return False


def allSetSegment():
    try:
        index = cellB9.curselection()[0]
        if Disk.view == "A":
            indTrack = cardA.listAssembly[index][0]
            endSegment = cardA.listTrack[indTrack][7]
        elif Disk.view == "B":
            indTrack = cardB.listAssembly[index][0]
            endSegment = cardB.listTrack[indTrack][7]
        cursorEnd = round(endSegment / 1000, 1)
        cellB12.config(to=int(cursorEnd))
        cursor.set(cursorEnd)
        outSetSegment()
        cursor.set(0)
        inSetSegment()
    except IndexError:
        messagebox.showinfo(LANG["title"][Disk.lang], LANG["select_err"][Disk.lang])
        return False


def equalSetSegment():
    try:
        index = cellB9.curselection()[0]
        if Disk.view == "A":
            indTrack = cardA.listAssembly[index][0]
            endSegment = cardA.listTrack[indTrack][7]
        elif Disk.view == "B":
            indTrack = cardB.listAssembly[index][0]
            endSegment = cardB.listTrack[indTrack][7]
        cursorEnd = round(endSegment / 1000, 1)
        cellB12.config(to=int(cursorEnd))
        cursorMed = round(endSegment / 2000, 1)
        cursor.set(cursorMed)
        outSetSegment()
        cursor.set(cursorMed)
        inSetSegment()
    except IndexError:
        messagebox.showinfo(LANG["title"][Disk.lang], LANG["select_err"][Disk.lang])
        return False


def addSegment():
    if Disk.view == "A":
        try:
            indTrack = cellB3.curselection()[0]
            if cardA.indAssembly == indTrack:
                indTrack = cardA.listAssembly[0][0]
        except:
            indTrack = cardA.listAssembly[0][0]
        status = cardA.setAssembly(indTrack, "add")
        cardA.indTrack = cardA.indAssembly
        index = len(cardA.listAssembly)
        diskA()
    elif Disk.view == "B":
        try:
            indTrack = cellB3.curselection()[0]
            if cardB.indAssembly == indTrack:
                indTrack = cardB.listAssembly[0][0]
        except:
            indTrack = cardB.listAssembly[0][0]
        status = cardB.setAssembly(indTrack, "add")
        cardB.indTrack = cardA.indAssembly
        index = len(cardB.listAssembly)
        diskB()
    cellB9.selection_clear(0, END)
    cellB9.selection_set(index)
    cellB9.see(index)
    inSegment()
    if not status:
        messagebox.showinfo(
            LANG["assembly_track"][Disk.lang], LANG["segment_add_no"][Disk.lang]
        )


def delSegment():
    if Disk.view == "A":
        status = cardA.setAssembly(0, "del")
        cardA.indTrack = cardA.indAssembly
        cardA.segmentAssembly()
        diskA()
    elif Disk.view == "B":
        indTrack = cardB.listAssembly[0][0]
        status = cardB.setAssembly(indTrack, "del")
        cardB.indTrack = cardB.indAssembly
        cardB.segmentAssembly()
        diskB()


def makeAssembly():
    indTrack = cellB3.curselection()[0]
    if Disk.view == "A":
        status = cardA.setAssembly(indTrack, "make")
        diskA()
    elif Disk.view == "B":
        status = cardB.setAssembly(indTrack, "make")
        diskB()
    cellB9.selection_set(0)
    cellB9.see(0)
    inSegment()


#
# -----------------------------------------------------------
#                   DEBUT DU SCRIPT
# -----------------------------------------------------------
#
cardA = Disk("A")
cardB = Disk("B")
#
# -----------------------------------------------------------
#                 INTERFACE GRAPHIQUE
# -----------------------------------------------------------
#
# Création de la fenêtre principale (main window)
bay = Tk()
bay.title(f"AdminNFS v.{VERS} - " + LANG["title"][Disk.lang])

FR = PhotoImage(file=script_dir + "/FR.png")
UK = PhotoImage(file=script_dir + "/UK.png")
NAGRA = PhotoImage(file=script_dir + "/NagraAres-C.png")
ICONE = PhotoImage(file=script_dir + "/ModuloNagra.png")

fontMedium = ("Arial", 12)
fontGreat = ("Arial", 20, "bold")

bay.configure(bg=COLOR[Disk.view])
bay.iconphoto(False, ICONE)
# ----------LIGNE 00 -----------------
cellA0 = Button(
    bay,
    image=FR,
    anchor="w",
    command=langFR,
    bg=BUTTON,
)
cellA0.grid(column=0, row=0, sticky=N + E + S + W)
cellB0 = Button(
    bay,
    text=LANG["physicDisk"][Disk.lang],
    command=resetDisk,
    bg=BUTTON,
)
cellB0.grid(column=1, row=0, columnspan=5, sticky=N + E + S + W)
cellG0 = Button(
    bay,
    image=UK,
    anchor="e",
    command=langUK,
    bg=BUTTON,
)
cellG0.grid(column=6, row=0, sticky=N + E + S + W)
# ----------LIGNE 01 -----------------
cellA1 = Button(
    bay, text="A", command=diskA, font=fontGreat, bg=COLOR["A"], borderwidth=0
)
cellA1.grid(column=0, row=1, sticky=W + E + N + S)
cellB1 = Listbox(bay, height=3, selectmode="single", bg=SCREEN)
cellB1.grid(column=1, row=1, padx=5, pady=5, columnspan=5, sticky=W + E)
cellB1.bind("<Double-1>", affectAB)
cellG1 = Button(
    bay, text="B", command=diskB, font=fontGreat, bg=COLOR["B"], borderwidth=0
)
cellG1.grid(column=6, row=1, sticky=W + E + N + S)
# ----------LIGNE 02 -----------------
cellA2 = Button(
    bay,
    text=LANG["edit_tit"][Disk.lang],
    command=editHeadDisk,
    bg=BUTTON,
    state="disabled",
)
cellA2.grid(column=0, row=2, sticky=W + E + N + S)
titDisk = StringVar()
cellB2 = Entry(bay, width=35, textvariable=titDisk, bg=SCREEN)
cellB2.grid(column=1, row=2, padx=5, sticky=W)
cellC2 = Label(bay, text="", bg=COLOR[Disk.view])
cellC2.grid(column=2, columnspan=4, row=2, padx=5, sticky=E)
cellG2 = ttk.Progressbar(bay)
cellG2.grid(column=6, row=2, sticky=W + E)
# ----------LIGNE 03 -----------------
cellA3 = Button(
    bay,
    text=LANG["details_track"][Disk.lang],
    command=lookTrack,
    bg=BUTTON,
)
cellA3.grid(column=0, row=3, sticky=W + E)
cellB3 = Listbox(bay, selectmode="single", bg=SCREEN)
cellB3.grid(column=1, row=3, rowspan=4, columnspan=5, padx=5, sticky=N + E + S + W)
cellB3.bind("<Double-1>", lambda x: cellA3.invoke())
cellG3 = Button(
    bay,
    text=LANG["exportNFS_track"][Disk.lang],
    command=exportNFS,
    bg=BUTTON,
)
cellG3.grid(column=6, row=3, sticky=W + E)
# ----------LIGNE 04 -----------------
cellA4 = Button(
    bay,
    text=LANG["add_track"][Disk.lang],
    command=importNFS,
    bg=BUTTON,
)
cellA4.grid(column=0, row=4, sticky=W + E)
cellG4 = Button(
    bay,
    text=LANG["copy_toB"][Disk.lang],
    command=copyNFS,
    bg=BUTTON,
)
cellG4.grid(column=6, row=4, sticky=W + E)
# ----------LIGNE 05 -----------------
cellA5 = Button(
    bay,
    text=LANG["import_track"][Disk.lang],
    command=importAudio,
    bg=BUTTON,
)
cellA5.grid(column=0, row=5, sticky=W + E)
cellG5 = Button(
    bay,
    text=LANG["export_mp3"][Disk.lang],
    command=exportMp3,
    bg=BUTTON,
)
cellG5.grid(column=6, row=5, sticky=W + E)
# ----------LIGNE 06 -----------------
cellA6 = Button(
    bay,
    text=LANG["erase_track"][Disk.lang],
    command=eraseTrack,
    bg=CAUTION,
    state="disabled",
)
cellA6.grid(column=0, row=6, sticky=W + E)
cellG6 = Button(
    bay,
    text=LANG["cancel_erase"][Disk.lang],
    command=cancelErase,
    bg=CAUTION,
    width=20,
    state="disabled",
)
cellG6.grid(column=6, row=6, sticky=W + E)
# ----------LIGNE 07 -----------------
cellB7 = Label(
    bay, text=LANG["title_track"][Disk.lang], bg=COLOR[Disk.view], state="disabled"
)
cellB7.grid(column=1, row=7, sticky=W)
cellC7 = Label(
    bay, text=LANG["time_track"][Disk.lang], bg=COLOR[Disk.view], state="disabled"
)
cellC7.grid(column=2, row=7, sticky=E)
trackHour = StringVar()
cellD7 = Entry(bay, width=2, textvariable=trackHour, bg=SCREEN)
cellD7.grid(column=3, row=7, sticky=W)
trackMin = StringVar()
cellE7 = Entry(bay, width=2, textvariable=trackMin, bg=SCREEN)
cellE7.grid(column=4, row=7, sticky=W)
cellF7 = Label(bay, width=10, text="", bg=COLOR[Disk.view])
cellF7.grid(column=5, row=7, sticky=W)
cellG7 = Button(
    bay,
    text=LANG["analysis_track"][Disk.lang],
    command=analysisTrack,
    bg=BUTTON,
)
cellG7.grid(column=6, row=7, sticky=W + E + N + S)
# ----------LIGNE 08 -----------------
cellA8 = Button(
    bay,
    text=LANG["edit_head"][Disk.lang],
    command=editHeadTrack,
    bg=BUTTON,
)
cellA8.grid(column=0, row=8, sticky=W + E + N + S)
trackTitle = StringVar()
cellB8 = Entry(bay, width=38, textvariable=trackTitle, bg=SCREEN)
cellB8.grid(column=1, row=8, padx=5, sticky=W)
cellC8 = Label(
    bay, text=LANG["day_track"][Disk.lang], bg=COLOR[Disk.view], state="disabled"
)
cellC8.grid(column=2, row=8, sticky=E)
trackDay = StringVar()
cellD8 = Entry(bay, width=2, textvariable=trackDay, bg=SCREEN)
cellD8.grid(column=3, row=8, sticky=W)
trackMonth = StringVar()
cellE8 = Entry(bay, width=2, textvariable=trackMonth, bg=SCREEN)
cellE8.grid(column=4, row=8, sticky=W)
trackYear = StringVar()
cellF8 = Entry(bay, width=2, textvariable=trackYear, bg=SCREEN)
cellF8.grid(column=5, row=8, sticky=W)
# ----------LIGNE 09 -----------------
cellA9 = Button(
    bay,
    text=LANG["assembly_set"][Disk.lang],
    command=makeAssembly,
    bg=BUTTON,
)
cellA9.grid(column=0, row=9, sticky=W + E)
cellB9 = Listbox(bay, height=4, selectmode="single", borderwidth=0, bg=SCREEN)
cellB9.grid(column=1, row=9, padx=5, pady=5, rowspan=3, sticky=W + E)
cellB9.bind("<Double-1>", lambda x: cellC10.invoke())
cellC9 = Button(
    bay,
    text="in◄-",
    font=fontMedium,
    command=inSetSegment,
    bg=BUTTON,
)
cellC9.grid(column=2, row=9, padx=5, sticky=W + E)
cellD9 = Button(
    bay,
    text="◄-►",
    font=fontMedium,
    command=allSetSegment,
    bg=BUTTON,
)
cellD9.grid(column=3, row=9, columnspan=2, sticky=W + E)
cellF9 = Button(
    bay,
    text="-►out",
    font=fontMedium,
    command=outSetSegment,
    bg=BUTTON,
)
cellF9.grid(column=5, row=9, padx=5, sticky=W + E)
cellG9 = Button(
    bay,
    text=LANG["segment_add"][Disk.lang],
    command=addSegment,
    bg=BUTTON,
)
cellG9.grid(column=6, row=9, columnspan=2, sticky=W + E)
# ----------LIGNE 10 -----------------
cellA10 = Label(image=NAGRA, bg=COLOR[Disk.view])
cellA10.grid(column=0, row=10, sticky=W + E)
cellC10 = Button(
    bay,
    text=LANG["segment_in"][Disk.lang],
    font=fontMedium,
    command=inSegment,
    bg=BUTTON,
)
cellC10.grid(column=2, row=10, padx=5, sticky=W + E)
cellD10 = Button(
    bay,
    text="-►◄-",
    font=fontMedium,
    command=equalSetSegment,
    bg=BUTTON,
)
cellD10.grid(column=3, row=10, columnspan=2, sticky=W + E)
cellF10 = Button(
    bay,
    text=LANG["segment_out"][Disk.lang],
    font=fontMedium,
    command=outSegment,
    bg=BUTTON,
)
cellF10.grid(column=5, row=10, padx=5, sticky=W + E)
cellG10 = Button(
    bay,
    text=LANG["segment_del"][Disk.lang],
    command=delSegment,
    bg=CAUTION,
)
cellG10.grid(column=6, row=10, columnspan=2, sticky=W + E)
# ----------LIGNE 11 -----------------
# ----------LIGNE 12 -----------------
cellA12 = Button(
    bay,
    text=LANG["listen"][Disk.lang],
    font=fontMedium,
    command=play,
    bg=BUTTON,
)
cellA12.grid(column=0, row=12, sticky=W + E + S)
cursor = DoubleVar()
cellB12 = Scale(
    bay,
    variable=cursor,
    orient=HORIZONTAL,
    from_=0,
    to=100,
    resolution=0.1,
    label=LANG["listen_point"][Disk.lang],
    bg=COLOR["A"],
    troughcolor=SCREEN,
    bd=1,
)
cellB12.bind("<ButtonRelease-1>", updateCursorTrack)
cellB12.grid(column=1, row=12, columnspan=5, sticky=W + E)
cursorSegment = DoubleVar()
cellG12 = Scale(
    bay,
    variable=cursorSegment,
    orient=HORIZONTAL,
    from_=5,
    to=60,
    resolution=1,
    label=LANG["duration_point"][Disk.lang],
    bg=COLOR["A"],
    troughcolor=SCREEN,
    bd=1,
)
cellG12.bind("<ButtonRelease-1>", updateDurSegment)
cellG12.grid(column=6, row=12, sticky=W + E)
# ----------LIGNE 13 -----------------
cellA13 = Button(
    bay,
    text=LANG["quit"][Disk.lang],
    command=bay.destroy,
    fg="red",
    bg=BUTTON,
)
cellA13.grid(column=0, row=13, pady=10, sticky=W + E)
cellB13 = Button(
    bay,
    text=LANG["cursor_cut"][Disk.lang],
    command=cursorCut,
    bg=CAUTION,
    state="disabled",
    width=31,
)
cellB13.grid(column=1, row=13, sticky=W)
cellC13 = Button(
    bay,
    text=LANG["save_cut"][Disk.lang],
    command=cancelCut,
    bg=CAUTION,
    state="disabled",
    width=31,
)
cellC13.grid(column=2, row=13, columnspan=4, sticky=E)
cellG13 = Button(
    bay,
    text=LANG["recovery_track"][Disk.lang],
    command=recoveryTrack,
    bg=CAUTION,
    state="disabled",
)
cellG13.grid(column=6, row=13, sticky=W + E)

# ------------- FIN ------------------
resetDisk()
bay.mainloop()
