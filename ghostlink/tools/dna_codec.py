# ghostlink/tools/dna_codec.py
from __future__ import annotations
import base64
from ..runtime.context import Context

CODONS = {
    'A':'GCU','B':'GGG','C':'CUC','D':'GAU','E':'GAA','F':'UUU','G':'GGC','H':'CAC',
    'I':'AUU','J':'CAA','K':'AAA','L':'UUA','M':'AUG','N':'AAC','O':'UAA','P':'CCC',
    'Q':'CAG','R':'AGA','S':'AGC','T':'ACA','U':'UGG','V':'GUU','W':'UGU','X':'CGC',
    'Y':'UAC','Z':'GUA','1':'AAU','3':'AAG','~':'ACU','&':'ACC','^':'ACG','%':'AGU',
    '$':'AGG','.':'UGA',',':'UAG','!':'UGC','?':'UCA','-':'CGU','_':'CGG',':':'CUA',
    ';':'CUG','\'':'GAG','"':'GAC','(':'UCC',')':'UCG','[':'GCC',']':'GCG','{':'CCG',
    '}':'CGA','+':'GGA','=':'GGU','\\':'UUC','|':'CUU','<':'UAU','/':'TTT'  # fallback
}
REV = {v:k for k,v in CODONS.items()}

START_BLOCK = 'AUG'; END_BLOCK='UGA'

def _to_codon_b64(b: bytes) -> str:
    s = base64.b64encode(b).decode()
    return START_BLOCK + ''.join(CODONS.get(ch,'TTT') for ch in s) + END_BLOCK

def _from_codon_b64(s: str) -> bytes:
    if s.startswith(START_BLOCK): s = s[len(START_BLOCK):]
    if s.endswith(END_BLOCK): s = s[:-len(END_BLOCK)]
    chars = []
    for i in range(0, len(s), 3):
        tri = s[i:i+3]
        if tri in REV: chars.append(REV[tri])
    return base64.b64decode(''.join(chars))

def main(ctx: Context, mode: str, data: str):
    if mode == 'encode':
        b = data.encode()
        return {"dna": _to_codon_b64(b)}
    if mode == 'decode':
        b = _from_codon_b64(data)
        return {"text": b.decode(errors='replace')}
    return {"error": "mode must be encode|decode"}
