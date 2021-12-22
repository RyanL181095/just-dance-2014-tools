import os, json, struct, zlib, io
from unidecode import unidecode
print("JD14 TAPE SERIALIZER BY: JACKLSUMMER15")

try:
    os.mkdir('input')
    os.mkdir('output')

    os.makedirs('input/msm')
    os.makedirs('input/gesture')

except:
    pass

codename=input("Enter your mapname: ")
codenamelow=codename.lower()

outputdirectory='output/'+codename
try:
    os.makedirs(outputdirectory)

except:
    pass

#reading layer id inputs
layerid=json.load(open("layerid.json"))

#timeline.tpl serialzing process
dtape=json.load(io.open("input/"+codenamelow+"_tml_dance.dtape.ckd",'r',encoding="utf-8"))

try:
    ktape=json.load(io.open("input/"+codenamelow+"_tml_karaoke.ktape.ckd",'r',encoding="utf-8"))

except:
    pass

timelinetpl={
    "pictos": [],
    "moves": [],
    "kinectmoves": [],
    "lyrics": [],
    "blocks": [],
    "pictoModels": [],
    "moveModels": [],
    "kinectmoveModels": [],
    "blockModels": [],
    "karaokedata": []
}

print('converting tapes...')

try:
    for ktape_clips in ktape["Clips"]:
        kstarttime=ktape_clips["StartTime"]/24
        kduration=ktape_clips["Duration"]/24
        lyric=unidecode(ktape_clips["Lyrics"])
        islineending=ktape_clips["IsEndOfLine"]

        timelinetpl["lyrics"].append(
        {
        "__class": "LyricClip",
        "text": lyric,
        "layerID": layerid["layers"][0]["Lyrics"],
        "startPosition": kstarttime,
        "stopPosition": kstarttime+kduration,
        "isLineEnding": islineending
        })
except:
    pass

try:
    for karaokedata in ktape["Clips"]:
        kstarttime=karaokedata["StartTime"]/24
        kduration=karaokedata["Duration"]/24
        kpitch=karaokedata["Pitch"]/4

        timelinetpl["karaokedata"].append(
            {
            "__class": "SignalAnnotation",
            "startTime": kstarttime/2,
            "pitch": kpitch,
            "endTime": kstarttime+kduration/2,
            "tolerance": {
                "__class": "TolerancePitchTime",
                "startTime":kstarttime/2-0.099998,
                "semitoneTolerance": 5.0,
                "endTime": kstarttime+kduration/2-0.099998
                }
            })
except:
    pass

