import struct, json, os

codename=input("Enter a map to decrypt: ")
codenamelow=codename.lower()

f = open("input/"+codenamelow+"pm.tpl.ckd","rb")

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

    altclassentry = f.read(4)
    print(altclassentry)

    if altclassentry == b'\x00\x00\x00\x04':

        f.read(4)

        len_alt1songname = struct.unpack('>I', f.read(4))[0]

        alt1songname = f.read(len_alt1songname).decode("utf-8")

        alt1jdversion = struct.unpack('>I', f.read(4))[0]

        alt1firstbeat = struct.unpack('>i', f.read(4))[0]

        alt1lastbeat = struct.unpack('>I', f.read(4))[0]

        alt1songswitch = struct.unpack('>I', f.read(4))[0]

        alt1videooff1 = struct.unpack('>f', f.read(4))[0]

        alt1videooff2 = struct.unpack('>f', f.read(4))[0]

        alt1videoscale = struct.unpack('>f', f.read(4))[0]

        len_alt1movename=struct.unpack('>I', f.read(4))[0]

        alt1movename=f.read(len_alt1movename).decode("utf-8")

        alt1blockclip={"__class":"AltBlock1","songName":alt1songname,"jdVersion": alt1jdversion,"frstBeat":alt1firstbeat,"lastBeat":alt1lastbeat,"songSwitch":alt1songswitch,"videoCoachOffset":[alt1videooff1,alt1videooff2],"videoCoachScale":alt1videoscale,"danceStepName":alt1movename}

        print(alt1blockclip)

        mutpl["COMPONENTS"][0]["BlockDescriptorVector"].append(alt1blockclip)

        f.read(4)

        len_alt2songname = struct.unpack('>I', f.read(4))[0]

        alt2songname = f.read(len_alt2songname).decode("utf-8")

        alt2jdversion = struct.unpack('>I', f.read(4))[0]

        alt2firstbeat = struct.unpack('>i', f.read(4))[0]

        alt2lastbeat = struct.unpack('>I', f.read(4))[0]

        alt2songswitch = struct.unpack('>I', f.read(4))[0]

        alt2videooff1 = struct.unpack('>f', f.read(4))[0]

        alt2videooff2 = struct.unpack('>f', f.read(4))[0]

        alt2videoscale = struct.unpack('>f', f.read(4))[0]

        len_alt2movename=struct.unpack('>I', f.read(4))[0]

        alt2movename=f.read(len_alt2movename).decode("utf-8")

        alt2blockclip={"__class":"AltBlock2","songName":alt2songname,"jdVersion": alt2jdversion,"frstBeat":alt2firstbeat,"lastBeat":alt2lastbeat,"songSwitch":alt2songswitch,"videoCoachOffset":[alt2videooff1,alt2videooff2],"videoCoachScale":alt2videoscale,"danceStepName":alt2movename}

        print(alt2blockclip)

        mutpl["COMPONENTS"][0]["BlockDescriptorVector"].append(alt2blockclip)

        f.read(4)

        len_alt3songname = struct.unpack('>I', f.read(4))[0]

        alt3songname = f.read(len_alt3songname).decode("utf-8")

        alt3jdversion = struct.unpack('>I', f.read(4))[0]

        alt3firstbeat = struct.unpack('>i', f.read(4))[0]

        alt3lastbeat = struct.unpack('>I', f.read(4))[0]

        alt3songswitch = struct.unpack('>I', f.read(4))[0]

        alt3videooff1 = struct.unpack('>f', f.read(4))[0]

        alt3videooff2 = struct.unpack('>f', f.read(4))[0]

        alt3videoscale = struct.unpack('>f', f.read(4))[0]

        len_alt3movename=struct.unpack('>I', f.read(4))[0]

        alt3movename=f.read(len_alt3movename).decode("utf-8")

        alt3blockclip={"__class":"AltBlock3","songName":alt3songname,"jdVersion": alt3jdversion,"frstBeat":alt3firstbeat,"lastBeat":alt3lastbeat,"songSwitch":alt3songswitch,"videoCoachOffset":[alt3videooff1,alt3videooff2],"videoCoachScale":alt3videoscale,"danceStepName":alt3movename}

        print(alt3blockclip)

        mutpl["COMPONENTS"][0]["BlockDescriptorVector"].append(alt3blockclip)

        f.read(4)

        len_alt4songname = struct.unpack('>I', f.read(4))[0]

        alt4songname = f.read(len_alt4songname).decode("utf-8")

        alt4jdversion = struct.unpack('>I', f.read(4))[0]

        alt4firstbeat = struct.unpack('>i', f.read(4))[0]

        alt4lastbeat = struct.unpack('>I', f.read(4))[0]

        alt4songswitch = struct.unpack('>I', f.read(4))[0]

        alt4videooff1 = struct.unpack('>f', f.read(4))[0]

        alt4videooff2 = struct.unpack('>f', f.read(4))[0]

        alt4videoscale = struct.unpack('>f', f.read(4))[0]

        len_alt4movename=struct.unpack('>I', f.read(4))[0]

        alt4movename=f.read(len_alt4movename).decode("utf-8")

        alt4blockclip={"__class":"AltBlock4","songName":alt4songname,"jdVersion": alt4jdversion,"frstBeat":alt4firstbeat,"lastBeat":alt4lastbeat,"songSwitch":alt4songswitch,"videoCoachOffset":[alt4videooff1,alt4videooff2],"videoCoachScale":alt4videoscale,"danceStepName":alt4movename}

        print(alt4blockclip)

        mutpl["COMPONENTS"][0]["BlockDescriptorVector"].append(alt4blockclip)

        total = total - 1

f.close()

mudec = open("output/"+codenamelow+"pm.tpl.ckd", "w")
mudec.write(json.dumps(mutpl))
mudec.close()