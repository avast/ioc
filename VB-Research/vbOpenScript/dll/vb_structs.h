
//slightly tweaked structures from vbParser by sysenter-eip

typedef struct {
    DWORD lpObjectInfo; 
    DWORD dwReserved;  
    DWORD lpPublicBytes;  
    DWORD lpStaticBytes;  
    DWORD lpModulePublic;  
    DWORD lpModuleStatic; 
    DWORD lpszObjectName;  
    DWORD dwMethodCount;  
    DWORD lpMethodNames; 
    DWORD bStaticVars;  
    DWORD fObjectType; 
    DWORD dwNull; 
} VBObject;

typedef struct {
    DWORD lpHeapLink;  
    DWORD lpExecProj;  
    DWORD lpProjectInfo2;  
    DWORD dwReserved;  
    DWORD dwNull;  
    DWORD lpProjectObject; 
    UUID uuidObject; 
    WORD fCompileState; 
    WORD dwTotalObjects;  
    WORD dwCompiledObjects; 
    WORD dwObjectsInUse;  
    VBObject *ObjectArray;  
    DWORD fIdeFlag;  
    DWORD lpIdeData;  
    DWORD lpIdeData2;  
    DWORD lpszProjectName;  
    DWORD dwLcid; 
    DWORD dwLcid2; 
    DWORD lpIdeData3;  
    DWORD dwIdentifier;  
} VB_ObjectTable;

typedef struct {
    DWORD dwVersion;  
    VB_ObjectTable *ObjectTable;  
    DWORD dwNull;  
    DWORD lpCodeStart; 
    DWORD lpCodeEnd;  
    DWORD dwDataSize;  
    DWORD lpThreadSpace;  
    DWORD lpVbaSeh;  
    DWORD lpNativeCode;  
    WCHAR wsPrimitivePath[3];  
    WCHAR wsProjectPath[261]; 
    DWORD lpExternalTable; 
    DWORD dwExternalCount; 
} VB_ProjInfo;

typedef struct { 
    CHAR szVbMagic[4]; 
    WORD wRuntimeBuild;  
    CHAR szLangDll[14];  
    CHAR szSecLangDll[14];  
    WORD wRuntimeRevision;  
    DWORD dwLCID;  
    DWORD dwSecLCID; 
    DWORD lpSubMain; 
    VB_ProjInfo *ProjectInfo; 
    DWORD fMdlIntCtls;  
    DWORD fMdlIntCtls2;  
    DWORD dwThreadFlags; 
    DWORD dwThreadCount;  
    WORD wFormCount;  
    WORD wExternalComponentCount;  
    DWORD dwThunkCount;  
    DWORD lpGuiTable; 
    DWORD lpExternalComponentTable;  
    DWORD lpComRegisterData;  
    DWORD bSZProjectDescription;  
    DWORD bSZProjectExeName; 
    DWORD bSZProjectHelpFile;  
    DWORD bSZProjectName;  
} VBHeader; 








