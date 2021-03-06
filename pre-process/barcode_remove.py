
#!/usr/bin/env python3
'''
Title: barcode_remove
Author:Yixun Huang
Description:
    This is a barcode-removing appoach of sequencing libraries generated by the 5’-RACE technology. TAC-Gn (no matter how many Gs it has) 
    at 5' will be cilpped. The clipped sequence will be printed into a new fastq file. The sequences will not be printed in the output file 
    if they do not have the barcode (TACGGG).
Usage:
    ./barcode_remove.py sample2.fastq filtered_sample.fastq
'''
import sys
record={}
idlist=[]
seq=[]
barcode=['TACGGG']
with open(sys.argv[1],'r') as fin:
    memory= []
    counter=1
    for line in fin:
        line=line.rstrip()
        if counter%4 == 1:
            if counter== 1:
                idlist.append(line)
            else:
                seq.append(memory)
                idlist.append(line)
                memory=[]
        else:
            memory.append(line)
        counter+=1
    seq.append(memory)
    record=dict(zip(idlist,seq))
with open(sys.argv[2],'w') as out:
    remove_seq = 0
    for id in idlist:
        seqline = record[id][0].upper() # So the barcode also matches lowercase sequence
        qualid = record[id][1]
        qualline = record[id][2]
        pos = seqline.find(barcode[0], 0, 40)
        if pos != -1:
            No_G=len(seqline[pos+6:])-len(seqline[pos+6:].lstrip('G'))
            out.write('{}\n{}\n{}\n{}\n'.format(id, seqline[pos+6:].lstrip('G'), qualid, qualline[pos+6+No_G:]))
        else:
            remove_seq+=1
  
