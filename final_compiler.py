#Triantafyllopoulos Andreas 4504 cse84504
#Koufopoulos Myron 4398 cse84398

import sys
letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
			'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',]
numbers = ['0','1','2','3','4','5','6','7','8','9']
bound_words = ['program','declare','if','else','while','switchcase','forcase','incase','default','case',
						'not','and','or','function','procedure','call','return','in','inout','input','print']
family_names = ['number','keyword','id','add_op','mul_op','rel_op','assignment','delimeter','group_symbol']

#token kwdikoi pou dinoume sto syntaktiko analyth family
number = 1 #12
keyword = 2 #while,if,else
identifier = 3 #lekseis
add_op = 4 #+-
mul_op = 5 #*/
rel_op = 6 #<=
assignment = 7 #:=
delimeter = 8 #.,;
group_symbol = 9 #{}

#kwdikoi gia xarakthres pou diavazei to automato
#gia auta prepei na kanw -40 ka8e fora gia na eimai mesa ston pinaka
gramma = 40
pshfio = 41
asteriskos = 42
slash = 43
syn = 44
plhn = 45
ison = 46
mikrotero = 47
megalytero = 48
leukoi = 49
enter = 50
agkylh_aristerh = 51
agkylh_de3ia = 52
paren8esh_aristerh = 53
paren8esh_de3ia = 54
hashtag = 55
anw_katw_teleia = 56
teleia = 57
komma = 58
erwtimatiko = 59
eof = 60
mh_apodekta = 61
anoigma_block = 62
kleisimo_block = 63
#katw_paula = 64 #ERWTHSH mporei na dw8ei to nikos_giwrgos?

#extra gia to katw sxhma
mikrotero_iso = 64
megalytero_iso = 65
ana8esh = 66
diaforo = 67

#kwdikoi gia endiameses katastaseis automatou
start = 0
dig = 1 #pshfio
idk = 2 #metavlhth h keyword
asgn = 3 #ana8esh timhs se metavlhth
smaller = 4
larger = 5
rem = 6 #sxolia

#errors
error_oxi_kleisimo_sxoliwn = -1
error_la8os_ana8esh = -2
error_ari8mos_xarakthras = -3
error_ari8mos_ektos_diasthmatos = -4
error_megalo_alfari8mhtiko = -5
error_symvolo_ektos_glwssas = -6

metavaseis_automatou = [
			#start		
						[idk,dig,asteriskos,slash,syn,plhn,ison,smaller,larger,start,start,agkylh_aristerh,agkylh_de3ia,paren8esh_aristerh,paren8esh_de3ia,
						rem,asgn,teleia,komma,erwtimatiko,eof,error_symvolo_ektos_glwssas,anoigma_block,kleisimo_block],
			#digit		
						[error_ari8mos_xarakthras,dig,pshfio,pshfio,pshfio,pshfio,pshfio,pshfio,pshfio,
						pshfio,pshfio,pshfio,pshfio,pshfio,pshfio,pshfio,pshfio,pshfio,pshfio,pshfio,pshfio,error_symvolo_ektos_glwssas,pshfio,pshfio],
			#metavlhth  
						[idk,idk,gramma,gramma,gramma,gramma,gramma,gramma,gramma,gramma,gramma,gramma,gramma,gramma,gramma,gramma,
						gramma,gramma,gramma,gramma,gramma,error_symvolo_ektos_glwssas,gramma,gramma],
			#ana8esh    
						[error_la8os_ana8esh,error_la8os_ana8esh,error_la8os_ana8esh,error_la8os_ana8esh,
						error_la8os_ana8esh,error_la8os_ana8esh,ana8esh,error_la8os_ana8esh,error_la8os_ana8esh,error_la8os_ana8esh,error_la8os_ana8esh,error_la8os_ana8esh,error_la8os_ana8esh,error_la8os_ana8esh,error_la8os_ana8esh,error_la8os_ana8esh,error_la8os_ana8esh,error_la8os_ana8esh,error_la8os_ana8esh,error_la8os_ana8esh,error_la8os_ana8esh,error_symvolo_ektos_glwssas,error_la8os_ana8esh,error_la8os_ana8esh],
			#smaller	
						[mikrotero,mikrotero,mikrotero,mikrotero,mikrotero,mikrotero,mikrotero_iso,mikrotero,diaforo,mikrotero,mikrotero,mikrotero,mikrotero,mikrotero,mikrotero,mikrotero,mikrotero,mikrotero,mikrotero,mikrotero,mikrotero,error_symvolo_ektos_glwssas,mikrotero,mikrotero],
			#larger		
						[megalytero,megalytero,megalytero,megalytero,megalytero,megalytero,megalytero_iso,megalytero,megalytero,megalytero,megalytero,megalytero,megalytero,megalytero,megalytero,megalytero,megalytero,megalytero,megalytero,megalytero,megalytero,error_symvolo_ektos_glwssas,megalytero,megalytero],
			#sxolia		
						[rem,rem,rem,rem,rem,rem,rem,rem,rem,rem,rem,rem,rem,rem,rem,start,rem,rem,rem,rem,error_oxi_kleisimo_sxoliwn,rem,rem,rem]]

class Token:
        def __init__(self,recognized_string='',family='',line_number=0): # ta arxikopoioume etsi wste na uparxei to prwto token prin anoixtei to arxeio mas
                self.recognized_string = recognized_string
                self.family = family
                self.line_number = line_number

        def __str__(self): # tupwnoume me auto 
                return self.recognized_string+'\t family : "' + family_names[self.family-1] + '",  line_number = ' + str(self.line_number)
class Lex:
	def __init__(self,current_line,file_name,token):
		self.current_line = current_line
		self.file_name = file_name
		self.token = token

	def lex_analysis(self):  # to LEX mas
		katastash = start	# kratame thn katastash pou briskomaste kai apothikeuetai prin thn eksodo to family pou anhkei to string
		alphanumeric = ''	# kratame thn lektikh monada
		while(katastash>-1 and katastash<7):	# oso h katastash mas einai apo 0-6
			xarakthras = f.read(1)				# diabazei ena-ena xarakthra
			if(xarakthras in letters):
				token_xar = gramma
			elif(xarakthras in numbers):
				token_xar = pshfio
			elif(xarakthras == '*'):
				token_xar = asteriskos
			elif(xarakthras == '/'):
				token_xar = slash
			elif(xarakthras == '+'):
				token_xar = syn
			elif(xarakthras == '-'):
				token_xar = plhn
			elif(xarakthras == '='):
				token_xar = ison
			elif(xarakthras == '<'):
				token_xar = mikrotero
			elif(xarakthras == '>'):
				token_xar = megalytero
			elif(xarakthras == ' '):
				token_xar = leukoi
			elif(xarakthras == '\t'):
				token_xar = leukoi
			elif(xarakthras == '\n'):
				self.current_line += 1		# otan brw to enter enhmerwnw thn metablhth tou constructor
				token_xar = enter
			elif(xarakthras == '['):
				token_xar = agkylh_aristerh
			elif(xarakthras == ']'):
				token_xar = agkylh_de3ia
			elif(xarakthras == '('):
				token_xar = paren8esh_aristerh
			elif(xarakthras == ')'):
				token_xar = paren8esh_de3ia
			elif(xarakthras == '#'):
				token_xar = hashtag
			elif(xarakthras == ':'):
				token_xar = anw_katw_teleia
			elif(xarakthras == '.'):
				token_xar = teleia
			elif(xarakthras == ','):
				token_xar = komma
			elif(xarakthras == ';'):
				token_xar = erwtimatiko
			elif(xarakthras == ''):
				token_xar = eof
			elif(xarakthras == '{'):
				token_xar = anoigma_block
			elif(xarakthras == '}'):
				token_xar = kleisimo_block
			else:
				token_xar = mh_apodekta
			katastash = metavaseis_automatou[katastash][token_xar-40]	# paw stis metavaseis gia na dw pou tha briskomai meta
																		# vazoume -40 giati oi xarakthres mas ksekinane apo to 40 kai theloume na paroume thn thesh sto pinaka
			if(len(alphanumeric)<31): 
				if(katastash != start and katastash != rem):			# oso dn eimaste sto start h sta sxolia
					alphanumeric += xarakthras
			else:
				katastash = error_megalo_alfari8mhtiko
		if(katastash == error_megalo_alfari8mhtiko):
			print("Error sth grammh " + str(self.current_line) + ".\n Dw8hke alfari8mhtiko megalytero tou epitreptou (30 xarakthres)")
			exit(-1)
		"""
		shmantikos elegxos gia na doume an exoume diavasei kapoio sumvolo xwris na to anagnwrisoume
		auto mporei na exei sumvei mono se tesseris periptwseis kai stis tesseris autes to epistrefoume
		gia na mporesoume na to ksanadiavasoume kai an autos o extra xarakthras pou diabasthke htan to enter 
		tote afairoume mia grammh"""
		if(katastash == gramma or katastash == pshfio or katastash == mikrotero or katastash == megalytero):
			if(xarakthras == '\n'):
				self.current_line = self.current_line - 1
			xarakthras = f.seek(f.tell()-1,0)
			alphanumeric = alphanumeric[0:-1]

		#periorismos gia to poso megalow mporei na einai enas arithmos
		if(katastash == pshfio):
			if(abs(int(alphanumeric)) < pow(2,32)):
				katastash = number #1 (ftiaxnoume ta family)
			else:
				katastash = error_ari8mos_ektos_diasthmatos	
		# tupwnoume ta error
		if(katastash == error_ari8mos_ektos_diasthmatos):
			print("Error sth grammh " + str(self.current_line) + ".\n Dw8hke ari8mos ektos tou diasthmatos [-(2^32-1) , 2^32-1]")
			exit(-1)
		elif(katastash == error_oxi_kleisimo_sxoliwn):
			print("Error sth grammh " + str(self.current_line) + ".\n Den exoun kleisei ta sxolia xreiazetai # sto telos")
			exit(-1)
		elif(katastash == error_la8os_ana8esh):
			print("Error sth grammh " + str(self.current_line) + ".\n Den vre8hke = meta apo : se ana8esh")
			exit(-1)
		elif(katastash == error_ari8mos_xarakthras):
			print("Error sth grammh " + str(self.current_line) + ".\n Xarakthras meta apo ari8mo (den ginetai sta8eros ari8mos na periexei gramma)")
			exit(-1)
		elif(katastash == error_symvolo_ektos_glwssas):
			print("Error sth grammh " + str(self.current_line) + ".\n To symvolo pou dw8hke den anagnwrizetai apo th glwssa")
			exit(-1)
		
		# edw elegxoume se pio family anhkei h kathe leksh mas
		if(katastash == gramma):
			if(alphanumeric in bound_words):	
				katastash = keyword #2 (ftiaxnoume ta family)
			else:
				katastash = identifier #3 (ftiaxnoume ta family)
		if(katastash == plhn or katastash == syn):
			katastash = add_op #4
		elif(katastash == asteriskos or katastash == slash):
			katastash = mul_op #5
		elif(katastash == mikrotero or katastash == megalytero or katastash == mikrotero_iso or katastash == megalytero_iso or katastash == diaforo or katastash == ison ):
			katastash = rel_op #6
		elif(katastash == ana8esh ):
			katastash = assignment #7
		elif(katastash == teleia or katastash == komma or katastash == erwtimatiko):
			katastash = delimeter #8
		elif(katastash == agkylh_de3ia or katastash == agkylh_aristerh or katastash == paren8esh_de3ia or katastash == paren8esh_aristerh or katastash == anoigma_block or katastash == kleisimo_block):
			katastash = group_symbol #9

		# apothikeuoume ola ta pedia pou xreiazetai o suntantikos analuths sto token
		p1.recognized_string = alphanumeric
		p1.family = katastash
		p1.line_number = self.current_line
		return p1

