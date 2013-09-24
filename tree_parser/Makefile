include constants.mk
VERILOG=iverilog
TARGET=root

all:clean copy_needed
	./treewalk.py
	$(VERILOG) ./$(PROJECT_DIR)/*.v -o ./$(PROJECT_DIR)/$(TARGET)
	./$(PROJECT_DIR)/$(TARGET)
	dot $(PROJECT_DIR)/$(PRIMITIVE_GRAPH) -Tpng -o $(PROJECT_DIR)/$(PRIMITIVE_IMG)
	dot $(PROJECT_DIR)/$(SOURCE_GRAPH) -Tpng -o $(PROJECT_DIR)/$(SOURCE_IMG)

compile:clean copy_needed
	./treewalk.py
	$(VERILOG) ./$(PROJECT_DIR)/*.v -o ./$(PROJECT_DIR)/$(TARGET)

copy_needed:
	mkdir -p $(PROJECT_DIR)
	cp ./$(BASIS_FUNCTIONS_DIR)/*.v ./$(PROJECT_DIR)/

clean:
	rm -rf ./output

clean-all:clean
	rm -rf __pycache__
	rm -rf ./$(BASIS_FUNCTIONS_DIR)/__pycache__
	rm -rf ./constants.mk