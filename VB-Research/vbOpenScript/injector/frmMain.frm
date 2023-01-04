VERSION 5.00
Begin VB.Form frmMain 
   Caption         =   "injector"
   ClientHeight    =   7305
   ClientLeft      =   165
   ClientTop       =   450
   ClientWidth     =   8670
   LinkTopic       =   "frmMain"
   ScaleHeight     =   7305
   ScaleWidth      =   8670
   StartUpPosition =   2  'CenterScreen
   Begin VB.ListBox List1 
      BeginProperty Font 
         Name            =   "Courier"
         Size            =   9.75
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   5130
      Left            =   90
      TabIndex        =   14
      Top             =   1935
      Width           =   8295
   End
   Begin VB.TextBox txtIPCHwnd 
      Height          =   330
      Left            =   1215
      TabIndex        =   13
      Top             =   1080
      Width           =   1185
   End
   Begin VB.CommandButton cmdSendIPC 
      Caption         =   "Send Cmd"
      Height          =   285
      Left            =   6210
      TabIndex        =   12
      Top             =   1125
      Width           =   1095
   End
   Begin VB.TextBox txtIPCCmd 
      Height          =   330
      Left            =   2520
      TabIndex        =   11
      Text            =   "my test IPC command"
      Top             =   1080
      Width           =   3615
   End
   Begin VB.CommandButton cmdBrowse 
      Caption         =   "..."
      Height          =   270
      Index           =   2
      Left            =   6240
      TabIndex        =   9
      Top             =   405
      Width           =   615
   End
   Begin VB.CommandButton cmdBrowse 
      Caption         =   "..."
      Height          =   270
      Index           =   1
      Left            =   6240
      TabIndex        =   8
      Top             =   765
      Width           =   615
   End
   Begin VB.CommandButton cmdBrowse 
      Caption         =   "..."
      Height          =   255
      Index           =   0
      Left            =   6255
      TabIndex        =   7
      Top             =   45
      Width           =   615
   End
   Begin VB.TextBox txtArgs 
      Height          =   315
      Left            =   1200
      OLEDropMode     =   1  'Manual
      TabIndex        =   6
      Top             =   360
      Width           =   4965
   End
   Begin VB.TextBox txtDll 
      Height          =   285
      Left            =   1200
      OLEDropMode     =   1  'Manual
      TabIndex        =   4
      Top             =   720
      Width           =   4965
   End
   Begin VB.CommandButton cmdStart 
      Caption         =   "Inject"
      Height          =   300
      Left            =   7065
      TabIndex        =   2
      Top             =   45
      Width           =   1335
   End
   Begin VB.TextBox txtExe 
      Height          =   315
      Left            =   1200
      OLEDropMode     =   1  'Manual
      TabIndex        =   1
      Top             =   0
      Width           =   4920
   End
   Begin VB.Label Label3 
      Caption         =   "Log Output"
      Height          =   285
      Left            =   90
      TabIndex        =   15
      Top             =   1530
      Width           =   915
   End
   Begin VB.Label Label2 
      Caption         =   "IPC hWnd"
      Height          =   240
      Left            =   0
      TabIndex        =   10
      Top             =   1125
      Width           =   1095
   End
   Begin VB.Label Label7 
      Caption         =   "Args"
      Height          =   285
      Left            =   60
      TabIndex        =   5
      Top             =   360
      Width           =   945
   End
   Begin VB.Label lblDll 
      Caption         =   "Inject DLL"
      ForeColor       =   &H00000000&
      Height          =   315
      Left            =   45
      TabIndex        =   3
      Top             =   750
      Width           =   1335
   End
   Begin VB.Label Label1 
      Caption         =   "Executable"
      Height          =   255
      Left            =   60
      TabIndex        =   0
      Top             =   60
      Width           =   975
   End
End
Attribute VB_Name = "frmMain"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit
'Author: david zimmer <dzzie@yahoo.com>
'Site:   http://sandsprite.com

Dim WithEvents sc As CSubclass2
Attribute sc.VB_VarHelpID = -1

Public fso As New CFileSystem2
Public dlg As New clsCmnDlg
Private runtime As String

Const targetRuntime As Long = &H360C5B48
'Compiled: Sat, Sep 26 1998, 3:11:04
'MD5:      EEBEB73979D0AD3C74B248EBF1B6E770
'SHA256:   E86CBB17C8FCD97BB04D9E0B7FB3EF7A33C6896E681705FC95405F14008737CD

