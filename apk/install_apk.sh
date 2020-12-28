echo "A shell script to install these apk that test needed :
poceservice and yosemite"

echo "After installed poceservice and yosemite , you need authorized it by manually"

echo "请插入手机，请一台一台安装后并点击授权"

adb install "./apk/pocoservice.apk"

adb install "./apk/yosemite.apk"

echo "Installed Successful !!!"
