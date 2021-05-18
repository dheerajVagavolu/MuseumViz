import os
import json
import random
import time
import random

# var graph = {{ obj|tojson }}

# dynastysole.log(graph['nodes'])

# var net_data = {'nodes': graph['nodes'], 
#           'edges': graph['edges']}


from flask import Flask, render_template, redirect, request, url_for

cur_dir = os.getcwd()

app = Flask(__name__)



@app.route('/')
def hello_world():

   data = proportion_data()
   mat = data['mat']
   typ = data['typ']
   origin = data['origin']
   dynasty = data['dynasty']
   sunb = data['sunb']
   trree = data['trree']

   # print(sunb)

   new_mat = []
   for i in mat.keys():
      temp = {'language': i, 'value': mat[i], 'color': '#00a2ee'}
      new_mat.append(temp)

   mat = new_mat

   new_typ = []
   for i in typ.keys():
      temp = {'language': i, 'value': typ[i], 'color': '#00a2ee'}
      new_typ.append(temp)
      
   typ = new_typ

   new_origin = []
   for i in origin.keys():
      temp = {'language': i, 'value': origin[i], 'color': '#00a2ee'}
      new_origin.append(temp)
      
   origin = new_origin

   new_dynasty = []
   for i in dynasty.keys():
      temp = {'language': i, 'value': dynasty[i], 'color': '#00a2ee'}
      new_dynasty.append(temp)
      
   dynasty = new_dynasty

   


   net_obj = network_g()
   # return render_template('test.html', obj = net_obj)

   return render_template('test.html', trree = trree, sunb = sunb, obj = net_obj, mat = mat, typ = typ, origin = origin, dynasty = dynasty)

def proportion_data():
   _file = open('static/gom_goa_data.json').read()
   data = json.loads(_file)

   mat = {}
   origin = {}
   typ = {}
   dynasty = {}

   for i in data['items']:
      try:
         if i["Main Material"] not in mat.keys():
            mat[i["Main Material"]] = 1
         else:
            mat[i["Main Material"]]  = mat[i["Main Material"]] + 1
      except:
         pass

      try:
         if i["Object Type"] not in typ.keys():
            typ[i["Object Type"]] = 1
         else:
            typ[i["Object Type"]]  = typ[i["Object Type"]] + 1
      except:
         pass
      
      try:
         if i["Origin Place"] not in origin.keys():
            origin[i["Origin Place"]] = 1
         else:
            origin[i["Origin Place"]]  = origin[i["Origin Place"]] + 1
      except:
         pass

      try:
         if i["Patron/Dynasty"] not in dynasty.keys():
            dynasty[i["Patron/Dynasty"]] = 1
         else:
            dynasty[i["Patron/Dynasty"]]  = dynasty[i["Patron/Dynasty"]] + 1
      except:
         pass

   sunb = tree_data({'mat': mat, 'dynasty': dynasty, 'origin': origin, 'typ': typ})
   trree = tree_map_data()
   
   return {'sunb': sunb, 'mat': mat, 'dynasty': dynasty, 'origin': origin, 'typ': typ, 'trree': trree}

   # print(mat)
            



def network_g():
   _file = open('static/gom_goa_data.json').read()
   data = json.loads(_file)

   nodes = []
   edges = []

   

   random.shuffle(data['items'])
   data['items'] = data['items'][:150]


   
   for num, i in enumerate(data['items']):

      image_name = i["Accession Number"].split('-')[-1]
      image_title = ""
      image_title = '<div>' + image_title + i["Title"] + '<hr>' 
      image_title = image_title + '<img style="height:150px" src="../static/images/'+image_name+'.jpg"><hr></div>'

      for kk in i.keys():
         if kk != "Brief Description" and kk != "Detailed Description" and kk != "Title":
            image_title = image_title + kk + ': ' + i[kk] + '<br>' 
         
      nodes.append({'id': num, 'shape': 'circularImage', 
      'image': '../static/images/'+image_name+'.jpg', 
      'brokenImage': '../static/images/fallback.jpg', 
      'physics': 'false', 'widthMin': 1,
      'widthMax': 1,
      'title': image_title, 
      'color': type_color(i["Object Type"])})
      
   for i in range(len(data['items'])):
      for j in range(i, len(data['items'])):
         if i != j:
            temp_edges = check_edges(data['items'][i], i, data['items'][j], j)
            if len(temp_edges) > 0:
               for ii in temp_edges:
                  edges.append(ii)
   
   return {'nodes': nodes, 'edges': edges}

