n=0
echo "### [BACK](../README.md)"> README.md
for image in *.png; do
    echo "> ###### $image" >> README.md
    echo "> ![image $n]($image)" >> README.md
    echo >> README.md
    let n=n+1
done