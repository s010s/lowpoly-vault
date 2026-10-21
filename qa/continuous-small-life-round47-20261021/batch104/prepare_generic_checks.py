from pathlib import Path
Q=Path('/workspace/shared/lowpoly-batch104-independent-qa-20261021')
old=Path('/workspace/shared/lowpoly-batch102-independent-qa-20261021/binary-audit.py').read_text()
old=old.replace("W=pathlib.Path('/workspace/shared/lowpoly-batch102-20261021');O=pathlib.Path('/workspace/shared/lowpoly-batch102-independent-qa-20261021')", "O=pathlib.Path(__file__).resolve().parent; intake=json.loads((O/'final-intake.json').read_text()); W=pathlib.Path(intake['worktree'])")
old=old.replace("for aid in ['arborea','swartpuntia','coronacollina','echmatocrinus']:","for item in intake['assets']:\n aid=item['asset_id']")
old=old.replace("rev={'arborea':'r003','swartpuntia':'r002','coronacollina':'r001','echmatocrinus':'r002'}[aid];p=W/'production/small-life-batch102'/aid/rev/'artifacts'/f'{aid}.glb'", "rev=item['revision'];p=W/item['glb']")
old=old.replace("volume=float(np.einsum('ij,ij->i',arr[:,0],np.cross(arr[:,1],arr[:,2])).sum()/6)","relative=arr-arr[0,0];volume=float(np.einsum('ij,ij->i',relative[:,0],np.cross(relative[:,1],relative[:,2])).sum()/6)")
old=old.replace("(O/aid/'binary-audit.json').write_text", "(O/aid).mkdir(exist_ok=True);(O/aid/'binary-audit.json').write_text")
(Q/'binary-audit.py').write_text(old)
rt=Path('/workspace/shared/lowpoly-batch102-independent-qa-20261021/runtime-audit.cjs').read_text()
start=rt.index(" for(const aid of")
end=rt.index("  const official=",start)
rt=rt[:start]+" const intake=JSON.parse(fs.readFileSync(path.join(__dirname,'final-intake.json'),'utf8'));\n for(const item of intake.assets){\n  const aid=item.asset_id,rev=item.revision,p=path.join(intake.worktree,item.glb),out=path.join(__dirname,aid),bytes=fs.readFileSync(p),sha=crypto.createHash('sha256').update(bytes).digest('hex');\n"+rt[end:]
(Q/'runtime-audit.cjs').write_text(rt)
