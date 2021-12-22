import struct, json, os

codename=input("Enter a map to encrypt: ")
codenamelow=codename.lower()

with open(codenamelow+"mu.tpl.ckd") as f:
    tape=json.load(f)

enc=open("ENCRYPTED_"+codenamelow+"mu.tpl.ckd","wb")
tapecount=len(tape["COMPONENTS"][0]["BlockDescriptorVector"])
print(tapecount)
tape_version=int(tapecount*220)
#header
enc.write(b'\x00\x00\x00\x01'+struct.pack(">I",tape_version)+b'\x1B\x85\x7B\xCE\x00\x00\x00\xAC\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x5B\x64\x8E\x44\x00\x00\x00\x2C\x00\x00\x00\x01\x00\x00\x00\x00')

#blockflow tapes
tapeclips=struct.pack(">I",tapecount)
for blockflow in tape["COMPONENTS"][0]["BlockDescriptorVector"]:
    if blockflow["__class"]=="IntroBlock":
        tapeclips+=b'\x00\x00\x01\xA8\x00\x00\x01\x94'
        tapeclips+=struct.pack(">I",len(blockflow["songName"]))+blockflow["songName"].encode()
        tapeclips+=struct.pack(">I",blockflow["jdVersion"])
        tapeclips+=struct.pack(">I",blockflow["frstBeat"])
        tapeclips+=struct.pack(">I",blockflow["lastBeat"])
        tapeclips+=b'\x00\x00\x00\x00'
        tapeclips+=struct.pack(">f",blockflow["videoCoachOffset"][0])
        tapeclips+=struct.pack(">f",blockflow["videoCoachOffset"][1])
        tapeclips+=struct.pack(">f",blockflow["videoCoachScale"])
        tapeclips+=b'\x00\x00\x00\x00\x00\x00\x00\x00'

    if blockflow["__class"]=="BaseBlock":
        tapeclips+=b'\x00\x00\x01\xA8\x00\x00\x01\x94'
        tapeclips+=struct.pack(">I",len(blockflow["songName"]))+blockflow["songName"].encode()
        tapeclips+=struct.pack(">I",blockflow["jdVersion"])
        tapeclips+=struct.pack(">I",blockflow["frstBeat"])
        tapeclips+=struct.pack(">I",blockflow["lastBeat"])
        tapeclips+=b'\x00\x00\x00\x00'
        tapeclips+=struct.pack(">f",blockflow["videoCoachOffset"][0])
        tapeclips+=struct.pack(">f",blockflow["videoCoachOffset"][1])
        tapeclips+=struct.pack(">f",blockflow["videoCoachScale"])
        tapeclips+=struct.pack(">I",len(blockflow["danceStepName"]))+blockflow["danceStepName"].encode()

    if blockflow["__class"]=="AltBlock":
        tapeclips+=b'\x00\x00\x00\x01\x00\x00\x01\x94'
        tapeclips+=struct.pack(">I",len(blockflow["songName"]))+blockflow["songName"].encode()
        tapeclips+=struct.pack(">I",blockflow["jdVersion"])
        tapeclips+=struct.pack(">I",blockflow["frstBeat"])
        tapeclips+=struct.pack(">I",blockflow["lastBeat"])
        tapeclips+=b'\x00\x00\x00\x00'
        tapeclips+=struct.pack(">f",blockflow["videoCoachOffset"][0])
        tapeclips+=struct.pack(">f",blockflow["videoCoachOffset"][1])
        tapeclips+=struct.pack(">f",blockflow["videoCoachScale"])
        tapeclips+=struct.pack(">I",len(blockflow["danceStepName"]))+blockflow["danceStepName"].encode()

enc.write(tapeclips)
enc.write(b'\x00\x00\x00\x00')