class Parser():
	def __init__(self,lexical_analyzer):
		self.lexical_analyzer = lexical_analyzer

	#ENDIAMESOS KWDIKAS
	def nextQuad(self):
		global counterQuads
		return counterQuads

	def genQuad(self,op,x,y,z):
		global counterQuads
		global listForQuads
		global listForEachQuad					# apla gia na krataei ta quads (den xreiazetai global)	
		listForEachQuad = []
		listForEachQuad += [self.nextQuad()]	# h thesh ths neas tetradas sthn sunolikh lista tetradwn
		listForEachQuad += [op]					# prosthetoume to prwto orisma
		listForEachQuad += [x]					# prosthetoume to deutero orisma
		listForEachQuad += [y]					# prosthetoume to trito orisma
		listForEachQuad += [z]					# prosthetoume to tetarto orisma
		listForQuads += [listForEachQuad]
		counterQuads +=1						# epomenh 4ada.
		return listForEachQuad

	def newTemp(self):
		global listOfTemporaryVariables			# mono gia to print sumplhrwthike
		global T_
		var = "T_"
		var += str(T_)
		T_ +=1
		listOfTemporaryVariables += [var]
		entity = Entity()
		entity.name = var
		entity.array[0] = 'Int'
		entity.typos = 'TemporaryVariable'
		entity.array[2] = calculateOffset()
		addEntity(entity)
		#print(listOfTempVariables)
		return var 								# epistrefei thn proswrinh metavlhth

	def emptyList(self):
		emptyLists = []							# dhmiourgoume kenes listes tetradwn
		return emptyLists

	def makeList(self, x):
		labelQuads = [x]						# lista etiketwn tetradwn periexontas mono to x
		return labelQuads

	def merge(self,list1,list2):
		mergeList = list1						# sunenwnoume tis listes
		mergeList += list2
		return mergeList

	def backPatch(self,list,z):
		global listForQuads
		for i in list:
			for j in listForQuads:
				if(i == j[0]):
					j[4] = z
		# sto prwto for gia ka8e stoixeio i ths listas me tis grammes pou 8eloun allagh
		# kai gia ka8e mikrh lista j mesa sto synolo twn listwn
		# an to i (h grammh pou den exei symplhrw8ei) einai iso me to prwto stoixeio ths listas j apo to synolo listwn
		# kane to 5o stoixeio ths listas iso me z
		return

	def syntax_analyzer(self):
		global token
		token = self.get_token()
		self.program()

	def get_token(self):
		return self.lexical_analyzer.lex_analysis()

	def program(self):
		global token
		if (token.recognized_string == 'program'):
			token = self.get_token()
			if (token.family == identifier):
				id_1 = token.recognized_string
				token = self.get_token()
				self.block(id_1,1)
				if (token.recognized_string == '.'):
					token = self.get_token()
					if (token.recognized_string == ''): # mporei na thelei allagh
						token = self.get_token()		# erwthsh ti token tha theloume na parei
						return
				else:
					print('ERROR !! sth grammh : '+ str(token.line_number) +'\n Den dothike teleia sto telos tou programmatos gia na termatisei swsta ')
					exit(-1)
			else:
				print('ERROR !! sth grammh : '+ str(token.line_number) +'\n Gia to arxeio den exei dothei onoma ')
				exit(-1)
		else:
			print('ERROR !! sth grammh : '+ str(token.line_number) +'\n Den exei dothei h leksh program sthn arxh tou programmatos ')
			exit(-1)
		return

	def block(self,name,check):
		global token
		global readScope
		if(token.recognized_string == '{'):
			token = self.get_token()
			createScope(name)
			# edw 8a dhmiourghsoume ena Entity gia ta orismata twn synarthsewn
			# to vazoume se auto to shmeio giati 8eloume na mpoun sto epomeno scope
			# ta eixame krathsei san argument prin vre8ei to { ths epomenhs synarthshs (krath8hkan sthn formalparitem)
			if(check!=1):
				addParameterToScope()
			self.declarations()
			self.subprograms()
			self.genQuad("begin_block",name,"_","_")
			# pername sto entityList.array[4] = startingQuad 
			# thn prwth ektelesimh entolh ths sunarthshs
			if(check!=1):								
				calculateQuad()
			self.blockstatements()
			if(check): 									# 8eloume to halt na einai panta prin to end_block
				self.genQuad("halt","_","_","_")		# gia na mporei na kanei jump an kapoia entolh px to else den yparxei
			else:
				calculateFramelength()  				# gia kathe entity theloume na kratame to framelength tou (last offset+4)
			self.genQuad("end_block",name,"_","_")		
			assemblyCode()								# otan teleiwnei ena block theloume na dhmiourgoume to kwdika sthn assembly
			if(token.recognized_string == '}'):
				token = self.get_token()
				# edw otan teleiwnei ena block pairnoume to offset tou teleutaiou entity tou scope pou teleiwnei, tou pros8etw 4 kai to vazw
				# sto teleutaio entity tou epomenou scope to opoio 8a einai h function h procedure kai sto offset tou
				# and (readScope.nextScope.entityList[-1].typos == 'Function' or readScope.nextScope.entityList[-1].typos == 'Procedure')): 
				if(readScope.nextScope != None):		
					readScope.nextScope.entityList[-1].array[2] = readScope.entityList[-1].array[2] + 4
				print_pinakas_symvolwn()
				removeScope()
				return
			else:
				print('ERROR !! sth grammh : '+ str(token.line_number) +'\n Den kleinei to block swsta, den exei dothei deksi kleisimo block')	
				exit(-1)
		else:
			print('ERROR !! sth grammh : '+ str(token.line_number) +'\n Den anoigei to block swsta, den exei dothei aristero anoigma block')
			exit(-1)
		return

	def declarations(self):
		global token
		global token_line
		while (token.recognized_string == 'declare'):
			token = self.get_token()
			token_line = token.line_number
			self.varlist()
			if (token.recognized_string == ';'):
				token = self.get_token()
			else:
				print('ERROR !! sth grammh ' + str(token_line) + '\n Den exoume sumplhrwsei to erwthmatiko sto telos ths entolhs declare ')
				exit(-1)
		return

	def varlist(self):
		global token
		if (token.family == identifier):
			listOfVariables.append(token.recognized_string)			# gia ta tis metablhtes pou dhlwnei o xrhsths(sto c arxeio)
			entity = Entity()
			entity.name = token.recognized_string
			entity.typos = 'Variable'
			entity.array[0] = 'Int'
			entity.array[2] = calculateOffset()
			addEntity(entity)
			token = self.get_token()
			while (token.recognized_string == ','):
				token = self.get_token()
				if (token.family == identifier):
					listOfVariables.append(token.recognized_string)	# gia ta tis metablhtes pou dhlwnei o xrhsths(sto c arxeio)
					entity = Entity()
					entity.name = token.recognized_string
					entity.typos = 'Variable'
					entity.array[0] = 'Int'
					entity.array[2] = calculateOffset()
					addEntity(entity)
					token = self.get_token()
				else:
					print('ERROR !! sth grammh ' + str(token.line_number) + '\n Yparxoun duo id xwris na xwrizontai me komma ')
					exit(-1)
		return

	def subprograms(self):
		global token
		while (token.recognized_string == 'procedure' or token.recognized_string == 'function'):
			self.subprogram() 		# den pairnoume kainourgio token theloume na exoume to idio
		return

	def subprogram(self):
		global token
		global token_line
		global flag
		if (token.recognized_string == 'procedure'):
			token = self.get_token()
			if (token.family == identifier):
				entity = Entity()
				entity.name = token.recognized_string
				entity.typos = 'Procedure'
				entity.array[0] = 'Int'
				addEntity(entity)
				name = token.recognized_string
				token = self.get_token()
				if (token.recognized_string == '('):
					token = self.get_token()
					token_line = token.line_number
					self.formalparlist()
					if (token.recognized_string == ')'):
						token = self.get_token()
						self.block(name,0)
						return
					else:
						print('ERROR !! sth grammh ' + str(token_line) + '\n H parenthesh anoigei alla den kleinei, den exei dothei deksia parenthesh')
						exit(-1)
				else:
					print('ERROR !! sth grammh ' + str(token.line_number) + '\n H parenthesh den exei anoiksei, den exei dothei aristerh parenthesh ')
					exit(-1)
			else:
				print('ERROR !! sth grammh ' + str(token.line_number) + '\n Leipei to onoma ths synarthshs meta to procedure ')
				exit(-1)
		elif (token.recognized_string == 'function'):
			token = self.get_token()
			if (token.family == identifier):
				entity = Entity()
				entity.name = token.recognized_string
				entity.typos = 'Function'
				entity.array[0] = 'Int'
				addEntity(entity)
				name = token.recognized_string
				token = self.get_token()
				if (token.recognized_string == '('):
					token = self.get_token()
					token_line = token.line_number
					self.formalparlist()
					if (token.recognized_string == ')'):
						token = self.get_token()
						self.block(name,0)
						return
					else:
						print('ERROR !! sth grammh ' + str(token_line) + '\n H parenthesh anoigei alla den kleinei, den exei dothei deksia parenthesh')
						exit(-1)
				else:
					print('ERROR !! sth grammh ' + str(token.line_number) + '\n H parenthesh den exei anoiksei, den exei dothei aristerh parenthesh ')
					exit(-1)
			else:
				print('ERROR !! sth grammh ' + str(token.line_number) + '\n Leipei to onoma ths synarthshs meta to function ')
				exit(-1)
		return

	def formalparlist(self):
		global token
		self.formalparitem()	# elegxetai to keno sthn apo katw sunarthsh gia auto den allazoume kai token
		while (token.recognized_string == ','):
			token = self.get_token()
			self.formalparitem()
		return

	def formalparitem(self):
		global token
		if (token.recognized_string == 'in'):
			token = self.get_token()
			if(token.family == identifier):
				argument = Argument()
				argument.name = token.recognized_string
				argument.parMode = 'CV' 				# perasma me timh
				addArgument(argument)					# pername thn formalparameter
				token = self.get_token()
			else:
				print('ERROR !! sth grammh ' + str(token.line_number) + '\n Leipei to onoma metavlhths meta to in ')
				exit(-1)
		elif (token.recognized_string == 'inout'):
			token = self.get_token()
			if(token.family == identifier):
				argument = Argument()
				argument.name = token.recognized_string
				argument.parMode = 'REF' 				# perasma me anafora
				addArgument(argument)					# pername thn formalparameter
				token = self.get_token()
			else:
				print('ERROR !! sth grammh ' + str(token.line_number) + '\n Leipei to onoma metavlhths meta to inout ')
				exit(-1)
		return

	def statements(self):
		global token
		global token_line
		if (token.recognized_string == '{'):
			token = self.get_token()
			self.statement()
			while (token.recognized_string == ';'):	# mporoume na doume mhpws elegxetai to erwthmatiko mesa sta statement kathe fora wste na eimaste komple kai me to erwthmatiko 
				token = self.get_token()
				self.statement()
			if (token.recognized_string == '}'):
				token = self.get_token()
				return
			else:
				print('ERROR !! sth grammh ' + str(token.line_number) + '\n Den kleinei to block den exei sumplhrwthei h deksia agkylh ')
				exit(-1)
		else:
			token_line = token.line_number
			self.statement()						# den brhke parenthesh ara o lektikos xarakthras pou exoume einai to statement
			if (token.recognized_string == ';'):
				token = self.get_token()
				return
			else:
				print('ERROR !! sth grammh ' + str(token_line) + '\n Den exei erwthmatiko sto telos ths entolhs ')
				exit(-1)
		return

	def blockstatements(self):
		global token
		global count
		count = 0
		self.statement()
		if (token.recognized_string == ';'):
			while (True):
				token = self.get_token()
				self.statement()
				if (token.recognized_string == ';'):
					pass
				else:
					break
		elif (count < 0):							# auto gia to prwto pou tha exw -2 na perasei an brei keno
			return
		else:
			print('ERROR !! sth grammh ' + str(token.line_number) + '\n Ksexasthke to erwthmatiko ')
			exit(-1)
		return
		

	def statement(self):
		global token
		global count  								# metraei posa erwthmatika eidame
		if (token.family == identifier):			# edw mpainoun oles oi metavlhtes ara kai ta error leksewn an exoun ginei
			self.assign_stat()
		elif (token.recognized_string == 'if'):
			token = self.get_token()
			self.if_stat()
		elif (token.recognized_string == 'while'):
		 	token = self.get_token()
		 	self.while_stat()
		elif (token.recognized_string == 'switchcase'):
		 	token = self.get_token()
		 	self.switchcase_stat()
		elif (token.recognized_string == 'forcase'):
		 	token = self.get_token()
		 	self.forcase_stat()
		elif (token.recognized_string == 'incase'):
		 	token = self.get_token()
		 	self.incase_stat()
		elif (token.recognized_string == 'call'):
		 	token = self.get_token()
		 	self.call_stat()
		elif (token.recognized_string == 'return'):
		 	token = self.get_token()
		 	self.return_stat()
		elif (token.recognized_string == 'input'):
		 	token = self.get_token()
		 	self.input_stat()
		elif (token.recognized_string == 'print'):
		 	token = self.get_token()
		 	self.print_stat()
		
		if(token.recognized_string == '}'):
			count = -1
		elif (token.recognized_string == '{'):
			print('ERROR !! sth grammh ' + str(token.line_number-1) + '\n Den perimena edw na uparxei { ')
			exit(-1)
		elif (token.recognized_string != ';'):
			token = self.get_token()
			if (token.recognized_string == '}'):
				count = -1
				return
			else:
				print('ERROR !! sth grammh ' + str(token.line_number-1) + '\n Ksexasthke to erwthmatiko edw')
				exit(-1)
		
		return

	def assign_stat(self):
		global token
		id_1 = token.recognized_string
		token = self.get_token()
		if(token.family == assignment):
			token = self.get_token()
			E_place = self.expression()
			self.genQuad(':=',E_place,'_',id_1)
			return
		else:
			print('ERROR !! sth grammh ' + str(token.line_number) + '\n Den exei dothei swsta to symvolo ths anatheshs \':=\' ')
			exit(-1)
		return

	def if_stat(self):
		global token
		global token_line
		if (token.recognized_string == '('):
			token = self.get_token()
			token_line = token.line_number
			B = self.condition()
			Btrue = B[0]
			Bfalse = B[1]
			self.backPatch(Btrue, self.nextQuad())
			if (token.recognized_string == ')'):
				token = self.get_token()
				self.statements()
				ifList = self.makeList(self.nextQuad())
				self.genQuad('jump','_','_','_')
				self.backPatch(Bfalse, self.nextQuad())
				self.elsepart()
				self.backPatch(ifList, self.nextQuad())
				return
			else:
				print('ERROR !! sth grammh ' + str(token_line) + '\n H parenthesh anoigei alla den kleinei dhladh den exoume deksia parenthesh')
				exit(-1)
		else:
			print('ERROR !! sth grammh ' + str(token.line_number) + '\n H parenthesh den anoigei swsta perimename aristerh parenthesh')
			exit(-1)
		return 

	def elsepart(self):
		global token
		if (token.recognized_string == 'else'):
			token = self.get_token()
			self.statements()
		return

	def while_stat(self):
		#B1[0] = Btrue, B1[1] = Bfalse
		global token
		global token_line
		if (token.recognized_string == '('):
			token = self.get_token()
			token_line = token.line_number
			
			nQuad = self.nextQuad()
			B = self.condition()
			Btrue = B[0]
			Bfalse = B[1]
			self.backPatch(Btrue, self.nextQuad())
			if (token.recognized_string == ')'):
				token = self.get_token()
				self.statements()
				self.genQuad('jump','_','_',nQuad)
				self.backPatch(Bfalse,self.nextQuad())
				return
			else:
				print('ERROR !! sth grammh ' + str(token_line) + '\n H paren8esh anoigei alla den kleinei ')
				exit(-1)
		else:
			print('ERROR !! sth grammh ' + str(token.line_number) + '\n H paren8esh ths while den anoigei swsta ')
			exit(-1)
		return 

	def switchcase_stat(self):
		global token
		global token_line
		exitList = self.emptyList()
		while (token.recognized_string == 'case'):
			token = self.get_token()
			if (token.recognized_string == '('):
				token = self.get_token()
				token_line = token.line_number
				condition = self.condition()
				Ctrue = condition[0]
				Cfalse = condition[1]
				self.backPatch(Ctrue,self.nextQuad())
				if (token.recognized_string == ')'):
					token = self.get_token()
					self.statements()
					t = self.makeList(self.nextQuad())
					self.genQuad('jump','_','_','_')
					exitList = self.merge(exitList,t)
					self.backPatch(Cfalse,self.nextQuad())
				else:
					print('ERROR !! sth grammh ' + str(token_line) + '\n H parenthesh anoigei alla den kleinei ')
					exit(-1)
				
			else:
				print('ERROR !! sth grammh ' + str(token.line_number) + '\n H parenthesh den anoigei swsta meta to case ')
				exit(-1)
		if (token.recognized_string == 'default'):
			token = self.get_token()
			self.statements()
			self.backPatch(exitList,self.nextQuad())
		else:
			print('ERROR !! sth grammh ' + str(token.line_number) + '\n Den ksekina swsta to default ths forcase ')
			exit(-1)
		return

	def forcase_stat(self):
		global token
		global token_line
		firstCondQuad = self.nextQuad()
		while (token.recognized_string == 'case'):
			token = self.get_token()
			if (token.recognized_string == '('):
				token = self.get_token()
				token_line = token.line_number
				condition = self.condition()
				Ctrue = condition[0]
				Cfalse = condition[1]
				self.backPatch(Ctrue,self.nextQuad())
				if (token.recognized_string == ')'):
					token = self.get_token()
					self.statements()
					self.genQuad('jump','_','_',firstCondQuad)
					self.backPatch(Cfalse,self.nextQuad())
				else:
					print('ERROR !! sth grammh ' + str(token_line) + '\n H parenthesh anoigei alla den kleinei ')
					exit(-1)
			else:
				print('ERROR !! sth grammh ' + str(token.line_number) + '\n H parenthesh den anoigei swsta meta to case ')
				exit(-1)
		if (token.recognized_string == 'default'):
			token = self.get_token()
			self.statements()
		else:
			print('ERROR !! sth grammh ' + str(token.line_number) + '\n Den ksekina swsta to default ths forcase ')
			exit(-1)
		return 

	def incase_stat(self):
		global token
		global token_line
		flag = self.newTemp()
		firstCondQuad = self.nextQuad()
		self.genQuad(':=',0,'_',flag)
		while (token.recognized_string == 'case'):
			token = self.get_token()
			if (token.recognized_string == '('):
				token = self.get_token()
				token_line = token.line_number
				condition = self.condition()
				Ctrue = condition[0]
				Cfalse = condition[1]
				if (token.recognized_string == ')'):
					self.backPatch(Ctrue,self.nextQuad())
					token = self.get_token()
					self.statements()
					self.genQuad(':=',1,'_',flag)
					self.backPatch(Cfalse,self.nextQuad())
				else:
					print('ERROR !! sth grammh ' + str(token_line) + '\n H parenthesh anoigei alla den kleinei swsta perimena deksia parenthesh')
					exit(-1)
			else:
				print('ERROR !! sth grammh ' + str(token.line_number) + '\n Den anoigei swsta h parenthesh, perimename aristerh parenthesh ')
				exit(-1)
		self.genQuad('=',flag,'1',firstCondQuad)
		return 

	def return_stat(self):
		global token
		global token_line
		# me to return exoume them sto pinaka sumvolwn pou dn mpainei mesa
		# omws stis diafanies uparxei sto kwdika ths assembly
		if (token.recognized_string == '('):
			token = self.get_token()
			token_line = token.line_number
			E_place = self.expression()
			self.genQuad('retv',E_place,'_','_')
			if (token.recognized_string == ')'):
				token = self.get_token()
				return
			else:
				print('ERROR !! sth grammh ' + str(token_line) + '\n H parenthesh anoigei alla den kleinei swsta, perimename deksia parenthesh')
				exit(-1)
		else:
			print('ERROR !! sth grammh ' + str(token.line_number) + '\n H parenthesh den anoigei swsta, perimename aristerh parenthesh ')
			exit(-1)
		return 

	def call_stat(self):
		global token
		global token_line
		if (token.family == identifier):
			varName = token.recognized_string
			token = self.get_token()
			if (token.recognized_string == '('):
				token = self.get_token()
				token_line = token.line_number
				self.actualparlist()
				self.genQuad('call',varName,'_','_')
				if (token.recognized_string == ')'):
					token = self.get_token()
					return
				else:
					print('ERROR !! sth grammh ' + str(token_line) + '\n H parenthesh anoigei alla den kleinei swsta, perimename deksia parenthesh ')
					exit(-1)
			else:
				print('ERROR !! sth grammh ' + str(token.line_number) + '\n H parenthesh den anoigei swsta, perimename aristerh parenthesh')
				exit(-1)
		else:
			print('ERROR !! sth grammh ' + str(token.line_number) + '\n Lathos eisodos, h metavlhth den exei oristei swsta ')
			exit(-1)
		return 

	def print_stat(self):
		global token
		global token_line
		if (token.recognized_string == '('):
			token = self.get_token()
			token_line = token.line_number
			E_place = self.expression()
			self.genQuad('out',E_place,'_','_')
			if (token.recognized_string == ')'):
				token = self.get_token()
			else:
				print('ERROR !! sth grammh ' + str(token_line) + '\n H paren8esh anoigei alla den kleinei swsta, perimename deksia parenthesh ')
				exit(-1)
		else:
			print('ERROR !! sth grammh ' + str(token.line_number) + '\n H parenthesh den anoigei swsta, perimename aristerh parenthesh')
			exit(-1)
		return

	def input_stat(self):
		global token
		global token_line
		if (token.recognized_string == '('):
			token = self.get_token()
			if (token.family == identifier):
				id_place = token.recognized_string
				self.genQuad('inp',id_place,'_','_')			# prin apo to token gt thelw to id oxi thn ')'
				token_line = token.line_number
				token = self.get_token()
				if (token.recognized_string == ')'):
					token = self.get_token()
					return
				else:
					print('ERROR !! sth grammh ' + str(token_line) + '\n H paren8esh anoigei alla den kleinei swsta, perimename deksia parenthesh')
					exit(-1)
			else:
				print('ERROR !! sth grammh ' + str(token.line_number) + '\n Lathos eisodos, h metavlhth den exei oristei swsta ')
				exit(-1)
		else:
			print('ERROR !! sth grammh ' + str(token.line_number) + '\n H parenthesh den anoigei swsta, perimename aristerh parenthesh')
			exit(-1)
		return

	def actualparlist(self):
		global token
		self.actualparitem()		# an den brei oute in oute inout tote keno
		while (token.recognized_string == ','):
			token = self.get_token()
			self.actualparitem()
		return

	def actualparitem(self):
		# den vazoume sto pinaka sumvolwn gia to call
		global token
		if (token.recognized_string == 'in'):
			token = self.get_token()
			expression = self.expression()
			self.genQuad('par',expression,'CV','_')
		elif (token.recognized_string == 'inout'):
			token = self.get_token()
			if (token.family == identifier):
				next_name = token.recognized_string
				token = self.get_token()
				self.genQuad('par',next_name,'REF','_')
			else:
				print('ERROR !! sth grammh ' + str(token.line_number) + '\n Den exei oristei swsta h metavlhth meta to inout')
				exit(-1)
		elif(token.recognized_string == ')'):	# gia otan exoume keno sto call(actualparlist)
			return 								# den theloume next token
		else:
			print('ERROR !! sth grammh ' + str(token.line_number) + '\n Den exei oristei swsta to <in> h to <inout> ')
			exit(-1)
		return

	def condition(self):
		#Q1[0] = Btrue, Q1[1] = Bfalse
		global token
		Q1 = self.boolterm()
		Btrue = Q1[0]
		Bfalse = Q1[1]
		while (token.recognized_string == 'or'):
			token = self.get_token()
			self.backPatch(Bfalse, self.nextQuad())
			Q2 = self.boolterm()
			Btrue = self.merge(Btrue, Q2[0])
			Bfalse = Q2[1]
		return Btrue, Bfalse

	def boolterm(self):
		global token
		R1 = self.boolfactor()
		Btrue = R1[0]
		Bfalse = R1[1]
		while (token.recognized_string == 'and'):
			token = self.get_token()
			self.backPatch(Btrue, self.nextQuad())
			R2 = self.boolfactor()
			Bfalse = self.merge(Bfalse, R2[1])
			Btrue = R2[0]
		return Btrue, Bfalse

	def boolfactor(self):
		global token
		if (token.recognized_string == 'not'):
			token = self.get_token()
			if (token.recognized_string == '['):
				token = self.get_token()
				B = self.condition()
				if (token.recognized_string == ']'):
					token = self.get_token()
					Btrue = B[1]
					Bfalse = B[0]
				else:
					print('ERROR !! sth grammh ' + str(token.line_number) + '\n H agkylh anoigei alla den kleinei swsta, perimename deksia agkylh')
					exit(-1)
			else:
				print('ERROR !! sth grammh ' + str(token.line_number) + '\n Den exei anoiksei swsta h akgylh, perimename aristerh agkylh ')
				exit(-1)
		elif (token.recognized_string == '['):
			token = self.get_token()
			B = self.condition()
			if (token.recognized_string == ']'):
				token = self.get_token()
				Btrue = B[0]
				Bfalse = B[1]
			else:
				print('ERROR !! sth grammh ' + str(token.line_number) + '\n H agkylh anoigei alla den kleinei swsta, perimename deksia agkylh ')
				exit(-1)
		else:
			E1 = self.expression()
			relop = self.relational_oper()
			E2 = self.expression()
			Btrue = self.makeList(self.nextQuad())
			self.genQuad(relop,E1,E2,'_')
			Bfalse = self.makeList(self.nextQuad())
			self.genQuad('jump','_','_','_')
		return Btrue, Bfalse

	def expression(self): 						# synarthsh gia to '+'
		global token
		self.optional_sign()
		T1_place = self.term()
		while (token.recognized_string == '+' or token.recognized_string == '-'):
			operator_add = self.add_oper()
			T2_place = self.term()
			w = self.newTemp()
			self.genQuad(operator_add,T1_place,T2_place,w)
			T1_place = w
		E_place = T1_place 
		return E_place

	def term(self): 							# synarthsh gia to '*'
		global token
		F1_place = self.factor()
		while (token.recognized_string == '*' or token.recognized_string == '/'):
			operator_mul = self.mul_oper()
			F2_place = self.factor()
			w = self.newTemp()
			self.genQuad(operator_mul,F1_place,F2_place,w)
			F1_place = w
		T_place = F1_place
		return T_place

	def factor(self):
		global token
		global token_line
		if (token.family == number):
			F_place = token.recognized_string
			token = self.get_token()
		elif (token.recognized_string == '('): 	# metafora E_place sto F_place
			token = self.get_token()
			token_line = token.line_number 		# einai gia to print tou error
			E_place = self.expression()
			F_place = E_place
			if (token.recognized_string == ')'):
				token = self.get_token()
			else:
				print('ERROR !! sth grammh ' + str(token_line) + '\n H paren8esh anoigei alla den kleinei swsta, perimename deksia parenthsh')
				exit(-1)
		elif (token.family == identifier): 		# metafora id_place sto F_place
			F_save = token.recognized_string
			token = self.get_token()		
			id_place = self.idtail(F_save)		# gia na kanw to call sto idtail xreiazomai to onoma ths sunarthshs
			F_place = id_place
		else:
			print('ERROR !! sth grammh ' + str(token.line_number) + '\n Sto sugkekrimeno shmeio prepei na dothei eite arithmos eite aristerh parenthesh eite kapoio onoma sunarthshs (ID) ')
			exit(-1)
		return F_place 							# epistrefoume F gia to term (F1,F2)
		
	def idtail(self,name):
		global token
		global token_line
		if (token.recognized_string == '('):
			token = self.get_token()
			token_line = token.line_number
			self.actualparlist()
			w = self.newTemp()						# ftiaxnoume to w giati den gnwrizoume ti tha mas epistrepsei h sunarthsh
			self.genQuad('par', w, 'RET', '_')		# RET epistrofh timhs sunarthshs
			self.genQuad('call', name, '_', '_')    # kalei me to onoma ths sunarthshs
			if (token.recognized_string == ')'):
				token = self.get_token()
				return w
			else:
				print('ERROR !! sth grammh ' + str(token_line) + '\n H paren8esh anoigei alla den kleinei swsta, perimename deksia parenthsh')
				exit(-1)
		return name

	def optional_sign(self):
		global token
		if (token.recognized_string == '+' or token.recognized_string == '-'):
			self.add_oper()
		return

	def relational_oper(self):
		global token
		# gyrname to string pou exei diavastei prin eksetasoume to epomeno token
		if (token.recognized_string == '='):
			token = self.get_token()
			return '='
		elif (token.recognized_string == '>'):
			token = self.get_token()
			return '>'
		elif (token.recognized_string == '<>'):
			token = self.get_token()
			return '<>'
		elif (token.recognized_string == '<'):
			token = self.get_token()
			return '<'
		elif (token.recognized_string == '<='):
			token = self.get_token()
			return '<='
		elif (token.recognized_string == '>='):
			token = self.get_token()
			return '>='
		else:
			print('ERROR !! sth grammh ' + str(token.line_number) + '\n Den dothike swsto sumvolo. Anamenotan enas apo tous parakatw telestes (=,<=,>=,>,<,<>) ')
			exit(-1)

	def add_oper(self):
		global token
		if (token.recognized_string == '+'):
			operator = token.recognized_string
			token = self.get_token()
		elif (token.recognized_string == '-'):
			operator = token.recognized_string
			token = self.get_token()
		else:
			print('ERROR !! sth grammh ' + str(token.line_number) + '\n Den dothike swsto sumvolo. Anamenotan enas apo tous parakatw telestes (+,-) ')
			exit(-1)
		return operator 									# gia na pairnei timh to prwto orisma ths tetradas

	def mul_oper(self):
		global token
		if (token.recognized_string == '*'):
			operator = token.recognized_string
			token = self.get_token()
		elif (token.recognized_string == '/'):
			operator = token.recognized_string
			token = self.get_token()
		else:
			print('ERROR !! sth grammh ' + str(token.line_number) + '\n Den dothike swsto sumvolo. Anamenotan enas apo tous parakatw telestes (*,/) ')
			exit(-1)
		return operator 									# gia na pairnei timh to prwto orisma ths tetradas

