GENERATED_FILES = \
	tslab.js 

all: $(GENERATED_FILES)

browserify:
	@browserify -r d3 -r ipy_node -r id3 -r jQuery-browserify ./index.js > tslab.js
