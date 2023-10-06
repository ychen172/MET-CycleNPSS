//Create intermediary points given 2 arrays but in logspace

real[] logspace(real start, real end, int n) {
	int i;
	real step = (end-start)/(n-1);
	real arr[]={};
	for(i= 0; i<n; i++)
	{
		arr.append(10.0**(start+i*step));
	}
	return arr;
}

// cout<<"Imported logspace(start, end, n)"<<endl<<endl;
//Test
// cout<<"testing..."<<endl;
// real test[] = linspace(1,10, 10);
// cout<<test<<endl;