def cCodeExporter():
	c = open("test.c","w")
	c.write("#include <stdio.h>\n")
	c.write("int main(){\n")
	c.write("\tint ")
	# write variables given by user
	for i in range(len(listOfVariables)):
		c.write(str(listOfVariables[i]) )
		if i <= len(listOfVariables)-2:						# gia na mhn mpainei to teleutaio (,) otan arxikopoioume tis metavlhtes sth C
			c.write(", ")
	c.write("; // variables \n")
	c.write("\tint ")
	# write temporary variables used by the program
	for i in range(len(listOfTemporaryVariables)):
		if(i == len(listOfTemporaryVariables)-1 ):
			c.write(str(listOfTemporaryVariables[i] + "; // temporary variable\n"))
		else:
			c.write(str(listOfTemporaryVariables[i] + ", "))
	for i in range(len(listForQuads)-1):
		if (str(listForQuads[i][1]) == "begin_block"):
			c.write("	L_" + str(listForQuads[i][0]) + ": \n")
		elif (str(listForQuads[i][1]) == "jump"):
			c.write("	L_" + str(listForQuads[i][0]) + ": " + "goto L_" + str(listForQuads[i][4]) + ";\n")
		elif (str(listForQuads[i][1]) == "+" or str(listForQuads[i][1]) == "-" or str(listForQuads[i][1]) == "*" or str(listForQuads[i][1]) == "/"):
			c.write("	L_" + str(listForQuads[i][0]) + ": " + str(listForQuads[i][4]) + " = " + str(listForQuads[i][2]) + " " + str(listForQuads[i][1]) + " " + str(listForQuads[i][3]) + ";\n")
		elif (str(listForQuads[i][1]) == ":="):
			c.write("	L_" + str(listForQuads[i][0]) + ": " + str(listForQuads[i][4]) + " = " + str(listForQuads[i][2]) + ";\n")
		elif (str(listForQuads[i][1]) == ">" or str(listForQuads[i][1]) == "<" or str(listForQuads[i][1]) == ">=" or str(listForQuads[i][1]) == "<="):
			c.write("	L_" + str(listForQuads[i][0]) + ": " + "if(" + str(listForQuads[i][2]) + " " + str(listForQuads[i][1]) + " " + str(listForQuads[i][3]) + ") goto L_" + str(listForQuads[i][4]) + ";\n")
		elif (str(listForQuads[i][1]) == "="):
			c.write("	L_" + str(listForQuads[i][0]) + ": " + "if(" + str(listForQuads[i][2]) + " == " + str(listForQuads[i][3]) + ") goto L_" + str(listForQuads[i][4]) + ";\n")
		elif (str(listForQuads[i][1]) == "<>"):
			c.write("	L_" + str(listForQuads[i][0]) + ": " + "if(" + str(listForQuads[i][2]) + " != " + str(listForQuads[i][3]) + ") goto L_" + str(listForQuads[i][4]) + ";\n")
		elif (str(listForQuads[i][1]) == "out"):
			c.write("	L_" + str(listForQuads[i][0]) + ": " + "printf(\"" + str(listForQuads[i][2]) + "= %d\", " + str(listForQuads[i][2]) + ");\n")
		elif (str(listForQuads[i][1]) == "inp"):
			c.write("	L_" + str(listForQuads[i][0]) + ": " + "scanf(\" %d\", &" + str(listForQuads[i][2]) + ");\n") #edw valame & to eixame 3exasei
		elif (str(listForQuads[i][1]) == "halt"):
			c.write("	L_" + str(listForQuads[i][0]) + ": {};\n")
			break;	
	c.write("}")
	c.close()

