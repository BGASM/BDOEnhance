from PyProbs import Probability as pr
import statistics

tries = 10000


bg = 640000
cbg = 9050000
loggia_acc = 1500000

acc_pri = 3450000
acc_duo = 13800000
acc_tri = 57500000

lg_acc = { 
  "PRI": {"prob": .7, "gem": ('bg', 1)},
  "DUO": {"prob": .4, "gem": ('bg', 2)},
  "TRI": {"prob": .3, "gem": ('bg', 3)},
  "TET": {"prob": .2, "gem": ('bg', 4)},
  "PEN": {"prob": .1, "gem": ('bg', 5)}
  }

lg_clothes = { 
  "1":    {"prob": 1.0, "gem": ('bg', 1)},
  "2":    {"prob": 1.0, "gem": ('bg', 1)},
  "3":    {"prob": 1.0, "gem": ('bg', 1)},
  "4":    {"prob": 1.0, "gem": ('bg', 1)},
  "5":    {"prob": 1.0, "gem": ('bg', 1)},
  "6":    {"prob": .9,  "gem": ('bg', 1)},
  "7":    {"prob": .8,  "gem": ('bg', 1)},
  "8":    {"prob": .7,  "gem": ('bg', 1)},
  "9":    {"prob": .6,  "gem": ('bg', 1)},
  "10":   {"prob": .5,  "gem": ('bg', 1)},
  "11":   {"prob": .45, "gem": ('bg', 1)},
  "12":   {"prob": .4,  "gem": ('bg', 1)},
  "13":   {"prob": .35, "gem": ('bg', 1)},
  "14":   {"prob": .3,  "gem": ('bg', 1)},
  "15":   {"prob": .2,  "gem": ('bg', 1)},
  "PRI":  {"prob": .5,  "gem": ('cbg', 1)},
  "DUO":  {"prob": .4,  "gem": ('cbg', 1)},
  "TRI":  {"prob": .3,  "gem": ('cbg', 1)},
  "TET":  {"prob": .2,  "gem": ('cbg', 1)},
  "PEN":  {"prob": .1,  "gem": ('cbg', 1)}
  }


def get_level(acc, i):
  a_switcher={
    0:'PRI',
    1:'DUO',
    2:'TRI',
    3:'TET',
    4:'PEN'    
  }
  b_switcher={
    0:'1',
    1:'2',
    2:'3',
    3:'4',
    4:'5',
    5:'6',
    6:'7',
    7:'8',
    8:'9',
    9:'10',
    10:'11',
    11:'12',
    12:'13',
    13:'14',
    14:'15',
    15:'PRI',
    16:'DUO',
    17:'TRI',
    18:'TET',
    19:'PEN'
  }
  return a_switcher.get(i, f"Invalid Level {i}") if acc else b_switcher.get(i, "Invalid Level")


def base_prob():
  ctry = 0  
  pri, duo, tri, tet, pen, succ = 0, 0, 0, 0, 0, 0
  while ctry < tries:
    ctry = ctry + 1
    if not pr.Prob(.7):
      pri = pri + 1
      continue
    if not pr.Prob(.4):
      duo = duo + 1
      continue
    if not pr.Prob(.3):
      tri = tri + 1
      continue
    if not pr.Prob(.2):
      tet = tet + 1
      continue
    if not pr.Prob(.1):
      pen = pen + 1
      continue
    succ = succ + 1
  prob = succ / tries
  message = (
  f"Attempts: {tries}\n"
  f"Success: {succ}\n"
  f"Probability: {prob}\n"
  f"Failures: {pri+duo+tri+tet+pen}\n"
  f"Pri: {pri} | Duo: {duo} | Tri: {tri} | Tet: {tet} | Pen: {pen}"
  )
  print(message)

def smash_acc(level):  
  lv_1 = lg_acc[level]
  gem_1 = lv_1["gem"]    
  return (gem_1[0], gem_1[1])  
  
def smash_eq(level):  
  lv_1 = lg_clothes[level]
  gem_1 = lv_1["gem"]    
  return (gem_1[0], gem_1[1])


def base_PRI():
  gems = {"bg": 0, "cbg": 0}
  acc = 1
  dur = 100
  clvl = -1
  succ = False
  lvl = get_level(False, 15)
     
  while not succ:
    x = smash_eq(get_level(False, clvl+1))        
    gems[x[0]] = gems[x[0]] + x[1]    
    if not pr.Prob(lg_clothes[get_level(False, clvl+1)]["prob"]):
      # clvl = -1
      dur = dur - 10
      if dur <= 10:        
        acc = acc + 9
        dur = 100
      continue
    else:
      clvl = clvl + 1      
      if lvl == get_level(False, clvl):
        succ = True 
  return (gems, acc)

def pri_pen(level):
  gems = {"bg": 0, "cbg": 0}
  acc = 1
  dur = 100
  clvl = 14
  succ = False
  lvl = get_level(False, level)
     
  while not succ:
    x = smash_eq(get_level(False, clvl+1))        
    gems[x[0]] = gems[x[0]] + x[1]    
    if not pr.Prob(lg_clothes[get_level(False, clvl+1)]["prob"]):
      if clvl > 14:
        clvl = clvl - 1
        dur = dur - 10
      if dur <= 10:        
        acc = acc + 9
        dur = 100
      continue
    else:
      clvl = clvl + 1      
      if lvl == get_level(False, clvl):
        succ = True 
  return (gems, acc)