Private Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)
Private Declare Function OpenProcess Lib "kernel32" (ByVal dwDesiredAccess As Long, ByVal bInheritHandle As Long, ByVal dwProcessId As Long) As Long
Private Declare Function WriteProcessMemory Lib "kernel32" (ByVal hProcess As Long, lpBaseAddress As Long, lpBuffer As Any, ByVal nSize As Long, lpNumberOfBytesWritten As Long) As Long
Private Declare Function CreateRemoteThread Lib "kernel32" (ByVal ProcessHandle As Long, lpThreadAttributes As Long, ByVal dwStackSize As Long, ByVal lpStartAddress As Any, ByVal lpParameter As Any, ByVal dwCreationFlags As Long, lpThreadID As Long) As Long
Private Declare Function GetModuleHandle Lib "kernel32" Alias "GetModuleHandleA" (ByVal lpModuleName As String) As Long
Private Declare Function GetProcAddress Lib "kernel32" (ByVal hModule As Long, ByVal lpProcName As String) As Long
Private Declare Function VirtualAllocEx Lib "kernel32" (ByVal hProcess As Long, lpAddress As Any, ByVal dwSize As Long, ByVal fAllocType As Long, FlProtect As Long) As Long
Private Declare Function CreateProcess Lib "kernel32" Alias "CreateProcessA" (ByVal lpApplicationName As Long, ByVal lpCommandLine As String, ByVal lpProcessAttributes As Long, ByVal lpThreadAttributes As Long, ByVal bInheritHandles As Long, ByVal dwCreationFlags As Long, ByVal lpEnvironment As Long, ByVal lpCurrentDriectory As Long, lpStartupInfo As STARTUPINFO, lpProcessInformation As PROCESS_INFORMATION) As Long
Private Declare Function ResumeThread Lib "kernel32" (ByVal hThread As Long) As Long
Private Declare Sub DebugBreak Lib "kernel32" ()
Private Declare Function CloseHandle Lib "kernel32" (ByVal hObject As Long) As Long
Private Declare Sub CopyMemory Lib "kernel32" Alias "RtlMoveMemory" (hpvDest As Any, hpvSource As Any, ByVal cbCopy As Long)
Private Declare Function WriteProcessBytes Lib "kernel32" Alias "WriteProcessMemory" (ByVal hProcess As Long, lpBaseAddress As Long, lpBuffer As Any, ByVal nSize As Long, lpNumberOfBytesWritten As Long) As Long
Private Declare Function SendMessage Lib "user32" Alias "SendMessageA" (ByVal hwnd As Long, ByVal wMsg As Long, ByVal wParam As Long, lParam As Any) As Long
Private Declare Function IsWindow Lib "user32" (ByVal hwnd As Long) As Long
'Private Declare Sub CopyMemory Lib "kernel32" Alias "RtlMoveMemory" (hpvDest As Any, hpvSource As Any, ByVal cbCopy As Long)

Private Const WM_COPYDATA = &H4A
Private Const PAGE_READWRITE = 4
Private Const CREATE_SUSPENDED = &H4
Private Const MEM_COMMIT = &H1000

Private Const STANDARD_RIGHTS_REQUIRED = &HF0000
Private Const SYNCHRONIZE = &H100000
Private Const PROCESS_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED Or SYNCHRONIZE Or &HFFF)
 
Private Type COPYDATASTRUCT
    dwFlag As Long
    cbSize As Long
    lpData As Long
End Type

Private Type PROCESS_INFORMATION
   hProcess As Long
   hThread As Long
   dwProcessId As Long
   dwThreadId As Long
End Type

Private Type STARTUPINFO
        cb As Long
        lpReserved As String
        lpDesktop As String
        lpTitle As String
        dwX As Long
        dwY As Long
        dwXSize As Long
        dwYSize As Long
        dwXCountChars As Long
        dwYCountChars As Long
        dwFillAttribute As Long
        dwFlags As Long
        wShowWindow As Integer
        cbReserved2 As Integer
        lpReserved2 As Long
        hStdInput As Long
        hStdOutput As Long
        hStdError As Long
End Type



Private Sub cmdBrowse_Click(index As Integer)
    Dim f As String
    
    f = dlg.OpenDialog(AllFiles, , "Open Executable", Me.hwnd)
    f = Trim(Replace(f, Chr(0), Empty))
    If Len(f) = 0 Then Exit Sub
    
    Select Case index
        Case 0: txtExe = f
        Case 1: txtDll = f
        Case 2: txtArgs = f
    End Select
    
End Sub

