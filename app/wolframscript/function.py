TRUNC_MULVAR_NORM = """
truncMultivarNorm[mean_List, cov_List, bounds_List] := Module[
{dist, truncDist},
dist = MultinormalDistribution[mean, cov];
truncDist = TruncatedDistribution[bounds, dist];
RandomVariate[truncDist]
];
"""