Pickup-and-delivery traveling salesman problem (PDTSP)

The subdirectory INSTANCES contains the following benchmark instances:

	D (35 instances)
	Dumitrescu, I., Ropke, S, Cordeau, J.-F., Laporte, G.:
	The traveling salesman problem with pickup and delivery: 
	polyhedral results and a branch-and-cut algorithm.
	Math. Prog., 121(1):269-305 (2010)

	R (20 instances)
	Source:
	J. Renaud, F. F. Boctor, and G. Laporte,
	Perturbation heuristics for the pickup and delivery traveling
	salesman problem.
	Comput. Oper. Res., 29(9):1129-1141 (2002)

	T (108 instances)
	Source:
	Renaud, J., Boctor, F. F., Ouenniche, J.:
	A heuristic for the pickup and delivery traveling salesman problem.
	Comput. Oper. Res., 27(9):905-916 (2000)

PICKUP_AND_DELIVERY_SECTION :
Each line is of the form

      <integer> <integer> <real> <real> <real> <integer> <integer>
 
The first integer gives the number of the node.
The second integer gives its demand.
The third and fourth number give the earliest and latest time for the node.
The fifth number specifies the service time for the node.
The last two integers are used to specify pickup and delivery. The first of
these integers gives the index of the pickup sibling, whereas the second integer
gives the index of the delivery sibling. 

The subdirectory TOURS contains the best tours found by LKH-3.

Tabulated results can be found in the subdirectory RESULTS.