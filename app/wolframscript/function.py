TRUNC_MULVAR_NORM = """
truncMultivarNorm[mean_List, cov_List, boundsPair_List] := Module[
{covariance, dist, truncDist,bounds},
covariance = Partition[cov,Sqrt[Length[cov]]];
dist = MultinormalDistribution[mean, covariance];
bounds = Table[boundsPair,{Length[mean]}];
truncDist = TruncatedDistribution[bounds, dist];
While[
    randomVariate = RandomVariate[truncDist];
    Total[Abs[randomVariate]] >= 1
  ];
Return[randomVariate];
];
"""

OPTIMIZED_COV_MTX = """
optimizedCovMatrix[unSolvedCoefficient_List,WgtSdProduct_List]:= Module[
{dim,unSolvedCoefficientMtx,unknownPos,upperTrianglePos,lowerTrianglePos,nVars,vars,WgtSdProductMtx,upperTriangleSub,lowerTriangleSub,CovMtxUpper,CovMtx,eigenVals,InitGuess,timedSol,time,sol,SolvedMatrix},
dim = Sqrt[Length[unSolvedCoefficient]];
unSolvedCoefficientMtx = Partition[unSolvedCoefficient, dim];
WgtSdProductMtx = Partition[WgtSdProduct, dim];
unknownPos = Position[unSolvedCoefficientMtx, x_ /; x ==10];
If[Length[unknownPos] == 0, Return[unSolvedCoefficientMtx * WgtSdProductMtx]];
upperTrianglePos = Select[unknownPos, #[[1]] < #[[2]] &];
lowerTrianglePos = {#[[2]], #[[1]]} & /@ upperTrianglePos;
nVars = Length[upperTrianglePos];
vars = Array[Subscript[x, #] &, nVars];
upperTriangleSub = MapThread[Rule, {upperTrianglePos, vars*Extract[WgtSdProductMtx,upperTrianglePos]}];
lowerTriangleSub = MapThread[Rule, {lowerTrianglePos, vars*Extract[WgtSdProductMtx,upperTrianglePos]}];
CovMtxUpper = ReplacePart[WgtSdProductMtx, upperTriangleSub];
CovMtx = ReplacePart[CovMtxUpper, lowerTriangleSub];
eigenVals = Eigenvalues[CovMtx];
f[OptType_, ObjFunc_, InitGuess_] := Timing[
OptType[
Flatten[{ObjFunc, Abs[#] < 1 & /@ vars, Min[eigenVals] > 0}], MapThread[{#1, #2, -1, 1} &, {vars, InitGuess}]
]];
InitGuess = Table[.001, nVars];
timedSol = Map[f @@ # &, {{FindArgMax, FindArgMin, FindArgMax}, {Min[eigenVals], Total[vars^2], Variance[eigenVals]},Table[InitGuess, 3] } // Transpose];
{time, sol} = {#1, MapThread[Rule, {vars, #}] & /@ #2} & @@ Transpose[timedSol];
SolvedMatrix = ReplacePart[CovMtxUpper, upperTriangleSub /. sol[[1]]];
SolvedMatrix = ReplacePart[SolvedMatrix, lowerTriangleSub /. sol[[1]]];
SolvedMatrix = ReplacePart[SolvedMatrix, Thread[unknownPos -> (SolvedMatrix[[#1, #2]] & @@@ unknownPos)]];
Return[SolvedMatrix];
];
"""
