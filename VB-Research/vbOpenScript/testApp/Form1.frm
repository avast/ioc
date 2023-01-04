VERSION 5.00
Begin VB.Form Form1 
   Caption         =   "Sample App"
   ClientHeight    =   3015
   ClientLeft      =   60
   ClientTop       =   405
   ClientWidth     =   3165
   LinkTopic       =   "Form1"
   ScaleHeight     =   3015
   ScaleWidth      =   3165
   StartUpPosition =   3  'Windows Default
   Begin VB.ListBox List1 
      Height          =   2400
      Left            =   135
      TabIndex        =   1
      Top             =   495
      Width           =   2850
   End
   Begin VB.TextBox Text1 
      Height          =   285
      Left            =   135
      TabIndex        =   0
      Text            =   "Text1"
      Top             =   90
      Width           =   2850
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

Private Declare Function GetCurrentThreadId Lib "kernel32" () As Long

Public pubClass As New Class1

Public Function formMeth(x) As Long
    List1.AddItem "form1.formMeth received: " & x
    formMeth = &H11223344
End Function
    
Private Sub Form_Load()
    List1.AddItem "VB.Forms: " & Hex(ObjPtr(VB.Forms))
    List1.AddItem "ThreadID: " & Hex(GetCurrentThreadId())
    If Len(Command) > 0 Then List1.AddItem "CmdLine: " & Command
End Sub
