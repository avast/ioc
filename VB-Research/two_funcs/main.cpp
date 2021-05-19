
#include <windows.h>
#include <stdio.h>
#include <conio.h>

/*

Private Sub Main()
    two
End Sub

Function two() As Date
    DoEvents
End Function

4014C8 Module1.Sub Main:
4014C8    0A 00000000           ImpAdCallFPR4 Module1.Proc_401490
4014CD    74 74FF               FStFPR8 var_8C
4014D0    14                    ExitProcI4 
Last Offset: 4014D4

401490 Module1.Proc_401490:
401490    0A 01000000           ImpAdCallFPR4 rtcDoEvents
401495    17                    ExitProcR8 
Last Offset: 401498

Const Pool
0	4010DC	ExtApi	Module1.Proc_401490	
1	401020	ExtApi	rtcDoEvents	

 */ 

unsigned char SubMain[62] = {
	0x0A, 0x00, 0x00, 0x00, 0x00, 0x74, 0x74, 0xFF, 0x14, 0x00, 0x00, 0x00, 0x88, 0x10, 0x40, 0x00, 
	0x04, 0x00, 0x08, 0x00, 0x0C, 0x00, 0x24, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x19, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xCC, 0xCC
};

unsigned char two[56] = {
	0x0A, 0x01, 0x00, 0x00, 0x00, 0x17, 0x00, 0x00, 0x88, 0x10, 0x40, 0x00, 0x04, 0x00, 0x08, 0x00, 
	0x08, 0x00, 0x24, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x19, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
};

struct ObjectTable{
    int lNull1;	            // As Long      ' 0x00 (00d)
    int aExecProj;			// As Long      ' 0x04 (04d) Pointer to a memory structure
    int aProjectInfo2;		// As Long      ' 0x08 (08d) Pointer to Project Info 2
    int Const1;				// As Long      ' 0x0C
    int  Null2;				// As Long      ' 0x10
    int lpProjectObject;	// As Long      ' 0x14
    char uuidObj[15];		// As Byte      'converted from 4 flags dzzie (from vb.idc)
    short fCompileType;		// As Integer   ' 0x28 (40d) Internal flag used during compilation
    short ObjectCount1;		// As Integer   ' 0x2A
    short iCompiledObjects; // As Integer   ' 0x2C (44d) Number of objects compiled.
    short iObjectsInUse;	// As Integer   ' 0x2E (46d) Updated in the IDE to correspond the total number ' but will go up or down when initializing/unloading modules.
    int lpObjectArray;		// As Long      ' 0x30
    int fIdeFlag;			// As Long      ' 0x34
    int lpIdeData;			// As Long      ' 0x38
    int lpIdeData2;			// As Long      ' 0x3C
    int aProjectName;		// As Long      ' 0x40      NTS
    int LangID1;			//  As Long     ' 0x44
    int LangID2;			//  As Long     ' 0x48
    int lpIdeData3;			//  As Long     ' 0x4C
    int dwIdentifier;	    //  As Long     ' 0x50
};



struct CodeObject{
    int aObjectInfo;	//	As Long         ' 0x00  Pointer to the Object Info for this Object.
    int Const1;		    //	As Long         ' 0x04  Always set to -1 after compiling.
    int aPublicBytes;	//	As Long         ' 0x08  Pointer to Public Variable Size integers
    int aStaticBytes;	//	As Long         ' 0x0C  Pointer to Static Variables Struct
    int aModulePublic;	//	As Long         ' 0x10  Pointer to Public Variables in DATA section
    int aModuleStatic;	//	As Long         ' 0x14  Pointer to Static Variables in DATA section
    int aObjectName;	//	As Long         ' 0x18  Name of the Object.
    int ProcCount;		//  As Long         ' 0x1C  Number of Methods in Object
    int aProcNamesArray;//	As Long         ' 0x20  If present, pointer to Method names array.
    int oStaticVars;	//	As Long         ' 0x24  Offset to Static Vars from aModuleStatic
    int ObjectType;		//  As Long         ' 0x28  Flags defining the Object Type.
    int Null3;		    //  As Long         ' 0x2C  Not valid after compilation.
};

