# md5sha256
Libraries for generating Content Addresses as md5/hashdepthwidth/sha256-hash for use with my other projects.

This is a similar concept to IPFS's multihash, the theory being that:

While chunks of data can collide if addressed using `md5` only, it'll be damn hard for data to collide that matches its `md5` AND `sha256`.

If ever this theory is proven to be incorrect, this library must be revisited (eg. using SHA512, etc).
