for filename in mandelbrodt*; do 
    echo mv \"$filename\" \"${filename//mandelbrodt/mandelbrot}\"; 
done > rename.txt