
// make sure you are running exe and script at same permission level

var o = GetObject("remote.forms")
var f = o.Item(0)

f.List1.Clear()
WScript.Echo( f.text1.text)
f.text1.text = "test from js"
f.List1.AddItem("test list item",0)
f.caption = "yup it works"
WScript.echo(f.formMeth("remote hi").toString(16))
WScript.echo(f.pubClass.classMeth("remote class hi").toString(16)) 

for(i=0; i< f.controls.count; i++){
   f.List1.AddItem('Control ' + i + ' = ' + f.controls(i).name)
}