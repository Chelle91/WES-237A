//
//  main.cpp
//  Lab4
//
//  Created by Alireza on 2/14/20.
//  Copyright Â© 2020 Alireza. All rights reserved.
//

#include "main.h"
#include "cycletime.h"
#include "timer.h"
#include <unistd.h>
#include <iostream>

using namespace std;

int main(int argc, const char * argv[])
{
	float cpu_timer;
	unsigned int delay = 1;
	
	cout << "WES237A lab 4" << endl;

	char key=0;
	
	// 1 argument on command line: delay = arg
	if(argc >= 2)
	{
		delay = atoi(argv[1]);
	}

    // Declare 2 cpu_count variables: 1 for before sleeping, 1 for after sleeping
    unsigned long long cpu_before, cpu_after;
    
    // Initialize the counter with reset=1 and enable_divider=1
    init_counters(1, 1);

    // Get the cyclecount before sleeping
    cpu_before = get_cyclecount();
    usleep(delay);
    // Get the cyclecount after sleeping
    cpu_after = get_cyclecount();

    // Subtract the before and after cyclecount
    unsigned long long cycle_diff = cpu_after - cpu_before;
    // Print the cycle count
    cout << "Cycle count: " << cycle_diff << endl;

	LinuxTimer t;
	usleep(delay);
	t.stop();
	cpu_timer = t.getElapsed();

	
	cout << "Timer: " << (double)cpu_timer/1000000000.0 << endl;

	return 0;
}