import os, sys
import win32com.client 

# tested w/ 32bit python 2.7  
# If you do not have the win32com module run 'pip install pywin32'
# make sure you are running exe and script at same permission level

os.system("cls")

forms = win32com.client.GetObject("remote.forms")

for form in forms:
	print form.Name
	for c in form.Controls:
		print "    " + c.Name 

f = forms(0)
print "Text1 = " + f.text1.text
print hex(f.formMeth("remote hi"))  
print hex(f.pubClass.classMeth("remote class hi")) 
print f.pubClass.pubString  
f.text1.Text = "I see you"

if f.width < 8000:
    f.width = 8000
else:
    f.width = 4000
    
