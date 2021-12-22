import struct, json, zlib

print("JD14 MUSICTRACK SERIALIZER BY: JACKLSUMMER15")

codename=input("Enter your mapname: ")
codenamelow=codename.lower()

outputdirectory='output/'+codename
try:
    os.makedirs(outputdirectory)

except:
    pass

mt=json.load(open("input/"+codenamelow+"_musictrack.tpl.ckd"))

header=struct.pack(">I",1)
header+=struct.pack(">I",int((166*len(mt["COMPONENTS"][0]["trackData"]["structure"]["markers"]))+166))
header+=b'\x1B\x85\x7B\xCE\x00\x00\x00\xAC\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x88\x3A\x7E\x00\x00\x00\xB4\x00\x00\x00\xA4\x00\x00\x00\x48'
beats=struct.pack(">I",len(mt["COMPONENTS"][0]["trackData"]["structure"]["markers"]))
for beat in mt["COMPONENTS"][0]["trackData"]["structure"]["markers"]:
    beats+=struct.pack(">I",beat)
signatures=struct.pack(">I",len(mt["COMPONENTS"][0]["trackData"]["structure"]["signatures"]))
for signature in mt["COMPONENTS"][0]["trackData"]["structure"]["signatures"]:
    signatures+=struct.pack(">i",8)
    signatures+=struct.pack(">i",signature["marker"])
    signatures+=struct.pack(">i",signature["beats"])
sections=struct.pack(">I",len(mt["COMPONENTS"][0]["trackData"]["structure"]["sections"]))
for section in mt["COMPONENTS"][0]["trackData"]["structure"]["sections"]:
    sections+=struct.pack(">i",20)
    sections+=struct.pack(">i",section["marker"])
    sections+=struct.pack(">i",section["sectionType"])
    sections+=struct.pack(">i",len(section["comment"]))
    sections+=section["comment"].encode()
components=struct.pack(">i",mt["COMPONENTS"][0]["trackData"]["structure"]["startBeat"])
components+=struct.pack(">I",mt["COMPONENTS"][0]["trackData"]["structure"]["endBeat"])
components+=struct.pack(">f",mt["COMPONENTS"][0]["trackData"]["structure"]["videoStartTime"])
filename=[mt["COMPONENTS"][0]["trackData"]["path"].replace(mt["COMPONENTS"][0]["trackData"]["path"].split("/")[-1],"").replace("maps","jd5").replace("jd2015","jd5"),mt["COMPONENTS"][0]["trackData"]["path"].split("/")[-1]]
components+=struct.pack(">I",len(filename[0]))
components+=filename[0].encode()
components+=struct.pack(">I",len(filename[1]))
components+=filename[1].encode()
components+=struct.pack("<I",zlib.crc32(filename[1].encode()))
for index in range(2):
    components+=struct.pack(">I",0)

enc=open(outputdirectory+"/"+codenamelow+"_musictrack.tpl.ckd","wb")
enc.write(header)
enc.write(beats)
enc.write(signatures)
enc.write(sections)
enc.write(components)
enc.close()