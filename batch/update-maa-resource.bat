D:

cd "D:\Game\MAA"

cd "./new_resource"
git pull origin main
cd ..

cp -r -f "./new_resource/resource" "."

echo "Resource updated!"

timeout /t 5

exit