def intFile():
	j = open("test.int", "w")
	print("Edw typwnetai o endiamesos kwdikas")
	for i in range(len(listForQuads)):
		print (str(listForQuads[i][0])+" "+str(listForQuads[i][1])+" "+str(listForQuads[i][2])+" "+str(listForQuads[i][3])+" "+str(listForQuads[i][4]))	
		if(i == len(listForQuads)-1):
			j.write(str(listForQuads[i][0])+" "+str(listForQuads[i][1])+" "+str(listForQuads[i][2])+" "+str(listForQuads[i][3])+" "+str(listForQuads[i][4]))
		else:	
			j.write(str(listForQuads[i][0])+" "+str(listForQuads[i][1])+" "+str(listForQuads[i][2])+" "+str(listForQuads[i][3])+" "+str(listForQuads[i][4]) + "\n")
	j.close()

#PINAKAS SYMVOLWN
#------------------------------------------------------------------------------------------------------------------------------------------------------
class Entity():
	def __init__(self):
		self.name = ''
		self.array = ['','','','','','',[]] # 0:datatype 1:value 2:offset 3:mode 4:startingQuad 5:frameLength 6:formalParameters[]
		self.typos = ''

class Scope():
	def __init__(self):
		self.name = ''
		self.entityList = []
		self.nestingLevel = 0
		self.nextScope = None	

