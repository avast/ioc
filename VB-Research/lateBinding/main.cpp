
#include <windows.h>
#include <stdio.h>
#include <conio.h>

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


int __stdcall MsgBox(wchar_t *str)
{
	if(str == NULL || *str == NULL) return 0;
	return MessageBoxW(0, str, L"In C",0);
}


unsigned char pcode[] = {
	0xF5, 0x00, 0x00, 0x00, 0x00, 0x1B, 0x00, 0x00, 0x04, 0x68, 0xFF, 0x0A, 0x01, 0x00, 0x0C, 0x00, 
	0x04, 0x68, 0xFF, 0xFC, 0x34, 0xFC, 0xF8, 0x78, 0xFF, 0x35, 0x68, 0xFF, 0x3A, 0x58, 0xFF, 0x02, 
	0x00, 0x25, 0x08, 0x78, 0xFF, 0xFE, 0x98, 0x03, 0x00, 0x01, 0x00, 0x14, 0x88, 0x10, 0x40, 0x00, 
	0x04, 0x00, 0x34, 0x00, 0x2C, 0x00, 0x28, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x19, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x78, 0xFF, 0x03, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x68, 0xFF, 0x02, 0x00, 0xCC, 0xCC, 0xCC, 0xCC, 0xE9, 0xE9, 0xE9, 0xE9, 0xCC, 0xCC, 0xCC, 0xCC, 
	0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0x9E, 0x9E, 0x9E, 0x9E, 0x8C, 0x15, 0x00, 0x00, 
	0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xA0, 0x15, 0x00, 0x00
};

struct COMDEF{
	int unk;
	void* lpData1;
	void* lpData2;
	int unk2;
};

void main(void){

	int rv = 0;
	void* constPool[20] = {0};
	int lpProjObj[10] = {0};
	
	ObjectTable objtable = {0};
	CodeObject codeObj = {0};
	ObjectInfo objInfo = {0};
	
	typedef IUnknown* (__stdcall *CreateIExprSrvObj)(int,int,int);

	HMODULE h = (HMODULE)LoadLibrary("msvbvm60.dll");
	int lpProcCallEngine = (int)GetProcAddress(h,"ProcCallEngine");
	CreateIExprSrvObj IExprSrvObj = (CreateIExprSrvObj)GetProcAddress(h,"CreateIExprSrvObj"); 

	//printf("ProcCallEngine = %x, CreateIExprSrvObj=%x\n", lpProcCallEngine,IExprSrvObj);

	IUnknown *iunk = IExprSrvObj(0,4,0); //initilize runtime 
	
	int mainLastOffset = (int)&pcode + (0x2c); //last offset - funcstart
	(*(int*)mainLastOffset) = (int)&objInfo; //patch lastOffset of pcode to point to our dynamic ObjInfo Struct

	objInfo.aObject = (int)&codeObj;
	objInfo.lpConstantPool = (int)&constPool;
	objInfo.aObjectTable = (int)&objtable;
	objtable.lpProjectObject = (int)&lpProjObj; //ENGINE:66104EAB   [ebp-2Ch] = ObjTable.lpProjectObject[0x0C]; (heap memory) unknown

	BSTR b0 = SysAllocString(L"SAPI.SpVoice");
	BSTR b2 = SysAllocString(L"Late binding is cool");
	BSTR b3 = SysAllocString(L"Speak");

	constPool[0x0] = b0;
	constPool[0x1] = GetProcAddress(h,"rtcCreateObject2");
	constPool[0x2] = b2;
	constPool[0x3] = b3;

	HRESULT hh = CoInitialize(NULL);
	printf("Launching pcode CoInitialize = %x\n", hh); 

	_asm{
		//int 3
		mov edx, mainLastOffset
        mov ecx, lpProcCallEngine
		call ecx
	}

	if(iunk!=NULL) iunk->Release(); //doesnt really matter...

	printf("Press any key to exit...");
	getch();

}