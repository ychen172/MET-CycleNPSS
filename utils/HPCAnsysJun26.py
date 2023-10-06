# MAP NAME : HPCAnsysJun26.map

# ---------------------------------
import numpy as np

class CmpMap(object):
    pass
CmpMap.NcDes = 0.946052
CmpMap.RlineDes = 2.56506

CmpMap.Nc = np.array([0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1,])


CmpMap.R = np.array([1,1.182,1.364,1.545,1.727,1.909,2.091,2.273,2.455,2.636,2.818,3,])


CmpMap.Wc = np.array([[0.225,0.231,0.238,0.246,0.256,0.266,0.277,0.29,0.304,0.32,0.343,0.399,],
[0.255,0.263,0.271,0.28,0.29,0.301,0.312,0.325,0.338,0.353,0.368,0.383,],
[0.285,0.294,0.303,0.312,0.323,0.333,0.345,0.357,0.37,0.384,0.398,0.412,],
[0.315,0.324,0.334,0.344,0.354,0.365,0.377,0.389,0.401,0.414,0.427,0.441,],
[0.344,0.354,0.365,0.375,0.385,0.396,0.408,0.419,0.432,0.444,0.457,0.47,],
[0.374,0.385,0.396,0.407,0.417,0.428,0.439,0.45,0.462,0.474,0.487,0.5,],
[0.404,0.417,0.428,0.439,0.449,0.46,0.471,0.482,0.493,0.505,0.517,0.529,],
[0.435,0.448,0.461,0.472,0.482,0.493,0.504,0.514,0.525,0.537,0.548,0.56,],
[0.466,0.481,0.494,0.506,0.517,0.527,0.537,0.548,0.559,0.569,0.58,0.592,],
[0.499,0.515,0.529,0.541,0.552,0.562,0.572,0.582,0.593,0.603,0.613,0.624,],
[0.534,0.549,0.564,0.577,0.588,0.598,0.608,0.618,0.628,0.638,0.647,0.657,],
[0.566,0.582,0.599,0.614,0.625,0.635,0.645,0.655,0.665,0.674,0.683,0.693,],
])


CmpMap.eff = np.array([[0.897,0.901,0.905,0.909,0.911,0.913,0.914,0.915,0.915,0.914,0.918,0.935,],
[0.898,0.903,0.907,0.909,0.911,0.913,0.914,0.915,0.914,0.914,0.913,0.911,],
[0.897,0.902,0.906,0.909,0.91,0.912,0.913,0.913,0.913,0.913,0.912,0.911,],
[0.895,0.9,0.904,0.906,0.908,0.91,0.911,0.911,0.911,0.911,0.911,0.91,],
[0.89,0.896,0.9,0.903,0.905,0.907,0.908,0.908,0.908,0.909,0.908,0.908,],
[0.885,0.892,0.897,0.9,0.902,0.904,0.905,0.905,0.906,0.906,0.906,0.905,],
[0.88,0.887,0.893,0.897,0.899,0.9,0.901,0.902,0.902,0.902,0.902,0.902,],
[0.873,0.881,0.888,0.892,0.895,0.897,0.897,0.898,0.898,0.898,0.898,0.898,],
[0.866,0.875,0.882,0.887,0.89,0.892,0.892,0.893,0.894,0.894,0.894,0.893,],
[0.859,0.868,0.876,0.881,0.884,0.886,0.887,0.888,0.888,0.888,0.888,0.888,],
[0.854,0.861,0.869,0.875,0.878,0.879,0.88,0.881,0.882,0.882,0.882,0.881,],
[0.845,0.852,0.861,0.868,0.871,0.873,0.874,0.875,0.875,0.875,0.875,0.874,],
])


CmpMap.PR = np.array([[1.401,1.401,1.399,1.396,1.392,1.388,1.382,1.376,1.369,1.361,1.353,1.333,],
[1.511,1.51,1.508,1.504,1.499,1.493,1.487,1.48,1.472,1.464,1.455,1.446,],
[1.639,1.639,1.636,1.632,1.626,1.619,1.613,1.605,1.597,1.587,1.578,1.567,],
[1.788,1.788,1.786,1.781,1.775,1.768,1.76,1.752,1.743,1.734,1.723,1.712,],
[1.959,1.961,1.96,1.955,1.948,1.94,1.931,1.922,1.912,1.902,1.89,1.878,],
[2.152,2.159,2.16,2.155,2.147,2.138,2.128,2.118,2.107,2.095,2.084,2.078,],
[2.369,2.383,2.388,2.385,2.376,2.366,2.355,2.344,2.332,2.319,2.305,2.291,],
[2.613,2.636,2.648,2.648,2.641,2.629,2.616,2.603,2.589,2.575,2.56,2.544,],
[2.882,2.921,2.943,2.947,2.941,2.928,2.913,2.898,2.883,2.867,2.85,2.832,],
[3.188,3.241,3.273,3.285,3.281,3.266,3.25,3.233,3.215,3.196,3.175,3.154,],
[3.548,3.595,3.638,3.662,3.661,3.646,3.63,3.613,3.593,3.569,3.543,3.516,],
[3.903,3.964,4.044,4.088,4.087,4.077,4.065,4.048,4.024,3.996,3.966,3.938,],
])
