import json,pathlib,numpy as np,math,collections,datetime
O=pathlib.Path('/workspace/shared/lowpoly-batch107-independent-qa-20261021');out={}
for aid in ['dendrocystites','trochocystites','helicoplacus','stromatocystites']:
 data=next(iter(json.loads((O/aid/'source-geometry.json').read_text()).values()));v=np.array(data['vertices_world_m']);ct=data['contract'];off=np.array(ct['translation']);v-=off;cs={c['tag']:c for c in ct['components']};fs=ct['integrated_features'];measure={k:{'dimensions_m':np.ptp(v[c['vertices']],axis=0).tolist(),'centroid_m':v[c['vertices']].mean(axis=0).tolist()} for k,c in cs.items()}
 def q(k):return v[cs[k]['vertices']]
 r={'id':aid,'actual_component_kind_counts':dict(collections.Counter(c['kind'] for c in cs.values())),'measurements':measure}
 if aid=='dendrocystites':
  b=q('brachiole').reshape(-1,8,3).mean(axis=1);h=q('homoiostele').reshape(-1,16,3).mean(axis=1);r['actual_centerline_lengths_m']={'brachiole':np.linalg.norm(np.diff(b,axis=0),axis=1).sum(),'homoiostele':np.linalg.norm(np.diff(h,axis=0),axis=1).sum()};r['brachiole_chain_unbranched']=len(b)==57;r['single_suranal_feature']=sum(x['component']=='suranal' for x in fs)==1
 elif aid=='trochocystites':
  plates={}
  for name in ['thecal_plating','cinctus']:
   records=[]
   for f in fs:
    if f['component']!=name:continue
    z=v[f['vertices']];p=z[len(z)//2:];center=p.mean(axis=0);a=abs(np.dot(p[:,0],np.roll(p[:,1],-1))-np.dot(p[:,1],np.roll(p[:,0],-1)))/2
    records.append({'tag':f['tag'],'upper_polygon_centroid_m':center.tolist(),'top_projected_area_m2':a,'upper_polygon_xyz_m':p.tolist()})
   plates[name]=records
  central=[x for x in plates['thecal_plating'] if x['upper_polygon_centroid_m'][2]>.0015];marg=plates['cinctus'];r['plating_actual']=plates;r['pavement_relative_scale']={'central_upper_plate_count':len(central),'central_projected_areas_m2':[x['top_projected_area_m2'] for x in central],'marginal_projected_areas_m2':[x['top_projected_area_m2'] for x in marg],'central_median_m2':float(np.median([x['top_projected_area_m2'] for x in central])),'marginal_median_m2':float(np.median([x['top_projected_area_m2'] for x in marg])),'qualification':'Area measurement describes observed reversal of relative pavement/frame scale. No exact plate-count or arbitrary numeric threshold introduced.'}
  r['mouth_right_of_operculum']=q('mouth').mean(0)[0]>q('operculum').mean(0)[0];r['posterior_short_stele']=measure['homostele']['dimensions_m'][1]<measure['theca']['dimensions_m'][1]
 elif aid=='helicoplacus':
  slopes=[]
  for f in fs:
   if f['component']!='helical_plating':continue
   poly=v[f['vertices'][:len(f['vertices'])//2]]
   for a,b in zip(poly,np.roll(poly,-1,axis=0)):
    d=(math.atan2(b[1],b[0])-math.atan2(a[1],a[0])+math.pi)%(2*math.pi)-math.pi
    if abs(d)>.01 and abs(b[2]-a[2])>1e-8:slopes.append((b[2]-a[2])/d)
  r['all_measured_oblique_plate_slopes_negative']=all(z<0 for z in slopes);r['slopes_count']=len(slopes);r['slopes_minmax_m_per_rad']=[min(slopes),max(slopes)];r['paths']={t:{'plate_count':sum(f['component']==t for f in fs),'z_range_m':[float(q(t)[:,2].min()),float(q(t)[:,2].max())]} for t in cs if t.startswith('ambulacrum_')}
 elif aid=='stromatocystites':
  paths=[k for k in cs if k.startswith('ambulacrum_')];body=q('theca');r['five_paths']=len(paths)==5;r['path_extent']={t:{'radial_max_m':float(np.linalg.norm(q(t)[:,:2],axis=1).max()),'paired_plate_count':sum(f['component']==t for f in fs)} for t in paths};r['body_radial_max_m']=float(np.linalg.norm(body[:,:2],axis=1).max());r['pad_aboral']=q('attachment_pad')[:,2].mean()<q('theca')[:,2].mean();r['periproct_offcenter']=float(np.linalg.norm(q('periproct').mean(0)[:2]));r['relief_versus_disc_m']={'body':np.ptp(body,axis=0).tolist(),'paths_zrange':[float(min(q(t)[:,2].min() for t in paths)),float(max(q(t)[:,2].max() for t in paths))]}
 out[aid]=r
(O/'independent-anatomy-measurements.json').write_text(json.dumps(out,indent=2,default=lambda x:x.item())+'\n');print(json.dumps(out['trochocystites']['pavement_relative_scale'],indent=2));print(out['helicoplacus']['slopes_minmax_m_per_rad'])
