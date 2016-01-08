#!/usr/bin/env python

import time

# filename of .mod
#ifs = open(oldfilename,"r")
#

oldfilename ="pin_array.mod"

# the file of .kicad_mod is made in this folder
#ofs = open( folderpath +"/"+filename+".kicad_mod","w")
# where filename is given by "$MODULE filename" in Legacy format
# folder is made or prepared before execute
#

folderpath ="lib"

# if resize ==1
# font size is (1, 1), thickness is 0.15
# line width is 0.15
#
resize = 1

# if defSMD ==1
# (attr SMD) 
#
defSMD = 0


#
#
# class KiCadFootprintHeader
#			-__init__(self)
#			-set_contents(self, items) #items is made by line.split()
#			-set_type(self,type) type is used for (attr type)
#			-get_filename(self) use for get created filename
#			-get_new_format(self) return list of texts(line list)
# class KiCadFootprintFpText
#			-__init__(self)
#			-set_contents(self, items)
#			-get_new_format(self)
# class KiCadFootprintFpLine
# class KiCadFootprintFpCircle(KiCadFootprintFpLine)
# class KiCadFootprintFpArc(KiCadFootprintFpLine)
#			-__init__(self)
#			-set_contents(self, items)
#			-get_new_format(self)
# class KiCadFootprintPad
#			-__init__(self)
#			-set_contents(self, items)
#			-get_new_format(self)
#
#

# creat header and footer? part
class KiCadFootprintHeader:
	def __init__(self):
		self.layer = "F.Cu"
		self.name = "undefined"
		self.tedit = hex(int(time.time()))
		
		if defSMD==1:
			self.type = "SMD"
		else:
			self.type = "undefined"
		self.description = "undefined"
		self.keywords = "undefined"
		
	def set_contents(self, items):
		if items[0]=="Po":
			if items[4]=="15":
				self.layer = "F.Cu"
			#add other layer if wanted
			#else:
			#	self.layer="F.Cu"
		elif items[0]=="Li":
			self.name = items[1]
		elif items[0]=="Cd":
			self.description ="\""
			for num in range(1,len(items)):
				self.description += items[num] + " "
			self.description +="\""
		elif items[0]=="Kw":
			self.keywords ="\""
			for num in range(1,len(items)):
				self.keywords += items[num]+ " "
			self.keywords +="\""
		elif items[0]=="At":
			self.type = items[1]

	def set_type(self,type):
		#(attr type) SMD or virtual
		self.type = type

	def get_filename(self):
		return self.name

	def get_new_format(self):
		linelist=["(module %s (layer %s) (tedit %s)" %(self.name , self.layer , self.tedit)]
		
		if self.type !="undefined":
			linelist.append("  (attr %s)" %(self.type))
		if self.description !="undefined":
			linelist.append("  (descr %s)" %(self.description))
		if self.keywords !="undefined":
			linelist.append("  (tags %s)" %(self.keywords))
		return linelist

class KiCadFootprintFpText:
	def __init__(self):
		self.type="undefined"
		self.layer= "F.SilkS"
		self.x="0"
		self.y="0"
		self.a="0"
		self.text ="undefined"
		self.textwidth=1
		self.textheight=1
		self.textthickness="0.15"
		self.visible="V"

	def set_contents(self, items):
		if items[0]=="T0":
			self.type = "reference"
			self.text = items[11]
			self.text = self.text.lstrip("\"")
			self.text = self.text.rstrip("\"")
		elif items[0]=="T1":
			self.type = "value"
			self.text = items[11]
			self.text = self.text.lstrip("\"")
			self.text = self.text.rstrip("\"")
		self.x= items[1]
		self.y= items[2]
		if resize==1:
			self.textheight = "1"
			self.textwidth = "1"
			self.textthickness = "0.15"
		else:
			self.textheight = items[3]
			self.textwidth = items[4]
			self.textthickness = items[6]
		self.a = items[5]
		self.visible = items[8]
		if items[9]=="21":
			self.layer= "F.SilkS"
		#add other layer if wanted
		#else:
		#	self.layer= "F.SilkS"

	def get_new_format(self):
		
		str = "  (fp_text %s %s " % (self.type, self.text)
		if self.a=="0":
			str +="(at %s %s) " % (self.x, self.y)
		else:
			str +="(at %s %s %s) " % (self.x, self.y, self.a)
		str+="(layer %s) " % (self.layer)
		if self.visible =="I":
			str +="hide"

		linelist=[str]
		linelist.append("    (effects (font (size %s %s) (thickness %s)))" % (self.textwidth, self.textheight, self.textthickness))
		linelist.append("  )")
		return linelist

