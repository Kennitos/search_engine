import subprocess
import sys

# import os
# import platform

# pip install modules to avoid "ModuleNotFoundError: No module found named '...'"
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("pandas")
install("elasticsearch")
install("bs4")
install("requests")
install("gitpython")



# maybe pipinstall these modules
# install("platform")


# example_str = "pd.set_option('display.max_rows',20)"

# def create_ref(input_str):
#     start = '#:~:text='
#     end = input_str.replace(' ','%20')
#     output = start+end
#     return output
    

# res = create_ref(example_str)
# print(res)
# t = 205


# print("A total of",total,"repos found. ")

# # input 
# user_input1 = input() 
# print(type(user_input1))

# def valid_check_samplesize(user_input,max_size):
# 	try:
# 		size = int(user_input)
# 		if max_size > size > 0:
# 			print("Downloading sample'size of",size)
# 		else:
# 			print("Choose within the delimiters of 0 and",max_size)
# 			print(),start_cloning(max_size)
# 	except:
# 		print("Type a integer")
# 		print(),start_cloning(max_size)

# def start_cloning(max_size):
# 	print("A total of",max_size,"repositories have been found.")
# 	print("Download all(Y) or use a sample size(N)? Type (Y) to clone all repos or type (N) to choose a sample size or (Q) to quit" )
# 	user_input1 = input()
# 	if user_input1 == "Y" or user_input1 == "y":
# 		print("Are you sure to download all",max_size,"repositories? Type (Y) to confirm")
# 		user_input2 = input()
# 		if user_input2 == "Y" or user_input2 == "y":
# 			print("Downloading all repositories")
# 		else:
# 			print("Type the size of your sample size")
# 			user_input3 = input()
# 			valid_check_samplesize(user_input3,max_size)

# 	elif user_input1 == "N" or user_input1 == "n":
# 		print("Type the size of your sample size")
# 		user_input3 = input()
# 		valid_check_samplesize(user_input3,max_size)

# 	elif user_input1 == "Q" or user_input1 == "q":
# 		return

# 	else:
# 		print("Type a 'y' or 'n'")
# 		print(),start_cloning(max_size)
  
# start_cloning(t)

# # output
# if str_os_sys=="windows":
# 	print(str_os_sys) 
# elif str_os_sys == 'mac':
# 	print(str_os_sys)
# else:
# 	print('Choose a valid os system')
# print("Your operating system:",platform.system())

# def check_os_system():
# 	print("Your operating system:",platform.system())
# 	print("What is your operating system? (type 'windows' or 'mac')")
# 	str_os_sys = str(input()) 
# 	if str_os_sys=="windows":
# 		print(str_os_sys) 
# 	elif str_os_sys == 'mac':
# 		print(str_os_sys)
# 	else:
# 		print('Choose a valid os system')
# 		check_os_system()

# # check_os_system()
# print(os.getcwd())