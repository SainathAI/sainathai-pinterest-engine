import os,time,json,zipfile
from PIL import Image,ImageDraw
def generate_title(k): return f"Top {k} ideas to boost engagement"
def generate_description(k): return f"High-converting pin ideas for {k}."
def generate_image(k,output_dir="outputs",filename=None):
  os.makedirs(output_dir,exist_ok=True)
  if not filename: filename=f"pin_{int(time.time())}.png"
  path=os.path.join(output_dir,filename)
  img=Image.new("RGB",(1000,1500),(255,255,255)); ImageDraw.Draw(img).text((50,50),k[:120],fill=(0,0,0)); img.save(path)
  return path
def package_assets(image_paths,title,description,out_dir="outputs",basename=None):
  if not basename: basename=f"pinpack_{int(time.time())}"
  os.makedirs(out_dir,exist_ok=True)
  zip_path=os.path.join(out_dir,f"{basename}.zip")
  with zipfile.ZipFile(zip_path,"w") as z:
    z.writestr("meta.json",json.dumps({"title":title,"description":description}))
    [z.write(p,arcname=os.path.basename(p)) for p in image_paths]
  return zip_path
