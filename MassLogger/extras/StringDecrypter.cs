internal static string StringDecrypter(int \u0020) 
{
    Dictionary<int, int> dictionary = new Dictionary<int, int>();
    BinaryReader binaryReader = new BinaryReader(Type.GetTypeFromHandle(YMn.TLiQPA(33554549)).Assembly.GetManifestResourceStream("6FF2DEHA59scuaOblI.3yVNoPUENeqkvGg9UY"));
    binaryReader.BaseStream.Position = 0L;
    byte[] cipherText = binaryReader.ReadBytes((int)binaryReader.BaseStream.Length);
    total_interations = cipherText.length / 4;
    num15 = 0;
    binaryReader.Close();
    //First run, string has not been decrypted
    if (massCrypto.IsInitialized()) {
        array7 = [0x74, 0x52, 0x47, 0x4A, 0x15, 0xD4, 0x9F, 0x2E, 0x31, 0x49, 0x7D, 0xD9, 0xC5, 0x0C, 0x33,
              0xB1, 0x09, 0x8D, 0xC8, 0xB3, 0xEA, 0x41, 0x8B, 0x7D, 0xDC, 0x21, 0xA9, 0x1E, 0x71, 0x97, 0x47, 0x7D];

        
        while (num_interations != total_interations -1) {
            num38 = num_interations % 0x08
            num4 = num_interations * 4; // num4 = reading offset
            num13 = (uint)(num38 * 4);
            num14 = (uint)((int)array7[(int)((UIntPtr)(num13 + 3U))] << 24 |(int)array7[(int)((UIntPtr)(num13 + 2U))] << 16 |(int)array7[(int)((UIntPtr)(num13 + 1U))] << 8 |(int)array7[(int)((UIntPtr)num13)]);
            //num26 = 255U;
            num7 += num14;
            num13 = (uint)num4;
            num_new_params = (uint)((int)cipherText[(int)((UIntPtr)(num13 + 3U))] << 24 | (int)cipherText[(int)((UIntPtr)(num13 + 2U))] << 16 | (int)cipherText[(int)((UIntPtr)(num13 + 1U))] << 8 | (int)cipherText[(int)((UIntPtr)num13)]);
            num8 = num7;
            num7 = 0;

            uint num27 = num8;
            uint num28 = num8;
            uint num29 = 1795577737U;
            uint num30 = 1182509082U;
            uint num31 = num28;
            uint num32 = 1406428146U;
            uint num33 = 526153867U;
            uint num34 = (num29 >> 11 | num29 << 21) ^ num32;
            uint num35 = num34 & 16711935U;
            num34 &= 4278255360U;
            num29 = (num34 >> 8 | num35 << 8);
            uint num36 = 3007391072U;
            num36 = 56678U * (num36 & 65535U) + (num36 >> 16);
            num29 = 37629U * (num29 & 65535U) - (num29 >> 16);
            num29 = 25451U * num29 - num36;
            ulong num37 = (ulong)(num29 * num29);
            if (num37 == 0UL) {
                num37 -= 1UL;
            }
            num32 = (uint)((ulong)(num32 * num32) % num37);
            num36 = 29546U * (num36 & 65535U) + (num36 >> 16);
            num29 = 21832U * (num29 & 65535U) + (num29 >> 16);
            num29 = 7417U * num29 + num36;
            num31 ^= num31 >> 11;
            num31 += num30;
            num31 ^= num31 << 17;
            num31 += num32;
            num31 ^= num31 >> 13;
            num31 += num33;
            num31 = ((num36 << 16) - num32 ^ num30) + num31;
            num8 = num27 + (uint)num31;

            num7 = num8
            num5 = (num7 ^ num_new_params);
            plainText[num4] = (byte)(num5 & 255U); // plainText = decrypted data
            plainText[num4 + 1] = (byte)((num5 & 65280U) >> 8);
            plainText[num4 + 2] = (byte)((num5 & 16711680U) >> 16);
            plainText[num4 + 3] = (byte)((num5 & 4278190080U) >> 24)

            num_interations++
        }
        
    }
    //Decrypted string table is added
    gMO.kpikRL5Cn6 = plainText;
    }
    //Return required string from provided index
    length = massCrypto.ToInt32(massCrypto.decryptedString, \u0020);
    string result = gMO.Nc(gMO.Ym(), gMO.kpikRL5Cn6, \u0020 + 4, length);
    return result;
}