class Argument():
	# type den to vazoume giati einai panta int
	def __init__(self):
		self.name = '' # 8a xreiastei na kanoume kapoia Arguments -> Entity opote prepei na perastei kai ena onoma
		self.parMode = ''

def addArgument(object): # vazoume to argument
	global readScope
	readScope.entityList[-1].array[6].append(object)

def addEntity(object):
	global readScope
	readScope.entityList.append(object)
	

def createScope(name):
	global readScope
	newScope = Scope()
	newScope.name = name
	if(readScope == None):
		newScope.nestingLevel = 0
	else:
		newScope.nestingLevel = readScope.nestingLevel + 1
		newScope.nextScope = readScope 		# pernaw to palio readScope mesa sto kainourio newScope (douleuei san nodes)
	readScope = newScope 					# ananewnw to readScope kai mpainei to kainourio

def removeScope(): 		# diagrafei to readScope
	global readScope
	deleteScope = readScope
	readScope = readScope.nextScope
	print("Egine remove to Scope " + deleteScope.name)
	print("-------------------------------------------------------------------------------------")
	del deleteScope


def calculateOffset():
	counter = 0
	if(len(readScope.entityList) != 0):
		for i in range(len(readScope.entityList)):
			if(readScope.entityList[i].typos == 'Variable' or readScope.entityList[i].typos == 'Parameter' or readScope.entityList[i].typos == 'TemporaryVariable'):
				counter += 1
	return 12+counter*4 	# to offset mas