Private Sub cmdSendIPC_Click()
    On Error Resume Next
    Dim hwnd As Long
    
    txtIPCCmd = Trim(txtIPCCmd)
    
    If Len(txtIPCCmd) = 0 Then
        MsgBox "Nothing to send", vbInformation
        Exit Sub
    End If
    
    hwnd = Replace(txtIPCHwnd, "0x", "&h", , , vbTextCompare)
    
    If Err.Number <> 0 Then
        MsgBox "hwnd not numeric? " & Err.Description, vbExclamation
        Exit Sub
    End If
    
    If IsWindow(hwnd) <> 1 Then
         MsgBox "hwnd not a valid window ", vbExclamation
        Exit Sub
    End If
    
    SendIPC hwnd, txtIPCCmd, Me.hwnd
    
End Sub

Private Sub cmdStart_Click()
        
    Dim exe As String
    Dim pf As String
    Dim ver As Long
    Dim tmp As String
    
    On Error GoTo hell
    
    List1.Clear

    If Not fso.FileExists(txtExe) Then
        List1.AddItem "Executable not found"
        Exit Sub
    End If

    If Not fso.FileExists(txtDll) Then
        List1.AddItem "Dll To inject not found"
        Exit Sub
    End If
    
    If Not fso.FileExists(runtime) Then
        List1.AddItem "Could not find a copy of our target runtime in my folder?"
        Exit Sub
    Else
        pf = fso.GetParentFolder(txtExe) & "\"
        tmp = pf & "msvbvm60.dll"
        If Not fso.FileExists(tmp) Then
            fso.Copy runtime, pf
            If Not fso.FileExists(tmp) Then
                List1.AddItem "Could not copy target runtime to exe folder"
                Exit Sub
            Else
                List1.AddItem "Target runtime copied to exe folder"
            End If
        Else
            'a copy of runtime is already in exe folder, is it ours?
            ver = GetCompileTime(tmp, True)
            List1.AddItem "Runtime timestamp: " & Hex(ver) & " - " & GetCompileTime(tmp)
            If ver <> targetRuntime Then
                List1.AddItem "VB runtime in exe folder does not match our target version."
                Exit Sub
            End If
        End If
    End If
        
    exe = txtExe

    If Len(txtArgs) > 0 Then exe = exe & " " & txtArgs
    
    If StartWithDLL(exe, txtDll) = 0 Then
        List1.AddItem "Injection failed"
    End If
    
    Exit Sub
hell:
    MsgBox "Error: " & Err.Description
    
