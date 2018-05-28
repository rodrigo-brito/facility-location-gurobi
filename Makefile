TWOUP    = $(GUROBI_HOME)
INC      = $(TWOUP)/include/
CPP      = g++-4.9
CARGS    = -m64 -g
CPPLIB   = -L$(TWOUP)/lib -lgurobi_c++ -lgurobi80                                                                                                   

build:
	$(CPP) $(CARGS) -o bin/solver src/solver.cpp -I$(INC) $(CPPLIB) -lm
run: build
	./bin/solver teste.m