class KiCadFootprintFpLine:
	def __init__(self):
		self.startx="0"
		self.starty="0"
		self.endx="0"
		self.endy="0"
		self.layer="F.SilkS"
		self.width="0.15"
	
	def set_contents(self, items):
		self.startx= items[1]
		self.starty= items[2]
		self.endx= items[3]
		self.endy= items[4]
		if resize ==1:
			self.width ="0.15"
		else:
			self.width =items[5]
		if items[6]=="21":
			self.layer="F.SilkS"
		else:
			self.layer="F.SilkS"

	def get_new_format(self):
		linelist=["  (fp_line (start %s %s) (end %s %s) (layer %s) (width %s))" %(self.startx, self.starty, self.endx, self.endy, self.layer, self.width)]
		return linelist

class KiCadFootprintFpCircle(KiCadFootprintFpLine):
	def get_new_format(self):
		linelist=["  (fp_circle (center %s %s) (end %s %s) (layer %s) (width %s))" %(self.startx, self.starty, self.endx, self.endy, self.layer, self.width)]
		return linelist

class KiCadFootprintFpArc(KiCadFootprintFpLine):
	def __init__(self):
		self.angle ="0"
		KiCadFootprintFpLine.__init__(self)

	def set_contents(self, items):
		self.startx= items[1]
		self.starty= items[2]
		self.endx= items[3]
		self.endy= items[4]
		self.angle =items[5]
		if resize ==1:
			self.width ="0.15"
		else:
			self.width =items[6]
		if items[7]=="21":
			self.layer="F.SilkS"
		else:
			self.layer="F.SilkS"

	def get_new_format(self):
		linelist=["  (fp_arc (start %s %s) (end %s %s) (angle %s) (layer %s) (width %s))" %(self.startx, self.starty, self.endx, self.endy, self.angle,self.layer, self.width)]
		return linelist

class KiCadFootprintPad:
	def __init__(self):
		self.x ="0"
		self.y ="0"
		self.name ="undefined"
		self.shape ="undefined"
		self.width ="0"
		self.height ="0"
		self.ydelta ="0"
		self.xdelta ="0"
		self.orientation ="0"
		
		self.drsize ="0"
		self.drx ="0"
		self.dry ="0"
		self.drw ="0"
		self.drh ="0"
		self.drtype="undefined"
		
		self.type = "undefined"
		self.mask = "undefined"
	
	def set_contents(self, items):
		if items[0]=="Sh":
			if items[1]=="\"\"":
				self.name ="NOCONN"
			else:
				self.name=items[1]
				self.name = self.name.lstrip("\"")
				self.name = self.name.rstrip("\"")
			if items[2]=="C":
				self.shape="circle"
			elif items[2]=="R":
				self.shape="rect"
			elif items[2]=="O":
				self.shape="oval"
			elif items[2]=="T":
				self.shape="trapezoid"
			self.width = items[3]
			self.height = items[4]
			self.ydelta = items[5]
			self.xdelta = items[6]
			self.orientation = items[7]
		elif items[0]=="Dr":
			self.drsize = items[1]
			self.drx = items[2]
			self.dry = items[3]
			if len(items) == 7:
				self.drw = items[5]
				self.drh = items[6]
				self.drtype="oval"
			else:
				self.drtype="round"
		elif items[0]=="At":
			if items[1]=="STD":
				self.type = "thru_hole"
			elif items[1]=="SMD":
				self.type = "smd"
			elif items[1]=="CONN":
				self.type = "connect"
			elif items[1]=="HOLE":
				self.type = "np_thru_hole"
			
			if items[3]=="00E0FFFF":
				self.mask = "layers *.Cu *.Mask F.SilkS"
			elif items[3]=="00888000":
				self.mask = "layers F.Cu F.Paste F.Mask"
			elif items[3]=="00F0FFFF":
				self.mask = "layers *.Cu *.Mask F.SilkS"
		elif items[0]=="Po":
			self.x = items[1]
			self.y = items[2]

	def get_new_format(self):
		str = "  (pad %s %s %s " % (self.name, self.type, self.shape)
		if self.orientation=="0": 
			str += "(at %s %s)" % (self.x, self.y)
		else:
			str += "(at %s %s %s) " % (self.x, self.y, self.orientation)
		
		str +="(size %s %s) " % (self.width, self.height)
		
		if self.shape=="trapezoid":
			str += "(rect_delta %s %s) " % (self.ydelta, self.xdelta)
		if self.type!="smd":
			if self.drtype=="round":
				str += "(drill %s " % (self.drsize)
				
				if (self.drx=="0") and (self.dry=="0"):
					str+=") "
				else:
					str +="(offset %s %s))" % (self.drx, self.dry)
			elif self.drtype=="oval":
				str += "(drill oval %s %s " % (self.drw, self.drh)
				
				if (self.drx=="0") and (self.dry=="0"):
					str+=") "
				else:
					str +="(offset %s %s)) " % (self.drx, self.dry)
			
		str+="(%s))" %(self.mask)
		linelist=[str]
		return linelist