struct ObjectInfo{
    short wRefCount;		// 0 As Integer          ' Always 1 after compilation.
	short ObjectIndex;		// 2 As Integer          '
    int aObjectTable;		// 4 As Long             ' Pointer to the Object Table
    int lpIdeData;			// 8 Long                ' Zero after compilation. Used in IDE only.
    int lpPrivateObject;	// 0xC As Long        ' Pointer to Private Object Descriptor.
    int dwReserved;			// 0x10 As Long
    int Null2;				// 0x14 As Long
    int aObject;			// 0x18 As Long       ' points to the parent tObject
    int lpProjectData;		// 0x1c As Long       ' 0x1C [can someone verify this?]
    short NumberOfProcs;	// 0x20 As Integer
    short wMethodCount2;	// 0x22 As Integer    ' Zeroed out after compilation. IDE only.
    int lpMethods;			// 0x24 As Long       ' Pointer to Array of Methods.
    short iConstantsCount;  // 0x28 As Integer    ' Number of Constants
    short iMaxConstants;    // 0x2A As Integer    ' Maximum Constants to allocate.
    int lpIdeData2;			// 0x2C As Long
    int lpIdeData3;			// 0x30 As Long
    int lpConstantPool;		// 0x34 As Long       'can be immediatly followed by OptionalObjectInfo
};

int lpProcCallEngine = 0;
int rtcDoEvents = 0;
int twoLastOffset = 0;

void __declspec(naked) stubCall_two(){
	_asm{
		mov     edx, twoLastOffset
		mov     ecx, lpProcCallEngine
		jmp     ecx
	}
}

void main(void){

	int rv = 0;
	int constPool[20] = {0};
	int lpProjObj[10] = {0};
	
	ObjectTable objtable = {0};
	CodeObject codeObj = {0};
	ObjectInfo objInfo = {0};
	
	typedef void (__stdcall *CreateIExprSrvObj)(int,int,int);

	HMODULE h = (HMODULE)LoadLibrary("msvbvm60.dll");
	lpProcCallEngine = (int)GetProcAddress(h,"ProcCallEngine");
	rtcDoEvents = (int)GetProcAddress(h,"rtcDoEvents");
	CreateIExprSrvObj IExprSrvObj = (CreateIExprSrvObj)GetProcAddress(h,"CreateIExprSrvObj"); 

	//printf("ProcCallEngine = %x, CreateIExprSrvObj=%x\n", lpProcCallEngine,IExprSrvObj);
	
	twoLastOffset = (int)&two + (0x401498 - 0x401490);
	int mainLastOffset = (int)&SubMain + (0x4014D4 - 0x4014c8); //last offset - funcstart

	constPool[0] = (int)&stubCall_two;
	constPool[1] = rtcDoEvents;

	IExprSrvObj(0,4,0); //initilize runtime just enough to work.. 
	
	//printf("mainLastOffset = %x  first = %x\n",  mainLastOffset, (*(int*)mainLastOffset));

	(*(int*)mainLastOffset) = (int)&objInfo; //patch RTMI of pcode to point to our dynamic ObjInfo Struct
    (*(int*)twoLastOffset) = (int)&objInfo;

	objInfo.aObject = (int)&codeObj;
	objInfo.lpConstantPool = (int)&constPool;
	objInfo.aObjectTable = (int)&objtable;
	objtable.lpProjectObject = (int)&lpProjObj;

	for(int i=0; i<2;i++){

		_asm{
			//int 3
			mov edx, mainLastOffset
			mov ecx, lpProcCallEngine
			call ecx
			mov rv, eax
		}
		

		//this sample does not take any args or return any values
		printf("pcode call complete, calling again..\n");
	}

	printf("Press any key to exit...");
	getch();

}