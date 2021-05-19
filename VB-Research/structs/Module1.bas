Attribute VB_Name = "Module1"
Option Explicit

Declare Function mMsgBox Lib "dummy" (ByVal msgPtr As Long) As Long

Type cfg
    str1 As String
    int1 As Long
End Type

Sub Main()

End Sub

Function test(ByRef c As cfg) As Long
    
    mMsgBox StrPtr(Hex(VarPtr(c)))
    mMsgBox StrPtr("c.int1 = 0x" & Hex(c.int1))
    mMsgBox StrPtr(c.str1)
    
    Dim tmp As String
    tmp = "will i get a crash? " & c.str1
    mMsgBox StrPtr(tmp)
    
End Function
