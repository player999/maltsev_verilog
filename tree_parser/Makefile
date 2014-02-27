include constants.mk
VERILOG=iverilog
ASSEMBLER=nasm
TARGET=root
NASM_FLAGS=-f elf64
CC=gcc
all:compile
	@./$(PROJECT_DIR)/$(TARGET)

compile:clean copy_needed
	@./treewalk.py
	@dot $(PROJECT_DIR)/$(PRIMITIVE_GRAPH) -Tpng -o $(PROJECT_DIR)/$(PRIMITIVE_IMG)
	@dot $(PROJECT_DIR)/$(SOURCE_GRAPH) -Tpng -o $(PROJECT_DIR)/$(SOURCE_IMG)

ifeq ($(PLATFORM),verilog)
	@$(VERILOG) ./$(PROJECT_DIR)/*.v -o ./$(PROJECT_DIR)/$(TARGET)
endif 
ifeq ($(PLATFORM),asm)
	@for i in `ls $(CURDIR)/$(PROJECT_DIR)/*.s`;\
	 do \
		 $(ASSEMBLER) $(NASM_FLAGS)  -l $${i%?}lst $$i; \
	 done
	@$(CC) -g -o $(CURDIR)/$(PROJECT_DIR)/$(TARGET) $(CURDIR)/$(PROJECT_DIR)/*.o
endif

copy_needed:
	@mkdir -p $(PROJECT_DIR)
ifeq ($(PLATFORM),verilog)
	@cp ./$(BASIS_FUNCTIONS_DIR)/*.v ./$(PROJECT_DIR)/
endif

clean:
	@rm -rf ./output

clean-all:clean
	@rm -rf __pycache__
	@rm -rf ./$(BASIS_FUNCTIONS_DIR)/__pycache__
	@rm -rf ./constants.mk
