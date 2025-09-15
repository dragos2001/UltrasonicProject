current_dir=$(pwd)
echo "$current_dir"
echo "This Script is responsible for creating project's build-system, building main.c and uploading to rp2350"
build_dir="$current_dir"/"build"
echo "$build_dir"
if [ -d  "$build_dir" ]; then
	echo "build dir exists."
	cd  "$build_dir"
	if [ "$(ls -A $build_dir)" ]; then
		echo "build from cache..."
		cmake . || goto error
	else
		echo "build from scratch..."
		cmake .. || goto error
	fi
else 
	echo "build dir does not exist."
	mkdir  "$build_dir"
	echo "build from scratch"
	cd "$build_dir"
	cmake .. || goto error
fi	
cd app
make || goto error

echo "Firmware was built!"
read -p  "Uploading to rp2350..."
picotool reboot -f -u || goto error
sleep 2s
picotool load main.uf2 || goto error
sleep 1s
picotool reboot || goto error

echo "main.uf2 was uploaded to rp2350!"

cd "$current_dir"

:error  
echo "An error occurred during the build or upload process."
cd "$current_dir"
exit 1