for dtape_clips in dtape["Clips"]:
    if dtape_clips["__class"] == "GoldEffectClip":
        goldframestarttime=dtape_clips["StartTime"]/24
        goldframeduration=dtape_clips["Duration"]/24

        if dtape_clips["EffectType"]==1 or dtape_clips["EffectType"]==0:
            timelinetpl["blocks"].append(
            {
            "modelName": "goldmove",
            "layerID": layerid["layers"][0]["Events_0"],
            "startPosition": goldframestarttime,
            "stopPosition": goldframestarttime+goldframeduration
            })

        elif dtape_clips["EffectType"]==2:
            timelinetpl["blocks"].append(
            {
            "modelName": "goldmovecascade",
            "layerID": layerid["layers"][0]["Events_0"],
            "startPosition": goldframestarttime,
            "stopPosition": goldframestarttime+goldframeduration
            })

    if dtape_clips["__class"]=="PictogramClip":
        pictostarttime=dtape_clips["StartTime"]/24
        pictogrampath=dtape_clips["PictoPath"]

        timelinetpl["pictos"].append(
        {
        "__class": "PictoClip",
        "position": pictostarttime,
        "pictoname": pictogrampath.replace("world/maps/"+codenamelow+"/timeline/pictos/","").replace(".png","").replace("world/database/jd0/"+codenamelow+"/timeline/pictos/","").replace("world/database/jd1/"+codenamelow+"/timeline/pictos/","").replace("world/database/jd2/"+codenamelow+"/timeline/pictos/","").replace("world/database/jd3/"+codenamelow+"/timeline/pictos/","").replace("world/database/jd4/"+codenamelow+"/timeline/pictos/","").replace("world/database/jd5/"+codenamelow+"/timeline/pictos/","").replace(".tga","").capitalize(),
        "texturePath": pictogrampath.replace("maps","jd5"),
        "layerID": layerid["layers"][0]["Pictos"]
        })

    if dtape_clips["__class"]=="MotionClip":
        if dtape_clips["ClassifierPath"].endswith('.msm'):
            msmstarttime=dtape_clips["StartTime"]/24
            msmduration=dtape_clips["Duration"]/24
            msmgoldmove=dtape_clips["GoldMove"]
            msmpath=dtape_clips["ClassifierPath"]

            if dtape_clips["CoachId"]==0:
                coachid=layerid["layers"][0]["Moves1"]

            if dtape_clips["CoachId"]==1:
                coachid=layerid["layers"][0]["Moves2"]

            if dtape_clips["CoachId"]==2:
                coachid=layerid["layers"][0]["Moves3"]

            if dtape_clips["CoachId"]==3:
                coachid=layerid["layers"][0]["Moves4"]

            timelinetpl["moves"].append(
            {
            "__class": "MoveClip",
            "moveName": msmpath.replace("world/maps/"+codenamelow+"/timeline/moves/"+codenamelow+"_","").replace("world/database/jd0/"+codenamelow+"/timeline/moves/"+codenamelow+"_","").replace("world/database/jd1/"+codenamelow+"/timeline/moves/"+codenamelow+"_","").replace("world/database/jd2/"+codenamelow+"/timeline/moves/"+codenamelow+"_","").replace("world/database/jd3/"+codenamelow+"/timeline/moves/"+codenamelow+"_","").replace("world/database/jd4/"+codenamelow+"/timeline/moves/"+codenamelow+"_","").replace("world/database/jd5/"+codenamelow+"/timeline/moves/"+codenamelow+"_","").replace(".msm","").replace(".gesture","").capitalize(),
            "layerID": coachid,
            "classifierPath": msmpath.replace("maps","jd5"),
            "startPosition": msmstarttime,
            "stopPosition": msmstarttime+msmduration,
            "goldMove": msmgoldmove
            })
    
        if dtape_clips["ClassifierPath"].endswith('.gesture'):
            gesturestarttime=dtape_clips["StartTime"]/24
            gestureduration=dtape_clips["Duration"]/24
            gesturegoldmove=dtape_clips["GoldMove"]
            gesturepath=dtape_clips["ClassifierPath"]

            if dtape_clips["CoachId"]==0:
                coachid=layerid["layers"][0]["KinectMoves1"]

            if dtape_clips["CoachId"]==1:
                coachid=layerid["layers"][0]["KinectMoves2"]

            if dtape_clips["CoachId"]==2:
                coachid=layerid["layers"][0]["KinectMoves3"]

            if dtape_clips["CoachId"]==3:
                coachid=layerid["layers"][0]["KinectMoves4"]

            timelinetpl["kinectmoves"].append(
            {
            "__class": "MoveClip",
            "moveName": gesturepath.replace("world/maps/"+codenamelow+"/timeline/moves/"+codenamelow+"_","").replace("world/database/jd0/"+codenamelow+"/timeline/moves/"+codenamelow+"_","").replace("world/database/jd1/"+codenamelow+"/timeline/moves/"+codenamelow+"_","").replace("world/database/jd2/"+codenamelow+"/timeline/moves/"+codenamelow+"_","").replace("world/database/jd3/"+codenamelow+"/timeline/moves/"+codenamelow+"_","").replace("world/database/jd4/"+codenamelow+"/timeline/moves/"+codenamelow+"_","").replace("world/database/jd5/"+codenamelow+"/timeline/moves/"+codenamelow+"_","").replace(".msm","").replace(".gesture","").capitalize(),
            "layerID": coachid,
            "classifierPath": gesturepath.replace("maps","jd5"),
            "startPosition": gesturestarttime,
            "stopPosition": gesturestarttime+gestureduration,
            "goldMove": gesturegoldmove
            })

# json.dump(timelinetpl,open(outputdirectory+'/timeline.json',"w")) #if you want to check out the deserialized timeline.

