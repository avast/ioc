VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "Class1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Public pubString As String

Public Function classMeth(x) As Long
    Form1.List1.AddItem "Class1.classMeth received: " & x
    classMeth = &H44556677
End Function

Private Sub Class_Initialize()
    pubString = "my public class string"
End Sub
