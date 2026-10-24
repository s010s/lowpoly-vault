# SPDX-License-Identifier: MIT
"""One purposeful underside QA view with the canonical studio lights mirrored below.
The four standard views retain the unmodified canonical illumination.
"""
import hashlib,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as r
r.DIRECTIONS['ventral']=(0,-90)
original_look=r._look_at
original_save=r.save_json
def look(obj,target):
    if obj.type=='LIGHT':obj.location.z=target.z-abs(obj.location.z-target.z)
    original_look(obj,target)
def save(path,value):
    if path.name=='render-config.json':
        value['adapter_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        value['lighting_note']='One canonical underside anatomy diagnostic; key and fill Z directions mirrored below subject to reveal walking and gill branches.'
        for light in value['lights']:light['direction'][2]=-abs(light['direction'][2])
        value['lighting']['lights']=value['lights']
    original_save(path,value)
r._look_at=look;r.save_json=save
r.main()
