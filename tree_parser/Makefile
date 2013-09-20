VERILOG=iverilog
TARGET=root
all:
	rm -rf ./output
	rm -f *.v
	./treewalk.py
	rm -f *_tb.v 
	rm -f *.vcd
	rm -f *.png
	$(VERILOG) *.v -o $(TARGET)
	./$(TARGET)

compile:
	rm -rf ./output
	rm -f *.v
	./treewalk.py
	rm -f *_tb.v 
	rm -f *.vcd
	rm -f *.png
	$(VERILOG) *.v -o $(TARGET)


clean:
	rm -rf ./output
	rm -f *.v
	rm -f *.vcd
	rm -f ./$(TARGET)
	rm -rf ./__pycache__
	rm -f *.png

clean-all:clean
	rm -rf __pycache__