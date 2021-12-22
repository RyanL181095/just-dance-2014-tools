import json, struct
print("JD14 SONGDESC SERIALIZER BY: JACKLSUMMER15")

songdesc=json.load(open("input/songdesc.tpl.ckd"))

codename=songdesc["COMPONENTS"][0]["MapName"]
codenamelow=codename.lower()

outputdirectory='output/'+codename
try:
    os.makedirs(outputdirectory)

except:
    pass

musictrack=json.load(open("input/"+codenamelow+"_musictrack.tpl.ckd"))

enc=open(outputdirectory+"/songdesc.tpl.ckd","wb")
#header
enc.write(struct.pack(">i",1)+struct.pack(">i",5541))
enc.write(b'\x1B\x85\x7B\xCE\x00\x00\x00\xAC\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x8A\xC2\xB5\xC6\x00\x00\x01\x04')
#components
enc.write(struct.pack(">i",len(songdesc["COMPONENTS"][0]["MapName"]))+songdesc["COMPONENTS"][0]["MapName"].encode())
enc.write(b'\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x9C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x00\x00\x00\x01')
enc.write(struct.pack(">i",len(songdesc["COMPONENTS"][0]["Artist"]))+songdesc["COMPONENTS"][0]["Artist"].encode())
enc.write(struct.pack(">i",len(songdesc["COMPONENTS"][0]["Title"]))+songdesc["COMPONENTS"][0]["Title"].encode())
enc.write(struct.pack(">I",songdesc["COMPONENTS"][0]["NumCoach"]))
enc.write(struct.pack(">I",songdesc["COMPONENTS"][0]["Difficulty"]))
enc.write(b'\x00\x00\x00\x01\x3F\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x10\x6F\x40\x37\xD0')
enc.write(struct.pack(">I",musictrack["COMPONENTS"][0]["trackData"]["structure"]["previewEntry"]))
enc.write(b'\x00\x00\x01\x24\x00\x00\x00\x10\xB1\x1F\xC1\xB6')
enc.write(struct.pack(">I",musictrack["COMPONENTS"][0]["trackData"]["structure"]["previewLoopStart"]))
enc.write(struct.pack(">I",musictrack["COMPONENTS"][0]["trackData"]["structure"]["previewLoopEnd"]))
enc.write(b'\x00\x00\x00\x02\x31\xD3\xB3\x47')
for element in [songdesc["COMPONENTS"][0]["DefaultColors"]["lyrics"][3],
                songdesc["COMPONENTS"][0]["DefaultColors"]["lyrics"][2],
                songdesc["COMPONENTS"][0]["DefaultColors"]["lyrics"][1],
                songdesc["COMPONENTS"][0]["DefaultColors"]["lyrics"][0]]:
    enc.write(struct.pack(">f",element))
enc.write(b'\x9C\xD9\x0B\xCB\x3F\x80\x00\x00\x3F\x80\x00\x00\x00\x00\x00\x00\x3F\x80\x00\x00\x00\x00\x00\x00')

enc.close()