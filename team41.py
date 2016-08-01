import random

class Player41:

	def update_lists(self,game_board, block_stat, move_ret, fl):
		game_board[move_ret[0]][move_ret[1]] = fl

		block_no = (move_ret[0]/3)*3 + move_ret[1]/3
		id1 = block_no/3
		id2 = block_no%3
		mflg = 0

		flag = 0
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if game_board[i][j] == '-':
					flag = 1

		if flag == 0:
			block_stat[block_no] = 'D'

		if block_stat[block_no] == '-':
			if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
				mflg=1
			if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
				mflg=1
			if mflg != 1:
	                    for i in range(id2*3,id2*3+3):
	                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-' and game_board[id1*3][i] != 'D':
	                                mflg = 1
	                                break
			if mflg != 1:
	                    for i in range(id1*3,id1*3+3):
	                        if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-' and game_board[i][id2*3] != 'D':
	                                mflg = 1
	                                break
		if mflg == 1:
			block_stat[block_no] = fl
		return mflg

	def __init__(self):
		self.cnt = 0
		self.dep = 5

	def move(self,temp_board,temp_block,old_move,flag):
		#List of permitted blocks, based on old move.
		a = -100000000
		b = 100000000
		temp=self.alphabeta(temp_board[:],temp_block[:] ,self.dep , a , b, True,old_move,flag)
		print temp
		return temp

	def board_heu_check(self,count1,count2):
		return_obj=[0 for i in range(3)]



	def block_heu_check(self,count1,count2):
		return_obj=[0 for i in range(3)]
		return_obj[1]=0
		if(count1==0):
			if(count2==1):
				return_obj[0] = -2.5;

			if(count2==2):
				return_obj[0] = -5;

			if(count2==3):
				return_obj[1]=1
				return_obj[0]=-10

		elif(count2==0):
			if(count1==0):
				return_obj[0] = 0

			elif(count1==1):
				return_obj[0] = 2.5

			elif(count1==2):
				return_obj[0]=5
			else:
				return_obj[0]=10
				return_obj[1]=1;

		else:
			if(count1 < count2):
				return_obj[0] = -1
			elif(count1 == count2):
				return_obj[0] = 1
			else:
				return_obj[0] = 2

		return return_obj[:]


	def alphabeta(self,board ,block ,depth , a , b,maximizingPlayer,old_move,flag):
		if(depth == 0):
			#print flag
			return self.heu(board,block,flag)

		if maximizingPlayer:
			v=-100000
		else:
			v=100000

		cells = self.get_empty_cells_out_of(board,self.determine_blocks_allowed(old_move,block),block);

		if(len(cells)==0):
			cells = self.get_empty_cells_out_of(board,range(0,8),block);


		temp = []

		#random.shuffle(cells)
		for i in cells:
			
			temp_block = ['-' for z in range(10)]
			for j  in range(0,len(block)):
				temp_block[j] = block[j]


			if maximizingPlayer:
				self.update_lists(board,temp_block,i,flag)
				vtemp = self.alphabeta(board,temp_block,depth - 1, a , b , False,i,flag)

			else:
				flag1 = ''
				if flag == 'x':
					flag1 = 'o'
				elif flag == 'o':
					flag1 = 'x'
				self.update_lists(board , temp_block , i ,flag1 )
				vtemp = self.alphabeta(board,temp_block,depth - 1, a , b , True,i,flag)

			board[i[0]][i[1]]='-'

			if maximizingPlayer:
					if(vtemp > v):
						v = vtemp
						temp = i
					
					a = max(a,v)
					if(b <= a):
						break

			else:

					if(vtemp < v):
						v = vtemp
						temp = i

					b = min(b,v)
					if(b <= a):
						break

		if maximizingPlayer:
			if(depth == self.dep):
				print temp
				return temp

		return v


	def check(self,i,board,flag):
		row = (i / 3) * 3
		col = (i % 3) * 3
		block = ['-' for z in range(10)]
		cnt = 0
		for i in range(row,row+3):
			for j in range(col, col + 3):
				block[cnt] = board[i][j]
				cnt += 1
		
		value = 0
		for num in range(0,3):
			count1 = 0
			count2 = 0
			for i in range(3*num,3*num+3):
				if(block[i]==flag):
					count1 += 1
				elif(block[i]!='-'):
					count2 += 1

			temp_arr=self.block_heu_check(count1,count2)
			#print temp_arr

			if temp_arr[1]==1:
				return temp_arr[0]
			else:
				value+=temp_arr[0]

		for num in range(3):
			count1=0
			count2=0
			for i in range(num,9,3):
				if(block[i]==flag):
					count1 += 1
				elif(block[i]!='-'):
					count2 += 1


			temp_arr=self.block_heu_check(count1,count2)

			if temp_arr[1]==1:
				return temp_arr[0]
			else:
				value+=temp_arr[0]

		count1 = 0
		count2 = 0
		for i in range(0,9,4):
			if(block[i]==flag):
				count1 += 1
			elif(block[i]!='-'):
				count2 += 1

		temp_arr=self.block_heu_check(count1,count2)
			
		if temp_arr[1]==1:
			return temp_arr[0]
		else:
			value+=temp_arr[0]


		count1 = 0
		count2 = 0
		for i in range(2,7,2):
			if(block[i]==flag):
				count1 += 1
			elif(block[i]!='-'):
				count2 += 1

		temp_arr=self.block_heu_check(count1,count2)
			
		if temp_arr[1]==1:
			return temp_arr[0]
		else:
			value+=temp_arr[0]

		return value;


	def heu(self,board,block,flag):
		value = 0

		for i in range(0,9):
			if i in [1,3,5,7]:
				value +=  3 * self.check(i,board,flag)
			elif i == 4:
				value += 4 * self.check(i,board,flag)
			else:
				value += 2 * self.check(i,board,flag)			

		for num in range(3):
			count1 = 0
			count2 = 0
			for i in range(3*num,3*(num)+3):
				if(block[i]==flag):
					count1 += 1
				elif(block[i]!='-'):
					count2 += 1

			if(count1==0):
				if(count2==1):
					value -= 25

				if(count2==2):
					value -= 50;

				if(count2==3):
					return -1000;

			elif(count2==0):
				if(count1==0):
					value += 0

				elif(count1==1):
					value += 25

				elif(count1==2):
					for i in range(0,3):
						if(block[i]=='-'):
							temp_cond = self.check(i,board,flag)
							if(temp_cond < 0):
								value -= 50
							else:
								value += 60
				else:
					return 1000;

			else:
				value -= 10

		
		for num in range(3):
			count1 = 0
			count2 = 0
			for i in range(num,9,3):
				if(block[i]==flag):
					count1 += 1
				elif(block[i]!='-'):
					count2 += 1

			if(count1==0):
				if(count2==1):
					value -= 25;

				if(count2==2):
					value -= 50;

				if(count2==3):
					return -1000;

			elif(count2==0):
				if(count1==0):
					value += 10
				elif(count1==1):
					value += 25
				elif(count1==2):
					for i in range(0,9,3):
						if(block[i]=='-'):
							temp_cond = self.check(i,board,flag)
							if(temp_cond < 0):
								value -= 50
							else:
								value += 60
				else:
					return 1000;

			else:
				value -= 10


		count1 = 0
		count2 = 0
		for i in range(0,9,4):
			if(block[i]==flag):
				count1 += 1
			elif(block[i]!='-'):
				count2 += 1

		if(count1==0):
			if(count2==1):
				value -= 35;

			if(count2==2):
				value -= 60;

			if(count2==3):
				return -1000;

		elif(count2==0):
			if(count1==0):
				value += 10
			elif(count1==1):
				value += 35
			elif(count1==2):
				for i in range(0,9,4):
					if(block[i]=='-'):
						temp_cond = self.check(i,board,flag)
						if(temp_cond < 0):
							value -= 50
						else:
							value += 60
			else:
				return 1000;

		else:
			value -= 10

		count1 = 0
		count2 = 0
		for i in range(2,7,2):
			if(block[i]==flag):
				count1 += 1
			elif(block[i]!='-'):
				count2 += 1

		if(count1==0):
			if(count2==1):
				value -= 35;

			if(count2==2):
				value -= 60;

			if(count2==3):
				return -1000;

		elif(count2==0):
			if(count1==0):
				value += 10
			elif(count1==1):
				value += 35
			elif(count1==2):
				for i in range(2,7,2):
					if(block[i]=='-'):
						temp_cond = self.check(i,board,flag)
						if(temp_cond < 0):
							value -= 50
						else:
							value += 60
			else:
				return 1000;

		else:
				value -= 10

		return value;

	def determine_blocks_allowed(self,old_move, block_stat):
		blocks_allowed = []
		if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
			blocks_allowed = [1,3]
		elif old_move[0] % 3 == 0 and old_move[1] % 3 == 2:
			blocks_allowed = [1,5]
		elif old_move[0] % 3 == 2 and old_move[1] % 3 == 0:
			blocks_allowed = [3,7]
		elif old_move[0] % 3 == 2 and old_move[1] % 3 == 2:
			blocks_allowed = [5,7]
		elif old_move[0] % 3 == 0 and old_move[1] % 3 == 1:
			blocks_allowed = [0,2]
		elif old_move[0] % 3 == 1 and old_move[1] % 3 == 0:
			blocks_allowed = [0,6]
		elif old_move[0] % 3 == 2 and old_move[1] % 3 == 1:
			blocks_allowed = [6,8]
		elif old_move[0] % 3 == 1 and old_move[1] % 3 == 2:
			blocks_allowed = [2,8]
		elif old_move[0] % 3 == 1 and old_move[1] % 3 == 1:
			blocks_allowed = [4]
		else:
			sys.exit(1)
		final_blocks_allowed = []
		for i in blocks_allowed:
			if block_stat[i] == '-':
				final_blocks_allowed.append(i)
		return final_blocks_allowed

	def get_empty_cells_out_of(self,gameb, blal,block_stat):
		cells = []  # it will be list of tuples
		#Iterate over possible blocks and get empty cells
		for block_num in blal:
			i = block_num/3
			j = block_num%3
			for x in range(i*3,i*3+3):
				for y in range(j*3,j*3+3):
					if gameb[x][y] == '-':
						cells.append((x,y))

		# If all the possible blocks are full, you can move anywhere
		if cells == []:
			new_blal = []
			all_blal = [i for i in range(9)]
			for i in all_blal:
				if block_stat[i]=='-':
					new_blal.append(i)

			for idb in new_blal:
				id1 = idb/3
				id2 = idb%3
				for i in range(id1*3,id1*3+3):
					for j in range(id2*3,id2*3+3):
						if gameb[i][j] == '-':
							cells.append((i,j))
		return cells
