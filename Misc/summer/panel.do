spshape2dta 中华人民共和国.shp, saving(sp1520) replace
use sp1520
spset
describe
list in 1/5
generate long fips = _ID
bysort fips: assert _N==1
assert fips !=.
spset fips, modify replace
bysort _CX: assert _N==1
assert _CX !=.
bysort _CY: assert _N==1
assert _CY !=.

drop if adcode == "100000"

drop adcode
sort fips
su fips

merge 1:m fips using panel.dta
keep if _merge ==3
drop _merge
su

xtset fips EndDate

preserve
keep if EndDate == 2015

spmatrix create idistance M 
spmatrix dir
spmatrix create contiguity W 
spmatrix dir

spmatrix export W using W.txt,replace
spmatrix export M using M.txt,replace

restore
su

//随机效应模型
eststo clear
xtreg InnIndRevenue InnRsrchDvlpNum  IntPenetrationRate i.EndDate, re
eststo preg

//空间滞后模型
spxtregress InnIndRevenue InnRsrchDvlpNum  IntPenetrationRate i.EndDate, re dvarlag(W)
eststo sar_W
estat impact InnRsrchDvlpNum 
spxtregress InnIndRevenue InnRsrchDvlpNum  IntPenetrationRate i.EndDate,re dvarlag(M) 
eststo sar_M
estat impact InnRsrchDvlpNum 
spxtregress InnIndRevenue InnRsrchDvlpNum  IntPenetrationRate i.EndDate c.InnRsrchDvlpNum##i.EndDate,re dvarlag(M)
eststo sar_M_interaction
estat impact c.InnRsrchDvlpNum

//空间杜宾模型
spxtregress InnIndRevenue  InnRsrchDvlpNum IntPenetrationRate  i.EndDate,re dvarlag(M)  ivarlag(M:IntPenetrationRate)
eststo durbin_net
spxtregress InnIndRevenue  InnRsrchDvlpNum IntPenetrationRate  i.EndDate,re dvarlag(M)  ivarlag(M:InnRsrchDvlpNum )
eststo durbin_patent
spxtregress InnIndRevenue  InnRsrchDvlpNum IntPenetrationRate  i.EndDate,re dvarlag(M)  ivarlag(M:IntPenetrationRate InnRsrchDvlpNum )
eststo durbin_both

//空间误差模型
spxtregress InnIndRevenue  InnRsrchDvlpNum IntPenetrationRate  i.EndDate,re error(W) 
eststo error_W
spxtregress InnIndRevenue  InnRsrchDvlpNum IntPenetrationRate  i.EndDate,re error(M)
eststo error_M
spxtregress InnIndRevenue  InnRsrchDvlpNum IntPenetrationRate  i.EndDate c.InnRsrchDvlpNum##i.EndDate,re error(M)
eststo error_M_interaction

//空间混合模型
spxtregress InnIndRevenue  InnRsrchDvlpNum IntPenetrationRate  i.EndDate,re dvarlag(W) error(W)  
eststo mixed_W         
spxtregress InnIndRevenue  InnRsrchDvlpNum IntPenetrationRate  i.EndDate,re dvarlag(W) error(M)    
eststo mixed_M          
spxtregress InnIndRevenue  InnRsrchDvlpNum IntPenetrationRate  i.EndDate,re sarpanel  dvarlag(W) error(M)
eststo mixed_sarW    
spxtregress InnIndRevenue  InnRsrchDvlpNum IntPenetrationRate  i.EndDate,re sarpanel  dvarlag(M) error(M)   
eststo mixed_sarM

//输出表格
esttab preg sar_W sar_M sar_M_interaction durbin_net durbin_patent durbin_both error_W error_M error_M_interaction mixed_W mixed_M mixed_sarW mixed_sarM using "pdata.rtf", replace

