VERILOG=iverilog
TARGET=root
all:
	rm -f *.v
	./treewalk.py
	rm -f *_tb.v 
	rm -f *.vcd
	rm -f *.png
	$(VERILOG) *.v -o $(TARGET)
	./$(TARGET)

compile:
	rm -f *.v
	./treewalk.py
	rm -f *_tb.v 
	rm -f *.vcd
	rm -f *.png
	$(VERILOG) *.v -o $(TARGET)

	
clean:
	rm -f *.v
	rm -f *.vcd
	rm -f ./$(TARGET)
	rm -rf ./__pycache__
	rm -f *.png