def calculateQuad():
	readScope.nextScope.entityList[-1].array[4] = antik_syntakt.nextQuad()	# pairnw to teleutaio stoixeio ths listas twn entity...to 4 einai gia to array sto entity

# to framelength tha einai 4 bytes meta to teleutaio offset tou teletaiou entity sto kathe scope
def calculateFramelength():
	readScope.nextScope.entityList[-1].array[5] = calculateOffset()

def addParameterToScope():
	global readScope
	for i in readScope.nextScope.entityList[-1].array[6]:
		entity = Entity()
		entity.typos = 'Parameter'
		entity.name = i.name
		entity.array[3] = i.parMode
		entity.array[2] = calculateOffset()
		addEntity(entity)

def print_pinakas_symvolwn():
	scope=readScope
	print("Pinakas Symvolwn Vhmatika")
	symb.write("Pinakas Symvolwn Vhmatika\n")
	print("Number of Nesting Levels: " + str(scope.nestingLevel+1))
	symb.write("Number of Nesting Levels: " + str(scope.nestingLevel+1)+"\n")
	while scope!= None:
		print("Scope: "+"name:"+scope.name+", nestingLevel:"+str(scope.nestingLevel))
		symb.write("Scope: "+"name:"+scope.name+", nestingLevel:"+str(scope.nestingLevel)+"\n")
		for entity in scope.entityList:
			if(entity.typos == 'Variable'):
				print("	Entity: ["+" name:"+entity.name+",  typos:"+entity.typos+",  offset:"+str(entity.array[2])+"]")
				symb.write("	Entity: ["+" name:"+entity.name+",  typos:"+entity.typos+",  offset:"+str(entity.array[2])+"]\n")
			elif(entity.typos == 'Parameter'):
				print("	Entity: ["+" name:"+entity.name+",  typos:"+entity.typos+",  mode:"+entity.array[3]+",  offset:"+str(entity.array[2])+"]")
				symb.write("	Entity: ["+" name:"+entity.name+",  typos:"+entity.typos+",  mode:"+entity.array[3]+",  offset:"+str(entity.array[2])+"]\n")
			elif(entity.typos == 'Function'):
				print("	Entity: ["+" name:"+entity.name+",  typos:"+entity.typos+",  dataType:"+entity.array[0]+",  offset:("+str(entity.array[2])+"),  startQuad:"+str(entity.array[4])+",  frameLength:"+str(entity.array[5])+"]")
				symb.write("	Entity: ["+" name:"+entity.name+",  typos:"+entity.typos+",  dataType:"+entity.array[0]+",  offset:("+str(entity.array[2])+"),  startQuad:"+str(entity.array[4])+",  frameLength:"+str(entity.array[5])+"]\n")
				for argument in entity.array[6]:
					print("		Argument: ["+" name:"+argument.name+", parMode:"+argument.parMode+"]")
					symb.write("		Argument: ["+" name:"+argument.name+", parMode:"+argument.parMode+"]\n")
			elif(entity.typos == 'Procedure'):
				print("	Entity: ["+" name:"+entity.name+",  typos:"+entity.typos+",  dataType:"+entity.array[0]+",  offset:("+str(entity.array[2])+"),  startQuad:"+str(entity.array[4])+",  frameLength:"+str(entity.array[5])+"]")
				symb.write("	Entity: ["+" name:"+entity.name+",  typos:"+entity.typos+",  dataType:"+entity.array[0]+",  offset:("+str(entity.array[2])+"),  startQuad:"+str(entity.array[4])+",  frameLength:"+str(entity.array[5])+"]\n")
				for argument in entity.array[6]:
					print("		Argument: ["+" name:"+argument.name+", parMode:"+argument.parMode+"]")
					symb.write("		Argument: ["+" name:"+argument.name+", parMode:"+argument.parMode+"]\n")
			elif(entity.typos == 'TemporaryVariable'):
				print("	Entity: ["+" name:"+entity.name+",  typos:"+entity.typos+",  offset:"+str(entity.array[2])+"]")
				symb.write("	Entity: ["+" name:"+entity.name+",  typos:"+entity.typos+",  offset:"+str(entity.array[2])+"]\n")

		scope= scope.nextScope
	print("-------------------------------------------------------------------------------------")
	symb.write("-------------------------------------------------------------------------------------\n")

#######################################################
################### TELIKOS KWDIKAS ###################
#######################################################
def gnlvcode(x):	
	tempScope = readScope				# den xreiazetai to tempScope (einai gia dikh mas dieukolhnsh)
	stackParentCounter = 0
	flagForWhile = True
	while (flagForWhile):
		if (tempScope == None):			# anazhtoume sto pinaka sumvolwn
			print("ERROR 1 den uparxei sto pinaka sumvolwn to "+ str(x))
			exit(-1)
		for entity in tempScope.entityList:
			if (entity.name == x):
				asm.write("lw t0, -4(sp) \n")		# prosexw giati to prwto lw to grafw outws h allws (dhladh tou patera)
				for j in range(stackParentCounter):
					asm.write("lw t0, -4(t0) \n")
				asm.write("addi t0, t0, -" + str(entity.array[2]) +"\n")
				flagForWhile = False
				break
		if (flagForWhile):
			stackParentCounter += 1					# metraei tous progonous pou epsakse gia na brethei to entity
			tempScope = tempScope.nextScope

