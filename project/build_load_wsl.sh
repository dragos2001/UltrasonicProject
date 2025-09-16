#!/bin/bash

RED='\033[0;31m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m' 
NC='\033[0m' 

#Step 1:Build and Make the project

#Check for build dir
build_dir="build"
if [ -d $build_dir ];then
  echo -e "$PURPLE Directory exists "
else
  echo -e "$PURPLE Directory doesn't exist "
  mkdir $build_dir
fi

cd $build_dir
#Create build filesystem
echo -e "$CYAN Creating the file system... "
cmake ./
a=$?
if [ $a -ne 0 ]; then
  echo -e "$RED Creating buildsystem failed! " 
  rm -rf ./*
  cmake ..
  a=$?
  if [$a -ne 0 ]; then
    echo -e "$RED Creating buildsystem failed again! "
  else
    echo -e "$CYAN Successfully created the build filesystem!"
  fi
else
  echo -e "$CYAN Successfully created the build filesystem!"

fi

#Navigate to app
cd "app"
echo -e "$CYAN Building the firmware... "

#Build
make -j8
if [ $? -ne 0 ]; then
  echo -e "$RED Building firmware failed! "
  exit 1
fi

#Step 2: Attach USB device (application mode)
echo -e " $CYAN Attaching USB device... "
BUSID=1-4
#List USB devices
cmd.exe /c usbipd list > log.txt
#Look for 2e8a:0009 VID:PID and chain the corresponding line to fragment using awk and return the first field BUSID
BUSID=$(grep '2e8a:0009' log.txt | awk '{print $1}')
echo "Busid:"
echo $BUSID
#Attach to the BUSID
cmd.exe /c usbipd attach --wsl --busid=$BUSID

#Give some time the device to be recognized
sleep 2 

# Step 3: Reboot Pico into BOOTSEL mode
echo -e " $CYAN Rebooting Pico into BOOTSEL mode... "
if ! sudo picotool reboot -f -u; then
   echo -e " $RED Failed to reboot into BOOTSEL mode. Retrying... "
   sleep 1
   sudo picotool reboot -f -u || { echo -e "{$RED}Second attempt failed. Exiting. "; exit 1; }
else 
  echo -e "$CYAN BOOTSEL successful "
fi

#wait 
sleep 2

#Step 4: Attach USB device (BOOTSEL mode)
#List USB devices
cmd.exe /c usbipd list > log2.txt
#Look for 2e8a:0009 VID:PID and chain the corresponding line to fragment using awk and return the first field BUSID
BUSID=$(grep '2e8a:000f' log2.txt | awk '{print $1}')
echo "Busid:"
echo $BUSID

#Attach to the BUSID
cmd.exe /c usbipd attach --wsl --busid=1-4

#waits are very important
sleep 2 

#Step 5: Load firmware
#Navigate to app folder
echo -e "$CYAN Load firmware..."
sudo picotool load main.uf2

echo -e "$PURPLE Detach device"
sudo picotool reboot
cmd.exe /c usbipd detach --busid=$BUSID
