"""Refresh image checksums while retaining supplied-deck media identities."""
import csv,hashlib,json
from pathlib import Path
def refresh(root):
 root=Path(root);p=root/'slide_image_map.json';rows=json.loads(p.read_text())
 for r in rows:
  r.setdefault('embedded_image_sha256',r['image_sha256']);r['image_sha256']=hashlib.sha256((root/r['figure']).read_bytes()).hexdigest()
 p.write_text(json.dumps(rows,indent=2))
 with (root/'slide_image_map.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
if __name__=='__main__':refresh(Path(__file__).resolve().parents[1])
