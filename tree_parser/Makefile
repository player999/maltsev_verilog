VERILOG=iverilog
TARGET=root
PROJECT_DIR=output
all:
	rm -rf ./output
	./treewalk.py
	$(VERILOG) ./$(PROJECT_DIR)/*.v -o ./$(PROJECT_DIR)/$(TARGET)
	./$(PROJECT_DIR)/$(TARGET)

compile:
	rm -rf ./output
	./treewalk.py
	$(VERILOG) ./$(PROJECT_DIR)/*.v -o ./$(PROJECT_DIR)/$(TARGET)


clean:
	rm -rf ./output

clean-all:clean
	rm -rf __pycache__
	rm -rf ./basis/__pycache__
