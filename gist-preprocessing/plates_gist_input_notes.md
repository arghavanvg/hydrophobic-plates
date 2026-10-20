# GIST input notes
Reference cpptraj input for running GIST on one plate simulation.

```
parm /gibbs/arghavan/plate_simulations/{t}K/{d}/topol_edited.prmtop
trajin /gibbs/arghavan/plate_simulations/{t}K/{d}/{t}K_{d}.nc
gist refdens refdens{t} temp {t} gridspacn 0.10 gridcntr 25 25.38 40 griddim {d*100} 170 170 floatfmt double floatprec 8 prefix gZ info Info.dat
go
```

For example:
```
gist pme refdens 0.03331284139 temp 300 gridspacn 0.10 gridcntr 25 25.38 40 griddim 504 500 796 floatfmt double floatprec 8 prefix d-{d_in_angstrom} info Info.dat
go
```
