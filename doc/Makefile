all: \
	concept.png \
	concept-forum.png


concept.png: concept.svg
	inkscape --export-filename=$@ --export-overwrite --export-background='#FFFFFFFF' $<

concept-forum.svg: concept.svg
	sed -e '/fill:/! s/style="\([^"]*\)"/style="\1;fill:#000000"/g' \
	    -e 's/#ffffff/#0c1633/g' \
	    -e 's/#000000/#c6ccd7/g' \
	    < concept.svg > $@

concept-forum.png: concept-forum.svg
	inkscape --export-filename=$@ --export-overwrite --export-background='#0c1633' $<
