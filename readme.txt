/*************************************************
//
// Copyright (C) 2016, Y. Nomura, all right reserved.
// This software is released under the MIT License.
//
// http://opensource.org/licenses/mit-license.php
//
*************************************************/

This script is not fully tested.
Partially tested in Python 2.7(windows).

This script need/read "Legacy footprint library format".
And create the "S-Expression libraries".

"oldfilename" is the filename of Legacy format.

"folder" is the relative folder path.


line 23 - 59 are options that works if the value is not "0"


"DEF_SMD" should be 1 if the modules in library are all SMD module.

The sample creat the S-Expression libraries from pinarray.mod (Ver bzr4022) is in "lib" folder.