def check_edges(a, a_num, b, b_num):
   edges = []

   # try:
   #    if a["Origin Place"] == b["Origin Place"]:
   #       edges.append({'from': a_num, 'to': b_num, 'physics': 'false', 'color': edge_type_color("Country")})
   # except:
   #    pass
   
   try:
      if a["Main Material"] == b["Main Material"]:
         edges.append({'from': a_num, 'to': b_num, 'physics': 'false', 'color': edge_type_color("Main Material")})
   except:
      pass

   try:
      if a["Object Type"] == b["Object Type"]:
         edges.append({'from': a_num, 'to': b_num, 'physics': 'false', 'color': edge_type_color("Object Type")})
   except:
      pass

   try:
      if a["Patron/Dynasty"] == b["Patron/Dynastye"]:
         edges.append({'from': a_num, 'to': b_num, 'physics': 'false', 'color': edge_type_color("Patron/Dynasty")})
   except:
      pass
   
   try:
      if a["Origin Place"] == b["Origin Place"]:
         edges.append({'from': a_num, 'to': b_num, 'physics': 'false', 'color': edge_type_color("Origin Place")})
   except:
      pass

   return edges

def tree_data(dat):
   

   sunb = []

   
   for i in dat.keys():
      temp = {'name': "", 'value':0, 'children': []}
      if i == 'mat':
         temp['name'] = 'Material Used'
      elif i == 'dynasty':
         temp['name'] = 'Dynasty'
      elif i == 'origin':
         temp['name'] = 'Origin'
      elif i == 'typ':
         temp['name'] = 'Object Type'

      ar = dat[i]
      val = 0
      for ss in dat[i].keys():
         val += dat[i][ss]

      for ss in dat[i].keys():
         inner_val = dat[i][ss]
         if (inner_val / val * 100 > 2 ):
            temp['children'].append({'name': ss, 'value': dat[i][ss]})

      temp['value'] = val
      print(i)
      sunb.append(temp)

   
   
   return sunb

def tree_map_data():
   _file = open('static/gom_goa_data.json').read()
   data = json.loads(_file)

   ulti = {"mat": {}, "origin": {}, "typ": {}, "dynasty": {}}
   
   for ii in data["items"]:
      image_name = ii["Accession Number"].split('-')[-1]
      _temp = {}
      _temp["img"] = '../static/images/' + image_name + '.jpg' 
      for key in ii.keys():
         if key != "Brief Description" and key != "Detailed Description":
            _temp[key] = ii[key]
      
      for key in ii.keys():   
         if key == "Main Material":
            if ii[key] not in ulti["mat"].keys():
               ulti["mat"][ii[key]] = [_temp]
            else:
               ulti["mat"][ii[key]].append(_temp)
         
         if key == "Origin Place":
            if ii[key] not in ulti["origin"].keys():
               ulti["origin"][ii[key]] = [_temp]
            else:
               ulti["origin"][ii[key]].append(_temp)
            
            
         if key == "Patron/Dynasty":
            if ii[key] not in ulti["dynasty"].keys():
               ulti["dynasty"][ii[key]] = [_temp]
            else:
               ulti["dynasty"][ii[key]].append(_temp)
            
         
         if key == "Object Type":
            if ii[key] not in ulti["typ"].keys():
               ulti["typ"][ii[key]] = [_temp]
            else:
               ulti["typ"][ii[key]].append(_temp)
            
   
   with open('tree.json', 'w') as outfile:
      json.dump(ulti, outfile)

   return ulti





def type_color(typ):
   data = {'Architecture': '#ec6262', 
           'Philately': '#e1d276', 
           'Painting': '#99ea86', 
           'Coin': '#d698d4', 
           'Sculpture': '#a8f0f9', 
           'Arms': '#e4a8f9', 
           'Textile': '#742d20'}

   return data[typ]

def edge_type_color(typ):
   data = {'Country': '#ec6262', 
           'Main Material': '#e1d276', 
           'Object Type': '#8986ea', 
           'Patron/Dynasty': '	#0000ff', 
           'Origin Place': '	#00ffff'}

   return data[typ]





if __name__ == '__main__':
   app.run(debug = True)