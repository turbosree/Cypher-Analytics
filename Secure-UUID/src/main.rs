// A universally unique identifier (UUID) is a 128-bit label used to
// identify entities in a distibuted system. 
// UUID can be generated using the X509 certificate data by simply 
// creting a SHA256 of the bytes and taking the first 16 bytes of the
// hash.
// In general, a 16-byte (i.e., 128-bit) unique ID generated using SHA256 
// is considered to be optimal length and extremely unlikely to collide, 
// even if there are a large number of certificates being considered. 
// The chances of a collision are on the order of 2^-128, 
// which is an astronomically small probability. 
// In practice, you can choose to take the first 16 bytes, the last 16 bytes, 
// or any other 16-byte sequence from the hash as your unique ID. 
// The choice is largely arbitrary and depends on your specific needs and 
// preferences. However, it's important to be consistent in your choice of byte 
// sequence to ensure that the same unique ID is generated for the same 
// certificate data every time.
// 
// Author: sreejith.naarakathil@gmail.com

use std::fs::File;
use std::io::Read;
use openssl::sha::sha256;
use hex;

fn main() -> std::io::Result<()> {
    // Open the X509 certificate file.
    let mut file = File::open("../test-ca/ecdsa/end.cert")?;

    // Read the file contents into a buffer.
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer)?;

    // Compute the SHA256 hash of the certificate data.
    let hash = sha256(&buffer);

    // Take the first 16 bytes of the hash as the unique ID.
    let unique_id = &hash[..16];

    // Print the unique ID as a hex string.
    println!("{}", hex::encode(unique_id));

    Ok(())
}