def acc_sim(level):
  gems = {"bg": 0, "cbg": 0}
  acc = 1
  clvl = -1
  succ = False
  lvl = get_level(True, level)
     
  while not succ:
    x = smash_acc(get_level(True, clvl+1))        
    gems[x[0]] = gems[x[0]] + x[1]    
    if not pr.Prob(lg_acc[get_level(True, clvl+1)]["prob"]):
      clvl = -1
      acc = acc + 1
      continue
    else:
      clvl = clvl + 1      
      if lvl == get_level(True, clvl):
        succ = True 
  return (gems, acc)
    

def cost_gems(gems):
  c_bg = gems["bg"]*bg
  c_cbg = gems["cbg"]*cbg
  return c_bg+c_cbg

def base_sim_acc(is_acc, level):
  ctry = 0
  l_bg = []
  l_cbg = []
  l_acc = []
  l_cost = []
  while ctry < tries:
    ctry = ctry + 1
    if is_acc:
      gems, acc = acc_sim(level)
      l_bg.append(gems["bg"])
      l_cbg.append(gems["cbg"])
      l_acc.append(acc)
      l_cost.append(cost_gems(gems)+(acc*loggia_acc))
    else:
      gems1, acc1 = base_PRI()
      gems2, acc2 = pri_pen(level)
      l_bg.append(gems1["bg"]+gems2["bg"])
      l_cbg.append(gems1["cbg"]+gems2["cbg"])
      l_acc.append(acc1+acc2)
      
      l_cost.append(cost_gems(gems1)+cost_gems(gems2)+(acc1*loggia_acc)+(acc2*loggia_acc))

  m_gem = statistics.mean(l_bg)
  m_acc = statistics.mean(l_acc)
  m_cost = statistics.mean(l_cost)
  o_gem = statistics.mean(l_cbg)

  message = (
  f"\n\n{get_level(is_acc, level)}\n"
  f"Attempts: {tries}\n"  
  f"Average Number Black Gems: {m_gem}\n"
  f"Average Number Concentrated Black Gems: {o_gem}\n"
  f"Average Number Accessories: {m_acc}\n"
  f"Average Cost: {m_cost:,}\n"
  )
  print(message)
  return m_cost


def base_sim():
  ctry = 0
  l_gems = []
  l_acc = []
  l_cost = []
  while ctry < tries:
    ctry = ctry + 1
    gems, acc = 0, 0
    succ = False
    
    while not succ:      
      gems = gems + 1
      acc = acc + 1
      if not pr.Prob(.7):            
        continue
      gems = gems + 2
      if not pr.Prob(.4):        
        continue
      gems = gems +3 
      if not pr.Prob(.3):        
        continue
      
      succ = True

    l_gems.append(gems)
    l_acc.append(acc)
    l_cost.append((gems*bg)+(acc*loggia_acc))

  m_gem = statistics.mean(l_gems)
  m_acc = statistics.mean(l_acc)
  m_cost = statistics.mean(l_cost)  
  message = (
  f"\n\nAttempts: {tries}\n"  
  f"Average Number Black Gems: {m_gem}\n"
  f"Average Number Accessories: {m_acc}\n"
  f"Average Cost: {m_cost:,}\n"
  )
  print(message)
  return m_cost

def duo_sim():
  ctry = 0
  l_gems = []
  l_acc = []
  l_cost = []
  while ctry < tries:
    ctry = ctry + 1
    gems, acc = 0, 0
    succ = False
    
    while not succ:      
      acc = acc + 1      
      gems = gems +3 
      if not pr.Prob(.3):        
        continue
      
      succ = True

    l_gems.append(gems)
    l_acc.append(acc)
    l_cost.append((gems*bg)+(acc*acc_duo))
  m_gem = statistics.mean(l_gems)
  m_acc = statistics.mean(l_acc)
  m_cost = statistics.mean(l_cost)
  message = (
  f"\n\nDuo->TRI Attempts: {tries}\n"  
  f"Average Number Black Gems: {m_gem}\n"
  f"Average Number Duo Accessories: {m_acc}\n"
  f"Average Cost: {m_cost:,}\n"
  )
  print(message)
  return m_cost


base_prob()
cost1 = base_sim()
print("\n\n---------Accessory---------\n")
cost2 = base_sim_acc(True, 0)
cost3 = base_sim_acc(True, 1)
cost4 = base_sim_acc(True, 2)
cost5 = base_sim_acc(True, 3)
cost6 = base_sim_acc(True, 4)
print("\n\n---------Equipment---------\n")
cost7 = base_sim_acc(False, 15)
cost8 = base_sim_acc(False, 16)
cost9 = base_sim_acc(False, 17)
cost10 = base_sim_acc(False, 18)
cost11 = base_sim_acc(False, 19)



  


  
