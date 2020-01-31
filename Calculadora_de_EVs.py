def stat(base,EV):
    s=int(5+int((int(EV/4)+31+2*base)/2))
    return s

def hp_stat(base,EV):
    s=60+int((int(EV/4)+31+2*base)/2)
    return s

def dmg(Def,atk_power):
    d=int(2+(22*atk_power)/(50*Def))
    return d

def avg_dmg(phys_dmg,sp_dmg,hp):
    #average damage taken from each roll of a physical and a special version of the same move
    tot=0
    for i in range(16):
        tot+=int(phys_dmg*(0.85+i/100))
        tot+=int(sp_dmg*(0.85+i/100))
    ad=tot/(hp*32)
    return ad    

def EVdist(HPb, DEFb, SPDEFb, EVhp, EVdef, EVspdef, EVable):      
    smallest=10
    #standard attack power used is infernape's 0 EVs close combat/focus blast (arbitrary choice)
    atk_power=124*120
    for x in range (EVhp,min(EVhp+EVable+1,253),4):
        available_evs_hp=x-EVhp
        for y in range (EVdef,min(EVdef+EVable-available_evs_hp+1,253),4):
            available_evs_def=y-EVdef
            available_evs_spdef=EVable-available_evs_hp-available_evs_def
            z=EVspdef+available_evs_spdef
            if x>252 or y>252 or z>252:
                print("", end="")
            else:
                admg=avg_dmg(dmg(stat(DEFb,y),atk_power),dmg(stat(SPDEFb,z),atk_power),hp_stat(HPb,x))      
                if admg<smallest and (x==0 or x%8==4) and (y==0 or y%8==4) and (z==0 or z%8==4):
                    smallest=admg
                    NewEVhp=x
                    NewEVdef=y
                    NewEVspdef=z
                    print ('min={0}, HP={1}, Def={2}, SpDef={3}'.format(smallest, x, y, z))
                   
    return smallest, NewEVhp, NewEVdef, NewEVspdef

HPb=int(input("HP: "))
DEFb=int(input("DEF: "))
SPDEFb=int(input("SPDEF: "))
EVhp=int(input("EVHP: "))
EVdef=int(input("EVDEF: "))
EVspdef=int(input("EVSPDEF: "))
EVable=int(input("EVABLE: "))
a, b, c, d = EVdist(HPb, DEFb, SPDEFb, EVhp, EVdef, EVspdef, EVable)
print ('\n', a, b, c, d)      

