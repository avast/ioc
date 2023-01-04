
'usage: cscript test.vbs
' make sure you are running exe and script at same permission level
'32/64 bit cmd prompt doesnt matter. 

'If you just double click on the file it will run in wscript and 
'the echo will be a msgbox vrs console print (still works but)

Set o = GetObject("remote.forms")

Set f = o.Item(0)
f.List1.Clear()

For Each form In o
	f.List1.AddItem  "Form: " & form.Name
	For Each c In form.Controls
		f.List1.AddItem  vbTab & "Control: " & c.Name & " - " & TypeName(c)
	Next
Next

WScript.echo Hex(f.formMeth("remote hi"))  
WScript.echo Hex(f.pubClass.classMeth("remote class hi")) 
WScript.echo  f.pubClass.pubString  
f.text1.Text = "I see you"
f.text1.Font.Name = "System"
if f.width < 8000 then f.width = 8000 else f.width = 4000
f.List1.AddItem "hi from script"
