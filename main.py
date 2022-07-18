from base64 import b64encode, b64decode, b85decode, b85encode
from cryptography.fernet import Fernet
from tkinter import filedialog
import tkinter as tk
import os
import clipboard as cl

 
os.system('mode con:cols=100 lines=30')
root = tk.Tk()
root.withdraw()

def encode():
	file_path = filedialog.askopenfilename()
	if file_path != '':
		file_size = os.path.getsize(file_path)
		if file_size < 52428800:
			print(file_path)
			new_file_path = file_path.split('/')
			file_name = new_file_path[-1]
			new_file_path.pop()
			org_filepath = ''
			for i in new_file_path:
				org_filepath = org_filepath + i + '/'
			is_pass = False
			while not is_pass:
				try:
					passw = input("Set a password : ").encode('utf-8')
					bs4 = b64encode(passw)
					bs4 = bs4.replace(b'==', b'=')
					if len(bs4) > 44:
						bs4 = bs4[:43]+b'='
					if len(bs4) < 44:
						lenb = 44 - len(bs4)
						for _ in range(lenb):
							bs4 = b'1' + bs4
					file = open(file_path,'rb').read()
					f = Fernet(bs4)
					is_pass = True
				except:
					print('\33[31m'+'That password won\'t work here : Provide Something Else'+'\033[0m')
			open(f'{org_filepath}{file_name}.cry','wb').write(b85encode(f.encrypt(file)))
			os.remove(file_path)
			print('\33[32m'+'Encode Sucessful'+'\033[0m')
			print(f'File Path : {org_filepath}{file_name}.cry')
			cl.copy(passw.decode('utf-8'))
			print("Password Copied To Clipboard\n")
		else:
			print('\33[31m'+'File Size Must Be Less Than 50MB'+'\033[0m')
	else:
		pass

def decode():
	file_path = filedialog.askopenfilename()
	if file_path != '' and file_path[-4::] == '.cry':
		print(file_path)
		new_file_path = file_path.split('/')
		file_name = new_file_path[-1]
		new_file_path.pop()
		org_filepath = ''
		for i in new_file_path:
			org_filepath = org_filepath + i + '/'
		try:
			passw = input("Enter password : ").encode('utf-8')
			bs4 = b64encode(passw)
			bs4 = bs4.replace(b'==', b'=')
			if len(bs4) > 44:
				bs4 = bs4[:43]+b'='
			if len(bs4) < 44:
				lenb = 44 - len(bs4)
				for _ in range(lenb):
					bs4 = b'1' + bs4
			file = open(file_path,'rb').read()
			f = Fernet(bs4)
			org = b85decode(file)
			org = f.decrypt(org)
			file_name = file_name.replace('.cry','')
			open(f'{org_filepath}{file_name}', 'wb').write(org)
			os.remove(f'{org_filepath}{file_name}.cry')
			print('\33[32m'+'Decode Sucessful'+'\033[0m')
			print(f'File Path : {org_filepath}{file_name}\n')
		except:
			print('\33[31m'+'Incorrect password\n'+'\033[0m')
	else:
		pass

def menu():
	print("""
███████╗██╗██╗     ███████╗ ██████╗██████╗ ██╗   ██╗██████╗ ████████╗
██╔════╝██║██║     ██╔════╝██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝
█████╗  ██║██║     █████╗  ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   
██╔══╝  ██║██║     ██╔══╝  ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   
██║     ██║███████╗███████╗╚██████╗██║  ██║   ██║   ██║        ██║   
╚═╝     ╚═╝╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝   
		""")
	print('[+] Encode')
	print('[+] Decode')
	print('[+] Clear')
	print('[+] Exit\n')
	screen = True
	while screen:
		a = ''
		while a == '':
			a = input('\33[32m' + "root:-$ " + '\033[0m')
		a = a.lower().strip()
		if a == 'encode' or a == 'decode' or a == 'exit' or a == 'clear':
			if a == 'clear':
				os.system('cls')
			if a == 'exit':
				screen = False
			if a == 'encode':
				encode()
			if a == 'decode':
				decode()
		else:
			print('\33[31m' + f"Command not found : {a}" + '\033[0m')

if __name__ == '__main__':
	menu()