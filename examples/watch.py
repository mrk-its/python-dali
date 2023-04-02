#!/usr/bin/env python3

import logging
import asyncio
from dali.driver.hid import hasseb
from dali.gear.general import RecallMaxLevel, RecallMinLevel, QueryActualLevel, Off
from dali.address import Broadcast, Short

import struct
import os

async def main():
    # Edit to pick a device type.
    #dev = tridonic("/dev/dali/daliusb-*", glob=True)
    dev = hasseb("/dev/dali/hasseb-*", glob=True)
    dev.connect()
    print("Waiting to be connected...")
    await dev.connected.wait()
    print(f"Connected, firmware={dev.firmware_version}, serial={dev.serial}")
    
    HASSEB_READ_FIRMWARE_VERSION    = 0x02
    HASSEB_CONFIGURE_DEVICE         = 0x05
    #await asyncio.sleep(0.5)
    #os.write(dev._f, struct.pack('BBBBBBBBBB', 0xAA, HASSEB_READ_FIRMWARE_VERSION, 1, 0, 0, 0, 0, 0, 0, 0))
    #await asyncio.sleep(0.5)
    #os.write(dev._f, struct.pack('BBBBBBBBBB', 0xAA, HASSEB_READ_FIRMWARE_VERSION, 2, 0, 0, 0, 0, 0, 0, 0))

    #data = struct.pack('BBBBBBBBBB', 0xAA, HASSEB_CONFIGURE_DEVICE, 3, 1, 0, 0, 0, 0, 0, 0)
    #os.write(dev._f, data)

    while True:
        await asyncio.sleep(1)

    for i in range(3):
        print("Set max...")
        await dev.send(RecallMaxLevel(Broadcast()))
        await asyncio.sleep(1)
        response = await dev.send(QueryActualLevel(Broadcast()))
        print(f"Response was {response}")
        print("Set min...")
        await dev.send(RecallMinLevel(Broadcast()))
        await asyncio.sleep(1)
        response = await dev.send(QueryActualLevel(Broadcast()))
        print(f"Response was {response}")
    await dev.send(Off(Broadcast()))
    dev.disconnect()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
