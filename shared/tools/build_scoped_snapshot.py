#!/usr/bin/env python3
from pathlib import Path
import argparse, shutil, json, hashlib

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("source",type=Path); ap.add_argument("target",choices=["writer","article-creator"]); ap.add_argument("destination",type=Path); a=ap.parse_args()
 if a.destination.exists(): shutil.rmtree(a.destination)
 a.destination.mkdir(parents=True)
 for name in ["knowledge","strategy","evidence","patterns","quality","learning","validation","docs"]: shutil.copytree(a.source/name,a.destination/name)
 shutil.copy2(a.source/"README.md",a.destination/"README.md"); shutil.copy2(a.source/"LICENSE",a.destination/"LICENSE"); shutil.copy2(a.source/"VERSION",a.destination/"VERSION"); shutil.copy2(a.source/"CHANGELOG.md",a.destination/"CHANGELOG.md")
 mapping=a.source/"mappings"/a.target/"application-mapping.md"
 shutil.copytree(a.source/"mappings"/a.target,a.destination/"mappings"/a.target)
 flat={"intent-analysis.md":"Intent-Analysis.md","hidden-anxiety.md":"Hidden-Anxiety.md","evidence-transparency.md":"Evidence-Transparency.md","serp-entity-preservation.md":"SERP-Entity-Preservation.md","internal-link-semantics.md":"Internal-Link-Semantics.md","decision-support.md":"Decision-Support.md"}
 for src,dst in flat.items(): shutil.copy2(a.source/"knowledge"/src,a.destination/dst)
 shutil.copy2(mapping,a.destination/("Writer-Application-Mapping.md" if a.target=="writer" else "Article-Creator-Application-Mapping.md"))
 ver=(a.source/"VERSION").read_text(encoding="utf-8").strip()
 product="SIMS Writer" if a.target=="writer" else "SIMS Article Creator"
 (a.destination/"SOURCE.md").write_text(f"# Snapshot Source\n\nSource: SIMS-Shared-Editorial-Knowledge\nIntegrated for: {product} {ver}\n",encoding="utf-8")
 scope={"target_product":a.target,"source_version":ver,"integrated_version":ver,"included_mapping":a.target,"excluded_mapping":"article-creator" if a.target=="writer" else "writer"}
 (a.destination/"SNAPSHOT_SCOPE.json").write_text(json.dumps(scope,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 files=[]
 for p in sorted(a.destination.rglob("*")):
  if p.is_file() and p.name!="SNAPSHOT_MANIFEST.json": files.append({"path":p.relative_to(a.destination).as_posix(),"sha256":sha(p)})
 manifest={"source_repository":"SIMS-Shared-Editorial-Knowledge","source_version":ver,"integrated_version":ver,"target_product":a.target,"files":files}
 (a.destination/"SNAPSHOT_MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__": main()
