Attribute VB_Name = "Module1"
Option Explicit

Declare Function callback Lib "dummy" (ByRef b As Byte) As Long
Declare Function progress Lib "dummy" (ByVal b As Byte) As Long
Private Declare Sub CopyMemory Lib "kernel32" Alias "RtlMoveMemory" (pDest As Any, pSrc As Any, ByVal ByteLen As Long)

Sub Main()

End Sub

Function test(ByVal xorKey As Long) As Long
    
    Dim s As String
    Dim b() As Byte
    Dim i As Long
    
    progress xorKey
    'create const pool entry
    'normally this would be a unicode string but we will make it binary
    s = "this is my string"
    progress LenB(s)
    
    ReDim b(LenB(s))

    CopyMemory ByVal VarPtr(b(0)), ByVal StrPtr(s), UBound(b)
    progress 4
    
    For i = 0 To UBound(b)
        b(i) = b(i) Xor xorKey
    Next
    
    callback b(0) 'we should receive decoded C string that we can modify
    test = progress(b(0))  'just to pass back the data to see if modified..
    
End Function
