
// Converts a MAP to python np arrays
void convertCompressorMap(string name, string MAPNAME){
	
	parseFile(MAPNAME);
	
	
	OutFileStream file {filename = name; }
	
	file {filename = name; }
	real ALPHA[] = S_map.TB_Wc.getValues("ALPHA");
	real SPED[]  = S_map.TB_Wc.getValues("SPED",ALPHA[0]);
	real R[] = S_map.TB_Wc.getValues("R",ALPHA[0],SPED[0]);
	cout<<"Converting "<< MAPNAME <<" to a numpy array ..."<<endl;
	cout<<"Alpha = "<<ALPHA<<"\nSpeed ="<<SPED<<"\nRline ="<<R<<endl;
	int i;
	int j;
	
	
	file<<"# MAP NAME : "<<MAPNAME<<endl<<endl;
	file<<"# ---------------------------------"<<endl;
	file<<"import numpy as np"<<endl<<endl;
	file<<"class CmpMap(object):"<<endl;
	file<<"    pass"<<endl;
	file<<"CmpMap.NcDes = "<<S_map.NcMapDes<<endl;
	file<<"CmpMap.RlineDes = "<<S_map.RlineMapDes<<endl;

	file<<"\nCmpMap.Nc = np.array([";
	for(i =0; i<SPED.entries(); i++){ file<<SPED[i]<<",";}
	file<<"])\n\n";
	file<<"\nCmpMap.R = np.array([";
	for(i =0; i<R.entries(); i++){ file<<R[i]<<",";}
	file<<"])\n\n";



	file<<"\nCmpMap.Wc = np.array([";
	for(i =0; i<SPED.entries(); i++){
		file<<"[";
		for(j=0; j<R.entries(); j++){
			
			file<<S_map.TB_Wc(0,SPED[i],R[j])<<",";
			
		}
		file<<"],\n";
	}
	file<<"])"<<endl<<endl;

	file<<"\nCmpMap.eff = np.array([";
	for(i =0; i<SPED.entries(); i++){
		file<<"[";
		for(j=0; j<R.entries(); j++){
			
			file<<S_map.TB_eff(0,SPED[i],R[j])<<",";
			
		}
		file<<"],\n";
	}
	file<<"])"<<endl<<endl;

	file<<"\nCmpMap.PR = np.array([";
	for(i =0; i<SPED.entries(); i++){
		file<<"[";
		for(j=0; j<R.entries(); j++){
			
			file<<S_map.TB_PR(0,SPED[i],R[j])<<",";
			
		}
		file<<"],\n";
	}
	file<<"])"<<endl<<endl;
	file.close();
	delete("S_map"); // use this to delete objects!

}

// Converts a MAP to python np arrays
void convertTurbineMap(string name, string MAPNAME){
	
	parseFile(MAPNAME);
	
	
	OutFileStream file {filename = name; }
	
	file {filename = name; }

	real SPED[]  = S_map.TB_Wp.getValues("SPED");
	real PR[] = S_map.TB_Wp.getValues("PR",SPED[0]);
	cout<<"Converting "<< MAPNAME <<" to a numpy array ..."<<endl;
	cout<<"\nSpeed ="<<SPED<<"\nPR ="<<PR<<endl;
	int i;
	int j;
	
	
	file<<"# MAP NAME : "<<MAPNAME<<endl<<endl;
	file<<"# ---------------------------------"<<endl;
	file<<"import numpy as np"<<endl<<endl;
	file<<"class TrbMap(object):"<<endl;
	file<<"    pass"<<endl;
	file<<"TrbMap.NpDes = "<<S_map.NpMapDes<<endl;
	file<<"TrbMap.PRdes = "<<S_map.PRmapDes<<endl;

	file<<"\nTrbMap.Np = np.array([";
	for(i =0; i<SPED.entries(); i++){ file<<SPED[i]<<",";}
	file<<"])\n\n";
	file<<"\nTrbMap.PR = np.array([";
	for(i =0; i<PR.entries(); i++){ file<<PR[i]<<",";}
	file<<"])\n\n";



	file<<"\nTrbMap.Wp = np.array([";
	for(i =0; i<SPED.entries(); i++){
		file<<"[";
		for(j=0; j<PR.entries(); j++){
			
			file<<S_map.TB_Wp(SPED[i],PR[j])<<",";
			
		}
		file<<"],\n";
	}
	file<<"])"<<endl<<endl;

	file<<"\nTrbMap.eff = np.array([";
	for(i =0; i<SPED.entries(); i++){
		file<<"[";
		for(j=0; j<PR.entries(); j++){
			
			file<<S_map.TB_eff(SPED[i],PR[j])<<",";
			
		}
		file<<"],\n";
	}
	file<<"])"<<endl<<endl;

	file.close();
	delete("S_map"); // use this to delete objects!

}

//----------------------------------------------------------
// TURBINE MAPS
//----------------------------------------------------------
// convertTurbineMap("CFM56LPT.py", "lpt_CFM56_3.map");
convertTurbineMap("hptCFM56.py", "hptCFM56.map");
// convertTurbineMap("E3HPT.py", "hptE3.map");
// convertTurbineMap("E3LPT.py", "lptE3.map");

// //----------------------------------------------------------
// // COMPRESSOR MAPS
// //----------------------------------------------------------
// // convertCompressorMap("lpcCFM56.py", "lpcCFM56.map");
// convertCompressorMap("fanCFM56.py", "fanCFM56.map");
convertCompressorMap("HPCAnsysJun26.py", "HPCAnsysJun26.map");
// // convertCompressorMap("lpcE3.py", "lpcE3.map");
// // convertCompressorMap("hpcE3.py", "hpcE3.map");


// // convertCompressorMap("CFM56_padded.py", "lpcCFM56_prash.map");
// convertCompressorMap("CFM56_padded.py", "lpcCFM56_prash_new.map");

// // cout<<S_map.TB_Wc.getTextRep(0)<<endl;
// // cout<<S_map.TB_Wc.getIndependentNames()<<endl;

