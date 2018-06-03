CPLEX		= /usr/ilog12.4
INC      	= -I$(CPLEX)/cplex/include -I$(CPLEX)/concert/include
CPP      	= g++
ARGS    	= -w -fPIC -fexceptions -DNDEBUG -DIL_STD
CPPLIB   	= -L$(CPLEX)/cplex/lib/x86-64_sles10_4.1/static_pic -lilocplex -lcplex -L$(CPLEX)/concert/lib/x86-64_sles10_4.1/static_pic -lconcert -lm -lpthread

build:
	$(CPP) $(ARGS) -o bin/solver model/cplex.cpp $(INC) $(CPPLIB)
run: build
	./bin/solver data/10LT.txt