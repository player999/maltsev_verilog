MALTSEV ALGEBRA VERILOG IMPLEMENTATION
======================================
Requirements
------------
* Icarus verilog
* GCC
* Python 3
* Graphviz
* Gtkwave
* Intel Qsys

Usage
-----
* Run make in tree\_parser directory.
* Sample project is in deleteme.txt.
* Numbers in the brackets in Makefile ("./treewalk.py deleteme.txt [30,7]") means arguments
* tree\_parser/output contains generated files

* accelerator_*_hw.tcl -- block for QSys  
* accelerator\_.v --verilog source of block for QSys 
* dump.vcd -- testbench waveform
* output.html -- Main report
* .eps -- graphs 
* .v -- verilog sources
* \_json.txt -- JSON description of tree
* root\_tb.v -- Main testbench
* root\_\*.v -- Main module


