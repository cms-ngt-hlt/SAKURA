# SAKURA - Miscellanea Tools
Miscellaneous tools and scripts for NGT Task 3.4 - "HLT Optimal Calibrations"

## CMSSW recipe 
```bash
cmsrel CMSSW_15_0_4
cd CMSSW_15_0_4/src
cmsenv
git cms-init
scram b -j 20
```

## General recipe
```bash
cd $CMSSW_BASE/src
git clone git@github.com:cms-hlt-ngt/sakura.git
cd sakura/MiscellaneaTools
cmsenv
```
