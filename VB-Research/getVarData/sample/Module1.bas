Attribute VB_Name = "Module1"
'lets have our loader feed us some different data based on a key we pass in including a byte array

Public Declare Function getData Lib "dummy" (ByVal key As Long) As Variant
Public Declare Sub mMsgBox Lib "dummy" (ByVal msg As String)

Dim maxCount As Long 'set from host language..yes we are fancy and in complete control.

Sub Main()

    Dim i As Long
    
    For i = 0 To maxCount
        getDataTest i
    Next
    
End Sub


Function getDataTest(key As Long) As Variant
    
    Dim v As Variant, t As String, msg As String, b() As Byte
    
    v = getData(key)
    t = TypeName(v)
    msg = "TypeName(v) = " & t
    mMsgBox key & " " & msg
    
    If t = "Byte()" Then
        b() = v
        mMsgBox "Ubound: " & UBound(b)
        msg = "Value = " & StrConv(b, vbUnicode, &H409)
    Else
        msg = "Value = " & v
    End If
    
    mMsgBox msg
    
End Function
