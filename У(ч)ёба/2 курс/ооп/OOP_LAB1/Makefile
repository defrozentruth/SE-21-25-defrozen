all: main

main: *.o
		g++ *.o -o main

*.o:
		g++ -c *.cpp -Imodules

clean: 
		rm -f *.o

cleanAll: clean
	rm -f main