End Sub

 
Private Sub Form_Load()

    Set sc = New CSubclass2
    
    sc.AttachMessage Me.hwnd, WM_COPYDATA

    txtDll = App.path & IIf(isIde(), "\..\", "\") & "openscript.dll"
    runtime = App.path & IIf(isIde(), "\..\", "\") & "msvbvm60.dll"
    
    If Not fso.FileExists(runtime) Then
        List1.AddItem "Could not locate target version of the runtime"
        runtime = Empty
    Else
        Dim ver As Long
        ver = GetCompileTime(runtime, True)
        If ver <> targetRuntime Then
            List1.AddItem "Target Runtime version mismatch? Time stamp is: " & GetCompileTime(runtime)
            runtime = Empty
        End If
    End If
    
    If Len(Command) > 0 Then
        txtExe = Replace(Command, """", Empty)
    Else
        txtExe = App.path & IIf(isIde(), "\..\", "\") & "testApp.exe"
    End If

End Sub

Private Sub Form_Unload(Cancel As Integer)
    Set sc = Nothing
End Sub

Private Sub sc_MessageReceived(hwnd As Long, wMsg As Long, wParam As Long, lParam As Long, Cancel As Boolean) '
    
    Dim CopyData As COPYDATASTRUCT
    Dim Buffer(1 To 2048) As Byte
    Dim temp As String, a As Long
    
    On Error Resume Next
    
    If wMsg = WM_COPYDATA Then

       CopyMemory CopyData, ByVal lParam, Len(CopyData)
       
       If CopyData.dwFlag = 3 Then
           CopyMemory Buffer(1), ByVal CopyData.lpData, CopyData.cbSize
           temp = StrConv(Buffer, vbUnicode, &H409)
           temp = Left$(temp, InStr(1, temp, Chr$(0)) - 1)
           temp = Trim(temp)
           If Len(temp) > 0 Then List1.AddItem temp
           If InStr(1, temp, "IPC listening on hwnd", vbTextCompare) > 0 Then
                a = InStrRev(temp, " ")
                If a > 0 Then txtIPCHwnd = "0x" & Trim(Mid(temp, a))
           End If
       End If
    
    End If
    
End Sub

Private Sub txtArgs_OLEDragDrop(data As DataObject, Effect As Long, Button As Integer, Shift As Integer, x As Single, y As Single)
    On Error Resume Next
    txtArgs = data.files(1)
End Sub

Private Sub txtDll_OLEDragDrop(data As DataObject, Effect As Long, Button As Integer, Shift As Integer, x As Single, y As Single)
    On Error Resume Next
    txtDll = data.files(1)
End Sub

Private Sub txtexe_OLEDragDrop(data As DataObject, Effect As Long, Button As Integer, Shift As Integer, x As Single, y As Single)
    On Error Resume Next
    txtExe = data.files(1)
End Sub

Private Sub Form_Resize()
    On Error Resume Next
    List1.Width = Me.Width - List1.Left - 200
    List1.Height = Me.Height - List1.Top - 500
End Sub

Function isIde() As Boolean
    On Error GoTo hell
    Debug.Print 1 \ 0
Exit Function
hell: isIde = True
End Function

Function GetCompileTime(Optional ByVal exe As String, Optional returnRawVal As Boolean = False)
    
    Dim f As Long, i As Integer
    Dim stamp As Long, e_lfanew As Long
    Dim base As Date, compiled As Date

    On Error GoTo errExit
    
    If Len(exe) = 0 Then
        exe = App.path & "" & App.EXEName & ".exe"
    End If
    
    FileLen exe 'throw error if not exist
    
    f = FreeFile
    Open exe For Binary Access Read As f
    Get f, , i
    
    If i <> &H5A4D Then GoTo errExit 'MZ check
     
    Get f, 60 + 1, e_lfanew
    Get f, e_lfanew + 1, i
    
    If i <> &H4550 Then GoTo errExit 'PE check
    
    Get f, e_lfanew + 9, stamp
    Close f
    
    If returnRawVal Then
        GetCompileTime = stamp
    Else
        base = DateSerial(1970, 1, 1)
        compiled = DateAdd("s", stamp, base)
        GetCompileTime = Format(compiled, "ddd, mmm d yyyy, h:nn:ss ")
    End If
    
    Exit Function
errExit:
    Close f
        
End Function



Function SendIPC(targetHwnd As Long, msg As String, Optional senderHwnd As Long = 0) As Long

    Dim cds As COPYDATASTRUCT
    Dim buf(1 To 255) As Byte
    
    List1.AddItem "SendIPC(hwnd=" & targetHwnd & ", msg=" & msg & ")"
    
    Call CopyMemory(buf(1), ByVal msg, Len(msg))
    cds.dwFlag = 3
    cds.cbSize = Len(msg) + 1
    cds.lpData = VarPtr(buf(1))
    SendIPC = SendMessage(targetHwnd, WM_COPYDATA, senderHwnd, cds)
     
End Function

Public Function StartWithDLL(exe As String, dll As String) As Long

    Dim hProcess As Long, hThread As Long, remoteLoadLib As Long, remoteMem As Long, bufLen As Long, writeLen As Long
    Dim pi As PROCESS_INFORMATION, si As STARTUPINFO, buf() As Byte
     
    buf() = StrConv(dll & Chr(0), vbFromUnicode)
    bufLen = UBound(buf) + 1

    If CreateProcess(0&, exe, 0&, 0&, 1&, CREATE_SUSPENDED, 0&, 0&, si, pi) = 0 Then Exit Function
    List1.AddItem "PID: 0x" & Hex(pi.dwProcessId) & " (" & pi.dwProcessId & ")"

    hProcess = OpenProcess(PROCESS_ALL_ACCESS, False, pi.dwProcessId)
    If hProcess = -1 Then Exit Function
    
    remoteMem = VirtualAllocEx(hProcess, ByVal 0, bufLen, MEM_COMMIT, ByVal PAGE_READWRITE)
    If remoteMem <> 0 Then
       If WriteProcessBytes(hProcess, ByVal remoteMem, buf(0), bufLen, writeLen) <> 0 Then
            remoteLoadLib = GetProcAddress(GetModuleHandle("kernel32.dll"), "LoadLibraryA")
            If CreateRemoteThread(hProcess, ByVal 0, 0, remoteLoadLib, remoteMem, 0, hThread) <> -1 Then
                List1.AddItem "ThreadID: 0x" & Hex(hThread)
                Sleep 300
                If ResumeThread(pi.hThread) <> -1 Then StartWithDLL = 1
            End If
        End If
    End If
             
    CloseHandle hProcess
    
End Function
