
#include <windows.h>
#include <stdio.h>
#include <conio.h>

#include "vb.h"     //structures
#include "pcode.h"

int lpProcCallEngine = 0;

//examples progress callback (same vb declare as sleep)
void __stdcall callback(int arg){
	printf("%d\n",arg);
}

void __stdcall strCallBack(char* arg){
	printf("string callback: %s\n",arg);
}

bool FileExists(LPCTSTR szPath)
{
  DWORD dwAttrib = GetFileAttributes(szPath);
  bool rv = (dwAttrib != INVALID_FILE_ATTRIBUTES && !(dwAttrib & FILE_ATTRIBUTE_DIRECTORY)) ? true : false;
  return rv;
}

int file_length(FILE *f)
{
	int pos;
	int end;

	pos = ftell (f);
	fseek (f, 0, SEEK_END);
	end = ftell (f);
	fseek (f, pos, SEEK_SET);

	return end;
}

SAFEARRAY* loadData(void){

	FILE *fp;
	char* dat = "lorem_ipsum.txt";
	//dat = "1mb_lorem_ipsum.bin";

	if(!FileExists(dat)){
		printf("%s not found\nPress any key to exit...", dat);
		getch();
		exit(0);
	}
	
	fp = fopen(dat, "rb");
	if(fp==0){
		printf("%s not found\nPress any key to exit...", dat);
		getch();
		exit(0);
	}

	int size = file_length(fp);
	SAFEARRAY* sa = SafeArrayCreateVector(VT_UI1, 0, size);

	if(sa==0){
		printf("Could not create safearray sz:%x\nPress any key to exit...", size);
		getch();
		exit(0);
	}

	fread(sa->pvData , 1, size, fp);
	fclose(fp);

	return sa;
}


void main(void){

	int rv = 0, i=0;
	int abort = 0; 
	int constPool[20] = {0}; //no const pool needed for the rc4
	int lpProjObj[10] = {0};
	
	objInfo.aObject = (int)&codeObj;
	objInfo.lpConstantPool = (int)&constPool;
	objInfo.aObjectTable = (int)&objtable;
	objtable.lpProjectObject = (int)&lpProjObj;

	HMODULE hRuntime = (HMODULE)LoadLibrary("msvbvm60.dll");
	lpProcCallEngine = (int)GetProcAddress(hRuntime,"ProcCallEngine");
	CreateIExprSrvObj IExprSrvObj = (CreateIExprSrvObj)GetProcAddress(hRuntime,"CreateIExprSrvObj"); 

	IExprSrvObj(0,4,0); //initilize runtime enough for most things to work (COM, native pcode handlers etc)

	// rc4  - 504 bytes
	int offset_rc4 = (int)&rc4 + 0x198;
	(*(int*)offset_rc4) = (int)&objInfo;

	char* pass = "secret";
	SAFEARRAY* data = loadData();
	SAFEARRAY* key =  SafeArrayCreateVector(VT_UI1, 0, strlen(pass));
	memcpy(key->pvData, pass, strlen(pass));

	unsigned char* d = (unsigned char*)data->pvData;
    printf("start %c%c%c%c%c\n", d[0], d[1], d[2], d[3], d[4]);

	//Public Sub rc4(b() As Byte, key() As Byte)  - data encrypted in place..
	
	unsigned int startTime = GetTickCount();

	for(i = 0; i < 10; i++){
		_asm{
			//int 3
			lea eax, key
			push eax
			lea eax, data
			push eax
			mov edx, offset_rc4
			mov ecx, lpProcCallEngine
			call ecx
		}

		printf("%2d)    %c%c%c%c%c\n", i, d[0], d[1], d[2], d[3], d[4]);
	}

	unsigned int elapsed = GetTickCount() - startTime;
	printf("We ran 504 byte pcode rc4 12 times on 100kb of data/cycle: elapsedTime: %d milliSeconds\n", elapsed);
	printf("Press any key to exit...");
	getch();

}


