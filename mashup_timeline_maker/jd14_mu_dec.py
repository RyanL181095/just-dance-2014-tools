import struct, json, os

codename=input("Enter a map to decrypt: ")
codenamelow=codename.lower()

f = open("input/"+codenamelow+"mu.tpl.ckd","rb")

mutpl={
    "__class": "Actor_Template",
    "WIP": 0,
    "LOWUPDATE": 0,
    "UPDATE_LAYER": 0,
    "PROCEDURAL": 0,
    "STARTPAUSED": 0,
    "FORCEISENVIRONMENT": 0,
    "COMPONENTS": [{
            "__class": "JD_BlockFlowTemplate",
            "IsMashUp": 1,
            "IsPartyMaster": 0,
            "BlockDescriptorVector": []}]}

#header
f.read(64)

#info
maptapes = struct.unpack('>I', f.read(4))[0]
print(maptapes)

total = maptapes *2

#intro part
f.read(8)

len_introsongname = struct.unpack('>I', f.read(4))[0]

introsongname = f.read(len_introsongname).decode("utf-8")

introjdversion = struct.unpack('>I', f.read(4))[0]

introfirstbeat = struct.unpack('>i', f.read(4))[0]

introlastbeat = struct.unpack('>i', f.read(4))[0]

introsongswitch = struct.unpack('>I', f.read(4))[0]

introvideooff1 = struct.unpack('>f', f.read(4))[0]

introvideooff2 = struct.unpack('>f', f.read(4))[0]

introvideoscale = struct.unpack('>f', f.read(4))[0]

f.read(8)

introclip={"__class":"IntroBlock","songName": introsongname,"jdVersion": introjdversion,"frstBeat": introfirstbeat,"lastBeat": introlastbeat,"songSwitch": introsongswitch,"videoCoachOffset": [introvideooff1, introvideooff2],"videoCoachScale": introvideoscale,"danceStepName": ""}

mutpl["COMPONENTS"][0]["BlockDescriptorVector"].append(introclip)

for x in range(maptapes):
    #base input
    baseclassentry = f.read(8)
    print(baseclassentry)

    if baseclassentry == b'\x00\x00\x01\xA8\x00\x00\x01\x94':
        len_basesongname = struct.unpack('>I', f.read(4))[0]

        basesongname = f.read(len_basesongname).decode("utf-8")

        basejdversion = struct.unpack('>I', f.read(4))[0]

        basefirstbeat = struct.unpack('>i', f.read(4))[0]

        baselastbeat = struct.unpack('>I', f.read(4))[0]

        basesongswitch = struct.unpack('>I', f.read(4))[0]

        basevideooff1 = struct.unpack('>f', f.read(4))[0]

        basevideooff2 = struct.unpack('>f', f.read(4))[0]

        basevideoscale = struct.unpack('>f', f.read(4))[0]

        len_basemovename=struct.unpack('>I', f.read(4))[0]

        basemovename=f.read(len_basemovename).decode("utf-8")

        baseblockclip={"__class":"BaseBlock","songName": basesongname,"jdVersion": basejdversion,"frstBeat": basefirstbeat,"lastBeat": baselastbeat,"songSwitch": basesongswitch,"videoCoachOffset": [basevideooff1, basevideooff2],"videoCoachScale": basevideoscale,"danceStepName": basemovename}

        print(baseblockclip)

        mutpl["COMPONENTS"][0]["BlockDescriptorVector"].append(baseblockclip)

    #replacing parts

    altclassentry = f.read(8)
    print(altclassentry)

    if altclassentry == b'\x00\x00\x00\x01\x00\x00\x01\x94':

        len_altsongname = struct.unpack('>I', f.read(4))[0]

        altsongname = f.read(len_altsongname).decode("utf-8")

        altjdversion = struct.unpack('>I', f.read(4))[0]

        altfirstbeat = struct.unpack('>i', f.read(4))[0]

        altlastbeat = struct.unpack('>I', f.read(4))[0]

        altsongswitch = struct.unpack('>I', f.read(4))[0]

        altvideooff1 = struct.unpack('>f', f.read(4))[0]

        altvideooff2 = struct.unpack('>f', f.read(4))[0]

        altvideoscale = struct.unpack('>f', f.read(4))[0]

        len_altmovename=struct.unpack('>I', f.read(4))[0]

        altmovename=f.read(len_altmovename).decode("utf-8")

        altblockclip={"__class":"AltBlock","songName":altsongname,"jdVersion": altjdversion,"frstBeat":altfirstbeat,"lastBeat":altlastbeat,"songSwitch":altsongswitch,"videoCoachOffset":[altvideooff1,altvideooff2],"videoCoachScale":altvideoscale,"danceStepName":altmovename}

        print(altblockclip)

        mutpl["COMPONENTS"][0]["BlockDescriptorVector"].append(altblockclip)

        total = total - 1

f.close()

mudec = open("output/"+codenamelow+"mu.tpl.ckd", "w")
mudec.write(json.dumps(mutpl))
mudec.close()