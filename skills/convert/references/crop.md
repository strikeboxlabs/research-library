# Crop pixels with an explicit coordinate frame

Require an owned, decoded single-frame raster image and the confirmed ImageMagick 6 executable. Define `image_in` as its ordinary absolute path and `image_out` as a fresh absolute .png path. Keep the original unchanged. Establish the input's pixel dimensions with the task's image reader before selecting the rectangle.

Define `geometry` as a reviewed positive width/height and nonnegative x/y offset, for example the **illustrative** `100x80+20+10`. These are pixels: the rectangle starts 20 pixels right and 10 down from the top-left and requests 100 by 80 pixels. Pass one quoted geometry argument directly to the tool; do not turn form values or a generated command string into shell code.

~~~bash
test ! -e "$image_out" && test ! -L "$image_out" &&
  convert "$image_in" +repage -gravity NorthWest -crop "$geometry" +repage "$image_out"
status=$?
~~~

Both offsets matter: omitting them asks for tiles, which can produce multiple images rather than one selected rectangle. The initial `+repage` resets virtual-canvas metadata so coordinates refer to the visible pixels; the final one removes the crop's retained canvas offset. Explicit gravity makes the coordinate origin deliberate.

Choose a rectangle inside the decoded input when exact output dimensions are required. An overhanging region can be clipped; a missed image can yield a one-pixel transparent result with a warning. Inspect stderr/status and decode the output to compare dimensions and actual retained pixels. A produced filename or zero status alone does not establish the intended crop. A policy/decoder failure is a prerequisite gap; choose a fresh output for a retry rather than using a partial result.

See the [crop and canvas option definitions](https://legacy.imagemagick.org/script/command-line-options.php/#crop) for implementation-specific geometry behavior.
