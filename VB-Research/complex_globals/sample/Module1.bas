Attribute VB_Name = "Module1"
Option Explicit

Dim g As Long
Dim v As Variant
Dim b() As Byte
Dim bool As Boolean
Dim s As Integer

Private Declare Sub strCallback Lib "dummy.dll" (ByVal s As String)

Sub Main()
    strCallback "g = " & Hex(g)
    strCallback "ubound(b) = " & UBound(b)
    strCallback "bool = " & Hex(bool)
    strCallback "s = " & Hex(s)
    strCallback "typename(v) = " & TypeName(v)
End Sub


