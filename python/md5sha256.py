'''
Copyright (c) 2015, John Ko
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import hashlib
import os

def md5foldersha256file( data, output_base_path='.' ):
    '''
    Take data, in pass it to md5sha256, return md5 as a folder and sha256 as a file
    Returns STRING, eg /50/58/f1/af/83/88/63/3f/60/9c/ad/b7/5a/75/dc/9d/5058f1af8388633f609cadb75a75dc9d-cdb4ee2aea69cc6a83331bbe96dc2caa9a299d21329efb0336fc02a82e1839a8
    '''
    md5_is_next = False
    md5_hex_length = 32
    sha256_is_next = False
    output = output_base_path
    while output.endswith( "/" ):
        output = output[:-1]
    for i in md5sha256( data ).split( "-" ):
        if md5_is_next:
            md5_as_path = os.sep.join( [ i[start:start+2] for start in range(0, md5_hex_length, 2) ] )
            output = os.sep.join( [ output, md5_as_path, i ] )
            md5_is_next = False
        elif sha256_is_next:
            output = "-".join( [ output, i ] )
            sha256_is_next = False
        elif i == "md5":
            md5_is_next = True
        elif i == "sha256":
            sha256_is_next = True
        else:
            output = os.sep.join( [ output, i ] )
    return output

def md5sha256( data ):
    '''
    Take data in, and hash it with md5 and sha256 separately
    Returns STRING, "md5-" + md5(data).hexdigest() + "-" + "sha256-" + sha256(data).hexdigest()
    '''
    md5_hash = hashlib.md5( data ).hexdigest()
    sha256_hash = hashlib.sha256( data ).hexdigest()
    return "-".join( [ "md5", md5_hash, "sha256", sha256_hash ] )

def compare_str_test( str1, str2 ):
    print str1
    print str2
    if str1 == str2:
        print "[ OK ]"
    else:
        print "[ FAIL ]"

def main():
    print "The following lines should match"
    test_dot = "md5-5058f1af8388633f609cadb75a75dc9d-sha256-cdb4ee2aea69cc6a83331bbe96dc2caa9a299d21329efb0336fc02a82e1839a8"
    compare_str_test( test_dot, md5sha256( "." ) )

    test_path = "./50/58/f1/af/83/88/63/3f/60/9c/ad/b7/5a/75/dc/9d/5058f1af8388633f609cadb75a75dc9d-cdb4ee2aea69cc6a83331bbe96dc2caa9a299d21329efb0336fc02a82e1839a8"
    compare_str_test( test_path, md5foldersha256file( "." ) )

    test_subpath = "./another/50/58/f1/af/83/88/63/3f/60/9c/ad/b7/5a/75/dc/9d/5058f1af8388633f609cadb75a75dc9d-cdb4ee2aea69cc6a83331bbe96dc2caa9a299d21329efb0336fc02a82e1839a8"
    compare_str_test( test_subpath, md5foldersha256file( ".", "./another" ) )

    test_trailslash = "/another/sub/50/58/f1/af/83/88/63/3f/60/9c/ad/b7/5a/75/dc/9d/5058f1af8388633f609cadb75a75dc9d-cdb4ee2aea69cc6a83331bbe96dc2caa9a299d21329efb0336fc02a82e1839a8"
    compare_str_test( test_trailslash, md5foldersha256file( ".", "/another/sub//" ) )

if __name__ == "__main__":
    main()
