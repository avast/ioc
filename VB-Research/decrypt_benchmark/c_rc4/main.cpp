/*
    robin verton, dec 2015
    implementation of the RC4 algo
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <windows.h>
#include <conio.h>

#define N 256   // 2^8

void swap(unsigned char *a, unsigned char *b) {
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

int KSA(char *key, unsigned char *S) {

    int len = strlen(key);
    int j = 0;

    for(int i = 0; i < N; i++)
        S[i] = i;

    for(int i = 0; i < N; i++) {
        j = (j + S[i] + key[i % len]) % N;

        swap(&S[i], &S[j]);
    }

    return 0;
}

int PRGA(unsigned char *S, char *plaintext, unsigned char *ciphertext) {

    int i = 0;
    int j = 0;

    for(size_t n = 0, len = strlen(plaintext); n < len; n++) {
        i = (i + 1) % N;
        j = (j + S[i]) % N;

        swap(&S[i], &S[j]);
        int rnd = S[(S[i] + S[j]) % N];

        ciphertext[n] = rnd ^ plaintext[n];

    }

    return 0;
}

int RC4(char *key, char *plaintext, unsigned char *ciphertext) {

    unsigned char S[N];
    KSA(key, S);

    PRGA(S, plaintext, ciphertext);

    return 0;
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

int main(int argc, char *argv[]) {

    FILE *fp;
	char* dat = "./../lorem_ipsum.bin";
	dat = "./../1mb_lorem_ipsum.bin";

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
	unsigned char* data = (unsigned char*)malloc(size);
	fread(data , 1, size, fp);
	fclose(fp);

	unsigned int startTime = GetTickCount();
	RC4("secret", (char*)data, data);
    unsigned int elapsed = GetTickCount() - startTime;
	printf("We ran C rc4 on 1mb of data: elapsedTime: %d milliSeconds\n", elapsed);
	printf("Press any key to exit...");
	getch();

    return 0;
}