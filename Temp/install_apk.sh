echo "A shell script to install these apk that test needed:"
echo "请插入手机,请一台一台安装后并点击授权"

for file in ./apk/*
do
  if test -f $file && [ "${file##*.}"x = "apk"x ]
  then
    echo 准备安装 $file
    adb install  $file
  else
    echo $file 不是apk文件,不能安装
  fi
done

echo "Installed Successful !!!"