# v   : onoma metablhths (theloume na diabasoume thn timh ths)
# reg : kataxwrhths pou tha topothetithei
def loadvr(v, reg):
	tempScope = readScope
	stackParentCounter = 0
	flagForWhile = True
	if (str(v).isnumeric()):					# check if integer
		asm.write("\tli " + reg + ", "+str(v)+"\n") 		# sumplhrwsh (li,tr,v)
	else :
		while (flagForWhile):
			if (tempScope == None):
				print("ERROR 2 den uparxei sto pinaka sumvolwn to : "+ str(v))
				exit(-1)
			for ent in tempScope.entityList:
				if (ent.name.__eq__(v)):
					entity = ent
					flagForWhile = False
					break
			if (flagForWhile):
				stackParentCounter += 1				# metraei tous progonous pou epsakse gia na brethei to entity
				tempScope = tempScope.nextScope
		# check global variable (to declare omws den mpainei sto pinaka sumvolwn)
		# (lw reg,-offset(gp)) lw : anagnwsh ths timhs
		if (tempScope.nestingLevel == 0 and (entity.typos == 'TemporaryVariable' or entity.typos == 'Variable')):
			asm.write("\tlw "+reg+", -"+str(entity.array[2]) +"(gp) \n")
		# temporary - localvariable - CV(perasma me timh)
		# (lw reg,-offset(sp))
		elif (stackParentCounter == 0 and (entity.typos == 'TemporaryVariable' or entity.typos == 'Variable' or entity.array[3] == 'CV')):
			asm.write("\tlw "+ reg +", -"+str(entity.array[2]) +" \n")
		# REF(perasma me anafora)
		# (lw t0,-offset(sp)    lw reg,(t0))
		elif (stackParentCounter == 0 and entity.array[3] == 'REF'):
			asm.write("\tlw t0, -"+str(entity.array[2])+"(sp) \n")
			asm.write("\tlw "+ reg +", (t0) \n")
		# localvariable - CV(perasma me timh)
		# (gnlvcode() produce('lw reg,(t0)'))
		elif (stackParentCounter != 0 and (entity.typos == 'Variable' or entity.array[3] == 'CV')): # check global variable
			gnlvcode(v)
			asm.write("\tlw "+ reg +", (t0) \n")
		elif (stackParentCounter != 0 and entity.array[3] == 'REF'): # check global variable
			gnlvcode(v)
			asm.write("\tlw t0,(t0) \n")
			asm.write("\tlw "+ reg +", (t0) \n")

# reg : source register
# v   : target variable (theloume na diabasoume thn timh ths)
def storerv(reg, v):
	tempScope = readScope
	stackParentCounter = 0
	flagForWhile = True
	while (flagForWhile):
		if (tempScope == None):
			print("ERROR 3 den uparxei sto pinaka sumvolwn to "+ str(v))
			exit(-1)
		for ent in tempScope.entityList:
			if (ent.name == v):
				entity = ent
				flagForWhile = False
				break
		if (flagForWhile):
			stackParentCounter += 1			# metraei tous progonous pou epsakse gia na brethei to entity
			tempScope = tempScope.nextScope
	# sw : apothikeush ths timhs
	if (tempScope.nestingLevel == 0 and (entity.typos == 'TemporaryVariable' or entity.typos == 'Variable')):
		asm.write("\tsw "+reg+", -"+str(entity.array[2]) +"(gp) \n")
	elif (stackParentCounter == 0 and (entity.typos == 'TemporaryVariable' or entity.typos == 'Variable' or entity.array[3] == 'CV')):
		asm.write("\tsw "+reg+", -"+str(entity.array[2]) +"(sp) \n")
	elif (stackParentCounter == 0 and entity.array[3] == 'REF'):
		asm.write("\tlw t0, -"+str(entity.array[2]) +"(sp) \n")
		asm.write("\tsw "+reg+", (t0) \n")
	elif (stackParentCounter != 0 and (entity.typos == 'Variable' or entity.array[3] == 'CV')):
		gnlvcode(v)
		asm.write("\tsw "+reg+", (t0) \n")
	elif (stackParentCounter != 0 and entity.array[3] == 'REF'):
		gnlvcode(v)
		asm.write("\tlw t0, (t0) \n")
		asm.write("\tsw "+reg+", (t0) \n")

