Attribute VB_Name = "Module1"
'this is a sample to test ripping a decoder with variant types from a malware to reuse it from C

Public Declare Sub cb Lib "dummy" (ByVal dwMilliseconds As Long)
Public Declare Sub scb Lib "dummy" (ByVal msg As String)

Sub Main()
    'main is for debugging and so we can breakpoint on the call to rc4 and examine the stack to get an example of
    'the exact args we need to call it from a c host successfully.
    'you could also probably compile to native with debug symbols on and the stack is probably the same..havent verified though
    'in pcode the bp would be ImpAdCallFPR4 opcode A0 i think it was. Look at the disasm in vbrip.
    Dim tmp As String
    tmp = rc4("AAAA", Chr(&H41), True)
    'InputBox "", , Hex(StrPtr(tmp)) 'this is how i extracted the encrypted value from memory...
    scb CStr(rc4(tmp, Chr(&H41), True)) 'replace this with a msgbox if testing in IDE
End Sub

'remember all args are byref by default.
'If type is not specified its a variant.
'if no return value type is specified, its a variant.
Public Function rc4(ByteOrString As Variant, ByVal password As String, strret As Boolean)
On Error Resume Next
    Dim RB(0 To 255) As Integer, X As Long, Y As Long, Z As Long, key() As Byte, temp As Byte
    Dim byteArray() As Byte
    
    Dim plen As Long
    Const LANG_US = &H409
    
    If TypeName(ByteOrString) = "Byte()" Then
        byteArray() = ByteOrString
        cb 1
    ElseIf TypeName(ByteOrString) = "String" Then
        byteArray() = StrConv(ByteOrString, vbFromUnicode, LANG_US)
        cb 2
    Else
        cb -1
        Exit Function
    End If
    
    If TypeName(password) = "Byte()" Then
        key() = password
        If UBound(key) > 255 Then ReDim Preserve key(255)
        cb 3
    Else
        If Len(password) = 0 Then
            cb -2
            Exit Function
        End If

        If Len(password) > 256 Then
            key() = StrConv(Left$(CStr(password), 256), vbFromUnicode, LANG_US)
        Else
            key() = StrConv(CStr(password), vbFromUnicode, LANG_US)
        End If
        cb 4
    End If
    
    plen = UBound(key) + 1
    cb 6
    
    'Debug.Print "key=" & HexDump(Key)
    'Debug.Print "data=" & HexDump(ByteArray)
    
    For X = 0 To 255
        RB(X) = X
    Next X
    
    X = 0
    Y = 0
    Z = 0
    For X = 0 To 255
        Y = (Y + RB(X) + key(X Mod plen)) Mod 256
        temp = RB(X)
        RB(X) = RB(Y)
        RB(Y) = temp
    Next X
    
    X = 0
    Y = 0
    Z = 0
    For X = 0 To UBound(byteArray)
        Y = (Y + 1) Mod 256
        Z = (Z + RB(Y)) Mod 256
        temp = RB(Y)
        RB(Y) = RB(Z)
        RB(Z) = temp
        byteArray(X) = byteArray(X) Xor (RB((RB(Y) + RB(Z)) Mod 256))
    Next X
    
    If strret Then
        cb 7
        rc4 = StrConv(byteArray, vbUnicode, LANG_US)
    Else
        cb 8
        rc4 = byteArray
   End If
    
End Function
