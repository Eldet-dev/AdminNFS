Nagra digital recorders manufactured from 1995 onwards made it possible to create files on a compact flash card in a proprietary format: Nagra File System (NFS), files that are therefore not directly readable on today's computers. At the time of the marketing of the recorders, a program running on Windows (Ares Import) made it possible to convert these files, but this had limited functions and was not maintained.

These recorders still work very well, have very pleasant ergonomics and have the advantage of having editing functions implemented on the device which made it possible to send the edited files to the broadcasting stations by digital telephone. The presence of two card ports also allows for copies and backups. The highest quality files are recorded in stereo with MPEG-1 Layer 2 (MP2) compression with a bitrate of 192 kb/s at 48 kHz, which is now obsolete, but listens to it, remains of excellent quality.

To allow the use of these legendary recorders nowadays, the program of this repository, developed in python, allows the manipulation of the files produced by these devices.

The program has two scripts, the main one: adminNFS manages the graphical interface in Tkinter and the second: cardCfNFS is the module that includes the NFS file format management class on the cards.

Scripts use the ffmpeg library which must be present on the computer and accessible by scripts.

The present scripts allow the manipulation of the tracks as on the Ares-C with its two PCMCIA ports: A and B and to perform operations from one to the other. 

These scripts only manipulate tracks compressed in mpeg-1 layer 2 (mp2) format, tracks in Ares-C G711 and G722 (telephone format) are not manipulable, but are displayed and simply erasable.

To access compact flash cards at a low level (at the byte level), it is imperative to run these scripts in ADMINISTRATOR MODE.

These scripts were developed by reverse engineering the NFS format, due to the lack of available sources and data manipulation software maintained as computing evolved.

Natively, these scripts have an interface in two languages: French, because Nagra manufactured these recorders in French-speaking Switzerland at the time, and in English to remain more universal. Both scripts work directly on Windows and Linux without modification (tested with Windows 10 and Xubuntu Linux).

In summary, the NFS format presents the tracks in the following way on a compact flash card: 
- a 512-byte header, the first 96 of which contain the name of the card, the date of formatting, the NAGRA name and probably the serial number of the recorder who carried out the formatting of the card;
- a suite of audio tracks and timeline tracks;
- each of these tracks has a 96-byte header with Nagra's own audio compression code;
- the size in bytes of the track (in multiples of 512 bytes, the value of a sector), the size of the editing tracks is always 512 bytes;
- the date and time of the recording;
- the title of the track;
- runway duration in milliseconds;
- after the header, there is the succession of audio frames with each their mpeg header;
- for the editing tracks after the header, there is a succession of 14-byte frames giving the physical addresses of the start and end of the chosen frames and the number of the track used in the editing, so you can only edit tracks present on the card;
- finally, a sequence of 32 bytes with a value of 255 (ff in hexadecimal) marks the end of the tracks.

The succession of tracks does not allow you to insert and delete tracks in the middle of the sequence, the deletion of one track necessarily leads to the deletion of the following ones, the addition can only be done after the last of the sequence. This is exactly the limit of the manipulations encountered on the recorders. Deleting a track by each device only manipulates the header, the track information is simply replaced by 32 bytes to 255 (ff). As a result of the multiple recordings and erasures, there are still many orphaned audio frames on the map, these scripts allow them to be recovered and given an audio track structure for possible recovery.

During a sudden power cut, the device does not have time to reflect in the header the complete track data at the time of the cut, and the device system indicates a corrupted card that can be checked by the device; The latter adds, usually at the end of the map, the end of the map tag (32 bytes to ff) and reflects the size of the track in the header of the last track, which results in an often disproportionate size of the track, thus prohibiting the addition of additional tracks. The present scripts, after analyzing the track that is too long, offer the possibility of making a cut after the last recorded audio frame, leaving behind a leftover track that can be deleted later or analyzed again.

The main manipulations that these scripts perform are: 
- display of all tracks on a map (audio and editing);
- import of audio files playable with ffmpeg;
- export of audio tracks in NFS (Nagra File System) format;
- export in mp3 format;
- the complete analysis of an audio track with decoding of the compression mode and the presence of unnecessary bytes on the track (between the header and the first audio frame and between the last frame and the end of the track);
- simple editing between tracks with export of edited tracks;
- recovering audio tracks after power is cut off during recording;
- the cutting of an audio track into two consecutive tracks with cancellation following the cut;
- erasure of consecutive audio tracks and undo of erasure as a result;
- the copy between the A and B cards and export the assemblies from one to the other.

Cutoff and erase undo use the available space on the first sector of the adapter between the adapter header and the end of the sector to save the original headers before manipulation.