def assemblyCode():	
	global tempValueOfQuads
	global countParam
	for i in range(tempValueOfQuads,len(listForQuads)):
		quad = listForQuads[i]
		if (str(quad[1]).__eq__(":=")):				# ekxwrhsh
			asm.write("L"+str(quad[0])+":\n")		# mpainei eswterika se kathena giati exoume to main:
			loadvr(quad[2],"t1")
			storerv("t1",quad[4])
		elif (str(quad[1]).__eq__("+")):			# operations
			asm.write("L"+str(quad[0])+":\n")
			loadvr(quad[2],"t1")
			loadvr(quad[3],"t2")
			asm.write("\tadd t1,t1,t2 \n")
			storerv("t1",quad[4])
		elif (str(quad[1]).__eq__("-")):			# operations
			asm.write("L"+str(quad[0])+":\n")
			loadvr(quad[2],"t1")
			loadvr(quad[3],"t2")
			asm.write("\tsub t1,t1,t2 \n")
			storerv("t1",quad[4])
		elif (str(quad[1]).__eq__("*")):			# operations
			asm.write("L"+str(quad[0])+":\n")
			loadvr(quad[2],"t1")
			loadvr(quad[3],"t2")
			asm.write("\tmul t1,t1,t2 \n")
			storerv("t1",quad[4])	
		elif (str(quad[1]).__eq__("/")):			# operations
			asm.write("L"+str(quad[0])+":\n")
			loadvr(quad[2],"t1")
			loadvr(quad[3],"t2")
			asm.write("\tdiv t1,t1,t2 \n")
			storerv("t1",quad[4])
		elif (str(quad[1]).__eq__("jump")):			# jump
			asm.write("L"+str(quad[0])+":\n")
			asm.write("\tj L"+str(quad[4])+"\n")
		elif (str(quad[1]).__eq__("=")):			# beq(=) (gia thn C-imple)
			asm.write("L"+str(quad[0])+":\n")
			loadvr(quad[2],"t1")
			loadvr(quad[3],"t2")
			asm.write("\tbeq t1,t2, L"+str(quad[4])+"\n")
		elif (str(quad[1]).__eq__("<>")):			# bne(<>) edwwww
			asm.write("L"+str(quad[0])+":\n")
			loadvr(quad[2],"t1")
			loadvr(quad[3],"t2")
			asm.write("\tbne t1,t2, L"+str(quad[4])+"\n")
		elif (str(quad[1]).__eq__("<")):			# blt(<)
			asm.write("L"+str(quad[0])+":\n")
			loadvr(quad[2],"t1")
			loadvr(quad[3],"t2")
			asm.write("\tblt t1,t2, L"+str(quad[4])+"\n")
		elif (str(quad[1]).__eq__(">")):			# bgt(>)
			asm.write("L"+str(quad[0])+":\n")
			loadvr(quad[2],"t1")
			loadvr(quad[3],"t2")
			asm.write("\tbgt t1,t2, L"+str(quad[4])+"\n")
		elif (str(quad[1]).__eq__("<=")):			# ble(<=)
			asm.write("L"+str(quad[0])+":\n")
			loadvr(quad[2],"t1")
			loadvr(quad[3],"t2")
			asm.write("\tble t1,t2, L"+str(quad[4])+"\n")
		elif (str(quad[1]).__eq__(">=")):			# bge(>=)
			asm.write("L"+str(quad[0])+":\n")
			loadvr(quad[2],"t1")
			loadvr(quad[3],"t2")
			asm.write("\tbge t1,t2, L"+str(quad[4])+"\n")
		elif (str(quad[1]).__eq__("halt")):			# halt (end of program)
			asm.write("L"+str(quad[0])+":\n")
			asm.write("\tli a0,0 \n")
			asm.write("\tli a7,93 \n")
			asm.write("\tecall \n")
		# sto end_block ths main dn tha ftasoume pote giati tha exei mpei pio prin sto halt kai tha exei termatisei h assembly me to ecall
		elif (str(quad[1]).__eq__("end_block")):
			asm.write("L"+str(quad[0])+":\n")
			asm.write("\tlw ra, (sp) \n")
			asm.write("\tjr ra \n")
		elif (quad[1].__eq__("begin_block") and readScope.nestingLevel == 0):	# main (mono)
			asm.write("main: \n")
			asm.write("L"+str(quad[0])+":\n")
			asm.write("\taddi sp,sp,"+str(readScope.entityList[-1].array[2]+4)+"\n")		# mesw tou offset+4 tha paroume to framelength
			asm.write("\tmv gp,sp \n")
		elif (str(quad[1]).__eq__("begin_block")):	# afou den mphke sto parapanw begin_block tote sigoura dn eimaste sthn main
			asm.write("L"+str(quad[0])+":\n")
			asm.write("\tsw ra, (sp) \n")
		elif (str(quad[1]).__eq__('retv')):
			asm.write("L"+str(quad[0])+":\n")
			loadvr(quad[2],"t1")	#edw mporei na 8elei kataxwrhth a0-a7 gia epistrofh apo synarthsh				# ston endiameso mpainei sthn thesh [2]3 to x sto teliko to exei sthn teleutaia
			asm.write("\tlw t0, -8(sp) \n")
			asm.write("\tsw t1, (t0) \n")
		elif (str(quad[1]).__eq__('inp')):			# opws brethike stis diafanies
			asm.write("L"+str(quad[0])+":\n")
			asm.write("\tli a7, 5 \n")
			asm.write("\tecall \n")
		elif (str(quad[1]).__eq__('out')):			# opws brethike stis diafanies
			asm.write("L"+str(quad[0])+":\n")
			asm.write("\tmv a0, t0 \n")
			asm.write("\tli a7, 1 \n")
			asm.write("\tecall \n")
			asm.write("\tla a0, str_nl \n")
			asm.write("\tli a7, 4 \n")
			asm.write("\tecall \n")		
		elif (str(quad[1]).__eq__("par") and str(quad[3]).__eq__("CV")):		# perasma me timh
			asm.write("L"+str(quad[0])+":\n")
			countParam += 1							# mporei na prepei na paei katw apo to d
			loadvr(quad[2],"t0")
			#loadvr(quad[2],"sp")# edw eprepe t0		# o kataxwrhths tha sumplhrwthei monos tou se sp
			d = 12 + (countParam-1)*4
			asm.write("\tsw t0, -"+str(d)+"(fp) \n")	# antigrafei sthn thesh mnhmhs tou [fp+d) oti kaname load ston t0	
		# eggrafetai sto eggrafhma drasthriopoihshs sto xwro pou exei kraththei gia auth
		# exoume metaferei ton fp sthn arxh tou eggrafhmatos drasthriopoihsh ths kalousas sunarthshs
		elif (str(quad[1]).__eq__("par") and str(quad[3]).__eq__("REF")):		# perasma me anafora
			tempScope = readScope
			flagForWhile = True
			asm.write("L"+str(quad[0])+":\n")
			while (flagForWhile):
				if (tempScope == None):
					print("ERROR 4 den uparxei sto pinaka sumvolwn to "+ str(x))
					exit(-1)
				for ent in tempScope.entityList:
					if (ent.name == quad[2]):
						entity = ent
						flagForWhile = False
						break
				if (flagForWhile):
					tempScope = tempScope.nextScope
			# sto perasma me anafora prepei na 3eroume an kai pws exei perastei h metavlhth se klhsh progonou wste na allaxtei katallhla
			# epishs prepei na 3eroume to offset sto opoio 8a graftoun oi allages
			if (tempScope.nestingLevel.__eq__(readScope.nestingLevel)):		# idio bathos fwliasmatos
				if (entity.typos.__eq__('Variable')):
					countParam += 1
					asm.write("\taddi t0, sp, -"+str(entity.array[2]) +"\n")
					asm.write("\tsw t0, -"+str(12+4*(countParam-1))+"(fp) \n")
				elif (entity.typos.__eq__('Parameter') and entity.mode.__eq__('CV')):
					countParam += 1 					# h 8esh ths parametrou mesa stis paren8eseis ths klhshs
					asm.write("\taddi t0, sp, -"+str(entity.array[2]) +"\n")
					asm.write("\tsw t0, -"+str(12+4*(countParam-1))+"(fp) \n")
				elif (entity.typos.__eq__('Parameter') and entity.mode.__eq__('REF')):
					countParam += 1 					# h 8esh ths parametrou mesa stis paren8eseis ths klhshs
					asm.write("\tlw t0, -"+str(entity.array[2]) +"(sp)\n")
					asm.write("\tsw t0, -"+str(12+4*(countParam-1))+"(fp) \n")	
			elif (tempScope.nestingLevel != readScope.nestingLevel):	# to tempScope den ginetai na exei megalutero nesting level apo to readScope
				gnlvcode(quad[2])
				if (entity.typos.__eq__('Parameter') and entity.mode.__eq__('REF')):
					countParam += 1 					# h 8esh ths parametrou mesa stis paren8eseis ths klhshs
					asm.write("\tlw t0, (t0) \n")
					asm.write("\tsw t0, -"+str(12+4*(countParam-1))+"(fp) \n")
				else:
					asm.write("\tsw t0, -"+str(12+4*(countParam-1))+"(fp) \n")
		# return (x)
		elif (str(quad[1]).__eq__("par") and str(quad[3]).__eq__("RET")):		# perasma me EPISTROFH
			tempScope = readScope
			flagForWhile = True
			asm.write("L"+str(quad[0])+":\n")
			while (flagForWhile):
				if (tempScope == None):
					print("ERROR 5 den uparxei sto pinaka sumvolwn to "+ str(x))
					exit(-1)
				for ent in tempScope.entityList:
					if (ent.name.__eq__(quad[2])):
						asm.write("\taddi t0, sp, -"+str(ent.array[2]) +" \n")
						asm.write("\tsw t0, -8(fp) \n")
						flagForWhile = False
						break
				if (flagForWhile):
					tempScope = tempScope.nextScope
		elif (quad[1].__eq__('call')):
			tempScope = readScope
			flagForWhile = True
			asm.write("L"+str(quad[0])+":\n")
			while (flagForWhile):
				if (tempScope == None):
					print("ERROR 6 den uparxei sto pinaka sumvolwn to "+ str(x))
					exit(-1)
				for ent in tempScope.entityList:
					if (ent.name.__eq__(quad[2])):
						entity = ent
						flagForWhile = False
						break
				if (flagForWhile):
					tempScope = tempScope.nextScope
			if (tempScope.nestingLevel.__eq__(readScope.nestingLevel)):		# idio bathos fwliasmatos
				asm.write("\tlw t0, -4(sp) \n")
				asm.write("\tsw t0, -4(fp) \n")
			elif (tempScope.nestingLevel != readScope.nestingLevel):	# to tempScope den ginetai na exei megalutero nesting level apo to readScope
				asm.write("\tsw sp, -4(fp) \n")
			asm.write("\taddi sp, sp, "+str(entity.array[5])+" \n")
			asm.write("\tjal L"+ str(entity.array[4])+" \n") #SWSTO yparxei startingQuad
			#asm.write("\tjal L"+ str(quad[0])+" \n") AUTO EINAI LATHOS	# bazoume to label pou kaleitai gia na kanei jump
			asm.write("\taddi sp, sp, -"+str(entity.array[5])+" \n")
			countParam = 0									# telos mhdenizoume to counter gia tis parametrous
	tempValueOfQuads = len(listForQuads)					# theloume kathe fora na krataei posa quads eixe prin

f = open(sys.argv[1], "r")
#f = open("_test_parser.ci", "r")
symb = open("test.symb", "w")
asm = open("test.asm", "w")
asm.write(".data\nstr_nl: .asciz \"\\n\" \n.text \n")	# xreiazetai gia thn allagh grammhs sto print
asm.write("L0:\n\tj main \n")		# to kanoume sthn arxh ths assembly (gia na ektelestei prwta o kwdikas ths main)
### endiamesos kwdikas ###
counterQuads = 1
listOfTemporaryVariables = []		
listOfVariables = []				# gia ta tis metablhtes pou dhlwnei o xrhsths(sto c arxeio
T_ = 1
### endiamesos kwdikas ###
global listForQuads
listForQuads = []
global p1
tempValueOfQuads = 0				# kratame ta quads pou pername sto teliko kwdika gia metatroph se assembly
countParam = 0						# kratame tis parametrous pou perniountai kathe fora stis sunarthseis tou telikou kwdika
readScope = None 					# to xrhsimopoioume gia na kratame to pio kainourio scope mas (pinakas symvolwn)
p1 = Token()						# to dinoume xwris orismata giati exoun oristei sto constructor
antik_lekt = Lex(1,f,p1)			# dhmiourgoume to antikeimeno Lex
antik_syntakt = Parser(antik_lekt)
antik_syntakt.syntax_analyzer()
cCodeExporter()
intFile()

'''
#testing gia ton lektiko analuth
f = open("factorial.ci", "r")
global p1
p1 = Token()		# to dinoume xwris orismata giati exoun oristei sto constructor
antik_lekt = Lex(1,f,p1)	# dhmiourgoume to antikeimeno Lex
while(True):
        antik_lekt.lex_analysis()	# psaxnoume gia kathe mia lektikh monada
        if (antik_lekt.token.recognized_string == ''):	# an doume EOF stamatame
                break
        print(p1.__str__())	# tupwnoume 
'''
