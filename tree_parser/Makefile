VERILOG=iverilog
TARGET=root
all:
	rm -f *.v
	./treewalk.py
	rm -f *_tb.v 
	rm -f *.vcd
	$(VERILOG) *.v -o $(TARGET)
	./$(TARGET)
	
clean:
	rm -f *.v
	rm -f *.vcd
	rm -f ./$(TARGET)
	rm -rf ./__pycache__
