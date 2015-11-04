/*
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
*/

package main

import (
	"bytes"
	"fmt"
	"log"
	"os"
	"os/exec"
	"path"
	"regexp"
	"strings"
)

func md5foldersha256file(filepath string, md5_path string, sha256_path string, output_base_path string) (output string, err error) {
	var hash string
	hash, err = md5sha256(filepath, md5_path, sha256_path)
	if err != nil {
		log.Panic("Error in md5foldersha256file: md5sha256 failed.", err)
		return
	}
	md5_is_next := false
	// md5_hex_length := 32
	sha256_is_next := false
	output = output_base_path
	if len(output) > 0 {
		for string(output[len(output)-1]) == string(os.PathSeparator) {
			output = strings.Trim(output, string(os.PathSeparator))
		}
	}
	dash_array := strings.Split(hash, "-")
	for i := range dash_array {
		if md5_is_next {
			// split hash to pairs
			pairs := regexp.MustCompile("[0-9a-f]{2}").FindAll([]byte(dash_array[i]), -1)
			md5_as_path := path.Join(string(bytes.Join(pairs, []byte(string(os.PathSeparator)))))
			output = path.Join(output, md5_as_path, dash_array[i])
			md5_is_next = false
		} else if sha256_is_next {
			output = output + "-" + dash_array[i]
			sha256_is_next = false
		} else if dash_array[i] == "md5" {
			md5_is_next = true
		} else if dash_array[i] == "sha256" {
			sha256_is_next = true
		} else {
			output = path.Join(output, dash_array[i])
		}
	}
	return
}

func md5sha256(filepath string, md5_path string, sha256_path string) (hash string, err error) {
	// use md5sum and shasum instead of import crypto/sha512
	// because the import has high memory usage (loads the data in RAM)
	// and Go lang uses garbage collection so the high RAM lingers
	// Assume the output is the hash
	md5cmd := exec.Command(md5_path, "-r", filepath)
	md5out, err := md5cmd.Output()
	if err != nil {
		log.Panic("Error in md5sha256: md5_path or file not found.", err)
		return
	}
	sha256cmd := exec.Command(sha256_path, "--algorithm", "256", filepath)
	sha256out, err := sha256cmd.Output()
	if err != nil {
		log.Panic("Error in md5sha256: sha256_path or file not found.", err)
		return
	}
	// Assume the first output before space is the hash
	md5_hash := strings.Split(strings.TrimSpace(fmt.Sprintf("%s", md5out)), " ")[0]
	sha256_hash := strings.Split(strings.TrimSpace(fmt.Sprintf("%s", sha256out)), " ")[0]
	hash = "md5-" + md5_hash + "-sha256-" + sha256_hash
	return
}

func main() {
	hash, err := md5sha256("/etc/rc.conf", "md5", "shasum")
	if err != nil {
		log.Panic("Error in main: md5sha256.", err)
	}
	log.Printf(hash)
	hash_path, err := md5foldersha256file("/etc/rc.conf", "md5", "shasum", "./test///")
	if err != nil {
		log.Panic("Error in main: md5foldersha256file.", err)
	}
	log.Printf(hash_path)
}
