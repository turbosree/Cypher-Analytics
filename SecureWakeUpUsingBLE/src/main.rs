// Secure wake up using BLE
// The Generic Access service includes attributes such as the device name
// 
// Author: sreejith.naarakathil@gmail.com

use rumble::CharacteristicHandle;
use rumble::CharacteristicProperties;
use rumble::Peripheral;
use rumble::Result;
use rumble::Service;

use std::sync::mpsc::{Receiver, Sender};
use std::sync::{Arc, Mutex};

// Define UUIDs for the service, characteristics, and descriptors
const GENERIC_ACCESS_SERVICE_UUID: &'static str = "00001800-0000-1000-8000-00805f9b34fb";
const GENERIC_ATTRIBUTE_SERVICE_UUID: &'static str = "00001801-0000-1000-8000-00805f9b34fb";
// Wakeup service
const SERVICE_UUID: &'static str = "00001234-0000-1000-8000-00805f9b34fb";
// CMAC based authentication
const CHARACTERISTIC1_UUID: &'static str = "00001235-0000-1000-8000-00805f9b34fb";
// Your own services
const CHARACTERISTIC2_UUID: &'static str = "00001236-0000-1000-8000-00805f9b34fb";
// Read/Write for Auth protocol
const READ_DESC_UUID: &'static str = "00002902-0000-1000-8000-00805f9b34fb";
const WRITE_DESC_UUID: &'static str = "00002901-0000-1000-8000-00805f9b34fb";

// Define the values for the characteristics
static mut VALUE1: u8 = 0;
static mut VALUE2: u8 = 0;

// Define the callback for when the characteristics are written to
fn write_callback1(_: &Peripheral, ch: CharacteristicHandle, value: &[u8]) {
    unsafe {
        VALUE1 = value[0];
    }
    println!("Value1: {}", unsafe { VALUE1 });
}

fn write_callback2(_: &Peripheral, ch: CharacteristicHandle, value: &[u8]) {
    unsafe {
        VALUE2 = value[0];
    }
    println!("Value2: {}", unsafe { VALUE2 });
}

fn main() -> Result<()> {
    // Create the peripheral
    let mut peripheral = Peripheral::new()?;

    // Define the standard services
    let ga_service = Service::new(GENERIC_ACCESS_SERVICE_UUID)?;
    let ga_device_name_char = ga_service.add_characteristic(
        "00002a00-0000-1000-8000-00805f9b34fb",
        CharacteristicProperties::READ,
    )?;
    let ga_appearance_char = ga_service.add_characteristic(
        "00002a01-0000-1000-8000-00805f9b34fb",
        CharacteristicProperties::READ,
    )?;

    let gatt_service = Service::new(GENERIC_ATTRIBUTE_SERVICE_UUID)?;


    // Define the service, characteristics, and descriptors
    let service = Service::new(SERVICE_UUID)?;
    let characteristic1 = service.add_characteristic_with_props(
        CHARACTERISTIC1_UUID,
        CharacteristicProperties::WRITE,
        write_callback1,
    )?;
    let characteristic2 = service.add_characteristic_with_props(
        CHARACTERISTIC2_UUID,
        CharacteristicProperties::WRITE,
        write_callback2,
    )?;
    let read_desc = characteristic1.add_descriptor(READ_DESC_UUID)?;
    let _ = characteristic2.add_descriptor(READ_DESC_UUID)?;
    let write_desc = characteristic1.add_descriptor(WRITE_DESC_UUID)?;
    let _ = characteristic2.add_descriptor(WRITE_DESC_UUID)?;

    // Add the service to the peripheral
    peripheral.add_service(service)?;
    // Add the standard services and the custom service to the peripheral
    peripheral.add_service(ga_service)?;
    peripheral.add_service(gatt_service)?;

    // Get a list of all the service UUIDs
    let all_services = peripheral.services().into_iter().map(|s| s.uuid().to_string()).collect::<Vec<_>>();
    let all_services_data = AdvertisementData::ServiceUuids16Bit(all_services);
 
    // Advertise the services and the list of all service UUIDs for 5 minutes
    peripheral.advertise(&[
         ga_device_name_char,
         ga_appearance_char,
         characteristic1,
         characteristic2,
     ], &[all_services_data], 300)?;
 
    // Run the event loop to keep the advertisement going for 5 minutes
    peripheral.event_loop();   

    // Advertise the peripheral
    peripheral.advertise()?;
    // Start advertising the peripheral.
    peripheral.start_advertising().unwrap();

    // Set the advertisement data for the peripheral.
    let adv_data = ble::AdvertisementData::new(
        vec![ble::UUID::from_u16(0x1800), ble::UUID::from_u16(0x1801), service_uuid.clone()],
        Vec::new(),
    );
    peripheral.set_advertisement_data(adv_data).unwrap();

    // Loop and wait for write operations on the first characteristic.
    let char1_value = Arc::new(Mutex::new(Vec::new()));
    loop {
        peripheral.poll(Duration::from_secs(1))?;

        // Check for any incoming connections.
        while let Ok(_connection) = peripheral.wait_for_connection(Duration::from_secs(1)) {
            // Connected, do nothing.
        }

        // Check for any incoming write operations on the first characteristic.
        while let Ok((_handle, value)) = peripheral.wait_for_value(&char1_uuid, Duration::from_secs(1)) {
            // Save the value.
            char1_value.lock().unwrap().clone_from(&value);
        }

        // Check if we need to emit a BLE beacon requesting setup assistance for 5 mins.
        if SystemTime::now().duration_since(SystemTime::UNIX_EPOCH).unwrap().as_secs() % 300 == 0 {
            let beacon_data = ble::AdvertisementData::new(
                vec![ble::UUID::from_u16(0xFFFF)],
                Vec::new(),
            );

            peripheral.set_advertisement_data(beacon_data).unwrap();
            peripheral.start_advertising().unwrap();
        }
        // Read the values of the characteristics
        unsafe {
            println!("Value1: {}", VALUE1);
            println!("Value2: {}", VALUE2);
        }    
    }    

}
