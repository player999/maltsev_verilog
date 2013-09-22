VERILOG=iverilog
TARGET=root
PROJECT_DIR=output
BASIS_DIR=basis
all:clean copy_needed
	./treewalk.py
	$(VERILOG) ./$(PROJECT_DIR)/*.v -o ./$(PROJECT_DIR)/$(TARGET)
	./$(PROJECT_DIR)/$(TARGET)

compile:clean copy_needed
	./treewalk.py
	$(VERILOG) ./$(PROJECT_DIR)/*.v -o ./$(PROJECT_DIR)/$(TARGET)

copy_needed:
	mkdir -p $(PROJECT_DIR)
	cp ./$(BASIS_DIR)/*.v ./$(PROJECT_DIR)/

clean:
	rm -rf ./output

clean-all:clean
	rm -rf __pycache__
	rm -rf ./basis/__pycache__