try:
    for movemodel_clips in os.listdir("input/msm"):

        with open("input/msm/"+movemodel_clips,'rb')as f: # modifying the msms

            try:
                os.makedirs(outputdirectory+'/msm')

            except:
                pass

            msmake=open(outputdirectory+'/msm/'+movemodel_clips,'wb')

            msmake.write(f.read(4))

            f.read(4) # change 00000007 to 00000005

            msmake.write(b'\x00\x00\x00\x05')

            msmake.write(f.read(128)) # rest of the header

            f.read(15)# Acc_Dev_Dir_NP

            msmake.write(b'\x41\x63\x63\x5F\x44\x65\x76\x5F\x44\x69\x72\x5F\x31\x30\x50')

            msmake.write(f.read(57))

            msmake.write(b'\x3F\x80\x00\x00\x21\x1C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

            f.read(24)

            msmake.write(f.read())# the rest of the msm data

    for msmname in os.listdir(outputdirectory+"/msm"):

        msmblock_name = msmname.replace(codename + '_', '').replace(codenamelow + '_', '').replace('.msm', '').replace('.gesture','')
        timelinetpl["moveModels"].append({
        "__class": "TimelineModelMove",
        "name": msmblock_name.capitalize()
        })

except:
    pass

try:
    for kinectmovemodel_clips in os.listdir("input/gesture"):

        with open("input/gesture/"+kinectmovemodel_clips,'rb')as f: 

            try:
                os.makedirs(outputdirectory+'/gesture')

            except:
                pass

            gestmake=open(outputdirectory+'/gesture/'+kinectmovemodel_clips,'wb')

            gestmake.write(f.read())

        gestureblock_name=kinectmovemodel_clips.replace(codename+'_','').replace(codenamelow+'_','').replace('.msm', '').replace('.gesture','')
        timelinetpl["kinectmoveModels"].append(
        {
        "__class": "TimelineKinectModelMove",
        "name": gestureblock_name.capitalize()
        })

except:
    pass

print('serializing converted tapes...')

lyric=struct.pack(">I",len(timelinetpl["lyrics"]))
for ktape in timelinetpl["lyrics"]:
    if ktape["__class"]=="LyricClip":
        lyric+=b'\x00\x00\x00\x30'
        lyric+=struct.pack(">I",len(ktape["text"]))+ktape["text"].encode()
        lyric+=struct.pack(">I",ktape["layerID"])+struct.pack(">I",ktape["isLineEnding"])
        lyric+=struct.pack(">f",ktape["startPosition"])
        lyric+=struct.pack(">f",ktape["stopPosition"])

ksd=struct.pack(">I",len(timelinetpl["karaokedata"]))
for karaokescoredata in timelinetpl["karaokedata"]:
    ksd+=b'\x00\x00\x00\x2C'
    ksd+=struct.pack(">f",karaokescoredata["startTime"])
    ksd+=struct.pack(">f",karaokescoredata["endTime"])
    ksd+=struct.pack(">f",karaokescoredata["pitch"])
    ksd+=b'\x00\x00\x00\x00\x00\x00\x00\x18'
    ksd+=struct.pack(">f",karaokescoredata["tolerance"]["endTime"])
    ksd+=struct.pack(">f",karaokescoredata["tolerance"]["startTime"])
    ksd+=b'\x00\x00\x00\x00\x00\x00\x00\x00'
    ksd+=struct.pack(">f",karaokescoredata["tolerance"]["semitoneTolerance"])

pict=struct.pack(">I",len(timelinetpl["pictos"]))
for picto in timelinetpl["pictos"]:
    if picto["__class"]=="PictoClip":
        pictoname=[picto["texturePath"].replace(picto["texturePath"].split("/")[-1],""),picto["texturePath"].split("/")[-1]]
        pict+=b'\x00\x00\x00\xA0'
        pict+=struct.pack(">f",picto["position"])
        pict+=struct.pack(">I",len(picto["pictoname"]))+picto["pictoname"].encode()
        pict+=struct.pack(">f",picto["layerID"])
        pict+=struct.pack(">I",len(pictoname[0]))+pictoname[0].encode()
        pict+=struct.pack(">I",len(pictoname[1]))+pictoname[1].encode()
        pict+=struct.pack("<I",zlib.crc32(pictoname[1].encode()))+struct.pack(">I",0)

msm=struct.pack(">I",len(timelinetpl["moves"]))
for move in timelinetpl["moves"]:
    if move["__class"]=="MoveClip":
        movename=[move["classifierPath"].replace(move["classifierPath"].split("/")[-1],""),move["classifierPath"].split("/")[-1]]
        msm+=b'\x00\x00\x00\x9C'
        msm+=struct.pack(">I",len(move["moveName"]))+move["moveName"].encode()
        msm+=struct.pack(">I",move["layerID"])
        msm+=struct.pack(">I",len(movename[0]))+movename[0].encode()
        msm+=struct.pack(">I",len(movename[1]))+movename[1].encode()
        msm+=struct.pack("<I",zlib.crc32(movename[1].encode()))+struct.pack(">I",0)
        msm+=struct.pack(">f",move["startPosition"])
        msm+=struct.pack(">f",move["stopPosition"])
        msm+=struct.pack(">I",move["goldMove"])+struct.pack(">I",0)+struct.pack(">I",0)+struct.pack(">I",0)

movemodel=struct.pack(">I",len(timelinetpl["moveModels"]))
movevalue=1000000
for model in timelinetpl["moveModels"]:
    if model["__class"]=="TimelineModelMove":
        movemodel+=b'\x00\x00\x00\x4C'
        movemodel+=struct.pack(">I",len(model["name"]))+model["name"].encode()
        movemodel+=b'\x00\x00\x00\x05\x00\x00\x00\x02'
        movemodel+=struct.pack(">f",movevalue)
        movemodel+=b'\x3F\x8C\xCC\xCD\x3F\x8C\xCC\xCD\x3F\x8C\xCC\xCD\x3F\x80\x00\x00\x3F\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        movevalue+=int(15)

gesture=struct.pack(">I",len(timelinetpl["kinectmoves"]))
for kinectmove in timelinetpl["kinectmoves"]:
    if kinectmove["__class"]=="MoveClip":
        kinectmovename=[kinectmove["classifierPath"].replace(kinectmove["classifierPath"].split("/")[-1],""),kinectmove["classifierPath"].split("/")[-1]]
        gesture+=b'\x00\x00\x00\x9C'
        gesture+=struct.pack(">I",len(kinectmove["moveName"]))+kinectmove["moveName"].encode()
        gesture+=struct.pack(">I",kinectmove["layerID"])
        gesture+=struct.pack(">I",len(kinectmovename[0]))+kinectmovename[0].encode()
        gesture+=struct.pack(">I",len(kinectmovename[1]))+kinectmovename[1].encode()
        gesture+=struct.pack("<I",zlib.crc32(kinectmovename[1].encode()))+struct.pack(">I",0)
        gesture+=struct.pack(">f",kinectmove["startPosition"])
        gesture+=struct.pack(">f",kinectmove["stopPosition"])
        gesture+=struct.pack(">I",kinectmove["goldMove"])+struct.pack(">I",0)+struct.pack(">I",0)+struct.pack(">I",0)

kinectmovemodel=struct.pack(">I",len(timelinetpl["kinectmoveModels"]))
kinectmovevalue=1000000
for kinectmodel in timelinetpl["kinectmoveModels"]:
    if kinectmodel["__class"]=="TimelineKinectModelMove":
        kinectmovemodel+=b'\x00\x00\x00\x74'
        kinectmovemodel+=struct.pack(">I",len(kinectmodel["name"]))+kinectmodel["name"].encode()
        kinectmovemodel+=b'\x00\x00\x00\x02\x00\x00\x00\x02'
        kinectmovemodel+=struct.pack(">I",movevalue)
        kinectmovemodel+=b'\x3F\x8C\xCC\xCD\x3F\x8C\xCC\xCD\x3F\x8C\xCC\xCD\x3F\x80\x00\x00\x3F\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3F\x80\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3F\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        kinectmovevalue+=int(15)

goldmovetext="GoldMove"
goldmovetextlow=goldmovetext.lower()
gmcascade="GoldMoveCascade"
gmcascadelow=gmcascade.lower()
frame=struct.pack(">I",len(timelinetpl["blocks"]))
for block in timelinetpl["blocks"]:
    if block["modelName"]=="goldmove":
        frame+=b'\x00\x00\x00\x5C'
        frame+=struct.pack(">I",0)
        frame+=struct.pack(">f",block["startPosition"])
        frame+=struct.pack(">f",block["stopPosition"])
        frame+=struct.pack(">I",block["layerID"])
        frame+=struct.pack(">I",len(goldmovetextlow))+goldmovetextlow.encode()
        frame+=b'\x00\xC0\xC0\xC0\x00\x00\x00\x01\x49\x69\x58\x69\x00\x00\x00\x18'
        frame+=struct.pack(">I",len(goldmovetext))+goldmovetext.encode()

    if block["modelName"]=="goldmovecascade":
        frame+=b'\x00\x00\x00\x5C'
        frame+=struct.pack(">I",0)
        frame+=struct.pack(">f",block["startPosition"])
        frame+=struct.pack(">f",block["stopPosition"])
        frame+=struct.pack(">I",block["layerID"])
        frame+=struct.pack(">I",len(gmcascadelow))+gmcascadelow.encode()
        frame+=b'\x00\xC0\xC0\xC0\x00\x00\x00\x00'

#combining all of the tapes into one file

finalenc=open(outputdirectory+"/timeline.tpl.ckd","wb")

#intro part
tape_version=int((166*len(timelinetpl["pictos"]+timelinetpl["moves"]+timelinetpl["kinectmoves"]+timelinetpl["lyrics"]+timelinetpl["blocks"]+timelinetpl["pictoModels"]+timelinetpl["moveModels"]+timelinetpl["kinectmoveModels"]+timelinetpl["blockModels"]+timelinetpl["karaokedata"]))+166)

finalenc.write(b'\x00\x00\x00\x01'+struct.pack(">I",tape_version)+b'\x1B\x85\x7B\xCE\x00\x00\x00\xAC\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x10\x9F\xBC\x33\x00\x00\x01\x9C')
finalenc.write(struct.pack(">I",len(codename))+codename.encode())

#karaoke data and shit
finalenc.write(b'\x00\x00\x00\x38\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x50\x00\x00\x00\x38\x00\x00\x01\x00\x00\x00\x01\x00\x42\xC8\x00\x00\x3F\x33\x33\x33\x3F\x66\x66\x66\x3F\x40\x00\x00\x42\xB4\x00\x00\x44\x61\x00\x00\x00\x00\x00\x0A\x00\x00\x00\x07\x3F\x4C\xCC\xCD\x00\x00\x00\x00\x00\x00\x00\x00')

finalenc.write(pict)
finalenc.write(msm)
finalenc.write(gesture)
finalenc.write(lyric)
finalenc.write(frame)

#serializing your layerid inputs

id_count=struct.pack(">I",len(layerid["layers"][0]))

try:
    lyricid=layerid["layers"][0]["Lyrics"]#lyrics
    id_count+=b'\x00\x00\x00\x2C'
    id_count+=b'\x00\x00\x00\x0F'
    id_count+=struct.pack(">I",len("Lyrics"))+"Lyrics".encode()
    id_count+=struct.pack(">I",0)+struct.pack(">I",lyricid)
    id_count+=b'\x00\x57\x80\xCD'
except:
    pass

try:
    moves1=layerid["layers"][0]["Moves1"]#moves1
    id_count+=b'\x00\x00\x00\x2C'
    id_count+=b'\x00\x00\x00\x0D'
    id_count+=struct.pack(">I",len("Moves1"))+"Moves1".encode()
    id_count+=struct.pack(">I",1)+struct.pack(">I",moves1)
    id_count+=b'\x00\xE6\xAA\x82'
except:
    pass

try:
    moves2=layerid["layers"][0]["Moves2"]#moves2
    id_count+=b'\x00\x00\x00\x2C'
    id_count+=b'\x00\x00\x00\x0D'
    id_count+=struct.pack(">I",len("Moves2"))+"Moves2".encode()
    id_count+=struct.pack(">I",2)+struct.pack(">I",moves2)
    id_count+=b'\x00\xE6\xAA\x82'
except:
    pass

try:
    moves3=layerid["layers"][0]["Moves3"]#moves3
    id_count+=b'\x00\x00\x00\x2C'
    id_count+=b'\x00\x00\x00\x0D'
    id_count+=struct.pack(">I",len("Moves3"))+"Moves3".encode()
    id_count+=struct.pack(">I",3)+struct.pack(">I",moves3)
    id_count+=b'\x00\xE6\xAA\x82'
except:
    pass

try:
    moves4=layerid["layers"][0]["Moves4"]#moves4
    id_count+=b'\x00\x00\x00\x2C'
    id_count+=b'\x00\x00\x00\x0D'
    id_count+=struct.pack(">I",len("Moves4"))+"Moves4".encode()
    id_count+=struct.pack(">I",4)+struct.pack(">I",moves4)
    id_count+=b'\x00\xE6\xAA\x82'
except:
    pass

try:
    pictoid=layerid["layers"][0]["Pictos"]#pictos
    id_count+=b'\x00\x00\x00\x2C'
    id_count+=b'\x00\x00\x00\x10'
    id_count+=struct.pack(">I",len("Pictos"))+"Pictos".encode()
    id_count+=struct.pack(">I",5)+struct.pack(">I",pictoid)
    id_count+=b'\x00\xB4\x8C\xE6'
except:
    pass

try:
    kinectmoves1=layerid["layers"][0]["KinectMoves1"]#kinectmoves1
    id_count+=b'\x00\x00\x00\x2C'
    id_count+=b'\x00\x00\x00\x0E'
    id_count+=struct.pack(">I",len("KinectMoves1"))+"KinectMoves1".encode()
    id_count+=struct.pack(">I",6)+struct.pack(">I",kinectmoves1)
    id_count+=b'\x00\x8C\xBE\x5A'
except:
    pass

try:
    kinectmoves2=layerid["layers"][0]["KinectMoves2"]#kinectmoves2
    id_count+=b'\x00\x00\x00\x2C'
    id_count+=b'\x00\x00\x00\x0E'
    id_count+=struct.pack(">I",len("KinectMoves2"))+"KinectMoves2".encode()
    id_count+=struct.pack(">I",7)+struct.pack(">I",kinectmoves2)
    id_count+=b'\x00\x8C\xBE\x5A'
except:
    pass

try:
    kinectmoves3=layerid["layers"][0]["KinectMoves3"]#kinectmoves3
    id_count+=b'\x00\x00\x00\x2C'
    id_count+=b'\x00\x00\x00\x0E'
    id_count+=struct.pack(">I",len("KinectMoves3"))+"KinectMoves3".encode()
    id_count+=struct.pack(">I",8)+struct.pack(">I",kinectmoves3)
    id_count+=b'\x00\x8C\xBE\x5A'
except:
    pass

try:
    kinectmoves4=layerid["layers"][0]["KinectMoves4"]#kinectmoves4
    id_count+=b'\x00\x00\x00\x2C'
    id_count+=b'\x00\x00\x00\x0E'
    id_count+=struct.pack(">I",len("KinectMoves4"))+"KinectMoves4".encode()
    id_count+=struct.pack(">I",9)+struct.pack(">I",kinectmoves4)
    id_count+=b'\x00\x8C\xBE\x5A'
except:
    pass

try:
    events_0=layerid["layers"][0]["Events_0"]#events_0
    id_count+=b'\x00\x00\x00\x2C'
    id_count+=b'\x00\x00\x00\x0C'
    id_count+=struct.pack(">I",len("Events_0"))+"Events_0".encode()
    id_count+=struct.pack(">I",10)+struct.pack(">I",events_0)
    id_count+=b'\x00\xA0\xA0\xA0'
except:
    pass

try:
    bpm=layerid["layers"][0]["BPM"]#bpm
    id_count+=b'\x00\x00\x00\x2C'
    id_count+=b'\x00\x00\x00\x03'
    id_count+=struct.pack(">I",len("BPM"))+"BPM".encode()
    id_count+=struct.pack(">I",11)+struct.pack(">I",bpm)
    id_count+=b'\x00\xA0\xA0\xA0'
except:
    pass

try:
    karaokescoring=layerid["layers"][0]["KaraokeScoring"]#karaokescoring
    id_count+=b'\x00\x00\x00\x2C'
    id_count+=b'\x00\x00\x00\x0E'
    id_count+=struct.pack(">I",len("KaraokeScoring"))+"KaraokeScoring".encode()
    id_count+=struct.pack(">I",12)+struct.pack(">I",karaokescoring)
    id_count+=b'\x00\xA0\xA0\xA0'
except:
    pass

finalenc.write(id_count)
finalenc.write(movemodel)
finalenc.write(kinectmovemodel)
#second gold move part
gmpart2=struct.pack(">I",len(timelinetpl["blocks"]))
for gm2 in timelinetpl["blocks"]:
    gmpart2+=b'\x00\x00\x00\x64'
    gmpart2+=struct.pack(">I",len('goldmove'))+'goldmove'.encode()
    gmpart2+=b'\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x1C\x00\x00\x00\x05\x43\x6C\x61\x73\x73\x00\x49\x69\x58\x69\x00\x00\x00\x18'
    gmpart2+=struct.pack(">I",len('GoldMove'))+'GoldMove'.encode()
finalenc.write(gmpart2)

pictomodel=struct.pack(">I",len(timelinetpl["pictoModels"]))

finalenc.write(pictomodel)

finalenc.close()