class KiCadFootprint3DModel:
	def __init__(self):
		self.path="undefine"
		self.xoffset="0"
		self.yoffset="0"
		self.zoffset="0"
		self.xscale="0"
		self.yscale="0"
		self.zscale="0"
		self.xrotate="0"
		self.yrotate="0"
		self.zrotate="0"

	def set_contents(self, items):
		if items[0]=="Na":
			self.path=items[1]
			self.path = self.path.lstrip("\"")
			self.path = self.path.rstrip("\"")
		elif items[0]=="Of":
			self.xoffset=items[1]
			self.yoffset=items[2]
			self.zoffset=items[3]
		elif items[0]=="Sc":
			self.xscale=items[1]
			self.yscale=items[2]
			self.zscale=items[3]
		elif items[0]=="Ro":
			self.xrotate=items[1]
			self.yrotate=items[2]
			self.zrotate=items[3]

	def get_new_format(self):
		linelist=["  (model %s" %(self.path)]
		linelist.append("    (at (xyz %s %s %s))" %(self.xoffset, self.yoffset, self.zoffset))
		linelist.append("    (scale (xyz %s %s %s))" %(self.xscale, self.yscale, self.zscale))
		linelist.append("    (rotate (xyz %s %s %s))" %(self.xrotate, self.yrotate, self.zrotate))
		linelist.append("  )")
		return linelist

def creat_fpmodule(items, fpclass):
	fpclass.set_contents(items)
	return fpclass.get_new_format()



def creat_fptext(items):
	fptext=KiCadFootprintFpText()
	return creat_fpmodule(items,fptext)

def creat_fpline(items):
	fpline=KiCadFootprintFpLine()
	return creat_fpmodule(items,fpline)

def creat_fpcircle(items):
	fpcircle=KiCadFootprintFpCircle()
	return creat_fpmodule(items,fpcircle)

def creat_fparc(items):
	fparc=KiCadFootprintFpArc()
	return creat_fpmodule(items,fparc)

def creat_fppad(ifs):
	fppad=KiCadFootprintPad()
	for line in ifs:
		items = line.split()
		if items[0]=="$EndPAD":
			break
		fppad.set_contents(items)

	return fppad.get_new_format()

def creat_fpmodel(ifs):
	fpmodel=KiCadFootprint3DModel()
	for line in ifs:
		items = line.split()
		if items[0]=="$EndSHAPE3D":
			break
		fpmodel.set_contents(items)

	return fpmodel.get_new_format()

def creat_fpheader(ifs):
	fphead = KiCadFootprintHeader()
	for line in ifs:
		items = line.split()
		if items[0]=="Op":
			break
		fphead.set_contents(items)
		
	return fphead.get_new_format()

def creat_fpfooter():
	linelist=[")\n"]
	return linelist

def make_new_format(ifs):

	outputlist=creat_fpheader(ifs)
	
	for line in ifs:
		items = line.split()
		if items[0]=="T0":
			outputlist.extend(creat_fptext(items))
		elif items[0]=="T1":
			outputlist.extend(creat_fptext(items))
		elif items[0]=="DS":
			outputlist.extend(creat_fpline(items))
		elif items[0]=="DC":
			outputlist.extend(creat_fpcircle(items))
		elif items[0]=="DA":
			outputlist.extend(creat_fparc(items))
		elif items[0]=="$PAD":
			outputlist.extend(creat_fppad(ifs))
		elif items[0]=="$SHAPE3D":
			outputlist.extend(creat_fpmodel(ifs))
		elif items[0]=="$EndMODULE":
			outputlist.extend(creat_fpfooter())
			break
	return outputlist


if __name__=="__main__":

	ifs = open(oldfilename,"r")

	for line in ifs:
		items = line.split()
		if items[0]=="$MODULE":
			ofs = open( folderpath +"/"+items[1]+".kicad_mod","w")
			outputlist=make_new_format(ifs)
			for line in outputlist:
				ofs.write(line +"\n")
			ofs.close()
