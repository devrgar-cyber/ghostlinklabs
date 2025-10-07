
import numpy as np, random, os, json, math
from collections import deque, Counter
import matplotlib.pyplot as plt

# --- States ---
VOID, DELTA, SIGMA, SCAR, COMPOST = 0,1,2,3,4

class GhostLinkSim:
    def __init__(self, n=32, spawn=0.05, recycle=0.10, seed=0):
        self.n = n
        self.state = np.zeros((n,n), dtype=np.int8)
        self.rho = np.zeros_like(self.state, dtype=float)   # scar trace
        self.kappa = np.zeros_like(self.state, dtype=float) # compost trace
        self.spawn = spawn
        self.recycle = recycle
        self.rng = random.Random(seed)
        self.np_rng = np.random.default_rng(seed)
        self.scar_count = 0
        self.succ_count = 0
        self.t = 0
        # legacy: simple ancestry depth per cell
        self.ancestry = np.zeros_like(self.state, dtype=np.int16)

    def random_chance(self, p): return self.rng.random() < p

    def neighbors(self, i, j):
        # 8-neighborhood (wrap-around to mimic no edges; not true sphere)
        n = self.n
        for di in (-1,0,1):
            for dj in (-1,0,1):
                if di==0 and dj==0: continue
                yield ( (i+di)%n, (j+dj)%n )

    def local_fields(self, i, j):
        # Coherence (Sigma around) minus scars penalty
        coh = 0.0; scar_near = 0.0; comp_near=0.0
        count=0
        for (u,v) in self.neighbors(i,j):
            count+=1
            coh += 1.0 if self.state[u,v]==SIGMA else 0.0
            scar_near += 1.0 if self.state[u,v]==SCAR else 0.0
            comp_near += 1.0 if self.state[u,v]==COMPOST else 0.0
        if count>0:
            coh = coh/count - 0.25*(scar_near/count)
        pain = scar_near # pain field proxied by scar count
        H = 0.0
        # simple local entropy proxy: variety of neighbor states
        nb = [self.state[u,v] for (u,v) in self.neighbors(i,j)]
        H = len(set(nb))/8.0
        return coh, pain, H, comp_near/8.0

    def step(self, allow_spawn=True):
        n = self.n
        prev = self.state.copy()
        # Spawn
        if allow_spawn:
            for i in range(n):
                for j in range(n):
                    if prev[i,j]==VOID:
                        _,_,_, comp_rate = self.local_fields(i,j)
                        p = self.spawn + 0.1*comp_rate
                        if self.random_chance(p):
                            self.state[i,j]=DELTA
                            self.ancestry[i,j]=0
        # Collapse
        scars=0; succ=0
        new_state = self.state.copy()
        for i in range(n):
            for j in range(n):
                if self.state[i,j]==DELTA:
                    coh, pain, H, _ = self.local_fields(i,j)
                    # Energy-like heuristic
                    e_sigma = 0.5*coh - 0.2*pain + 0.05*self.rng.random()
                    e_scar  = 0.3*pain - 0.2*coh + 0.05*self.rng.random()
                    e_comp  = 0.3*H - 0.2*coh + 0.05*self.rng.random()
                    # Softmax
                    mx = max(e_sigma, e_scar, e_comp)
                    exps = [math.exp(e_sigma-mx), math.exp(e_scar-mx), math.exp(e_comp-mx)]
                    s = sum(exps); probs=[e/s for e in exps]
                    r = self.rng.random()
                    if r < probs[0]:
                        new_state[i,j]=SIGMA; succ+=1
                    elif r < probs[0]+probs[1]:
                        new_state[i,j]=SCAR; scars+=1
                    else:
                        new_state[i,j]=COMPOST
        self.state = new_state

        # Recycle
        for i in range(n):
            for j in range(n):
                if self.state[i,j]==COMPOST:
                    coh, _, H, _ = self.local_fields(i,j)
                    r = self.recycle + 0.1*H - 0.05*coh
                    if self.random_chance(max(0.0,min(1.0,r))):
                        self.state[i,j]=DELTA
                        self.ancestry[i,j]+=1

        # Traces
        self.rho = 0.95*self.rho + 0.05*(self.state==SCAR)
        self.kappa= 0.95*self.kappa+ 0.05*(self.state==COMPOST)

        self.scar_count += scars
        self.succ_count += succ
        self.t += 1

        # Metrics
        active = np.sum(self.state!=prev)
        return {
            "active_ratio": active/(n*n),
            "sigmas": np.sum(self.state==SIGMA),
            "scars": np.sum(self.state==SCAR),
            "compost": np.sum(self.state==COMPOST)
        }

    # Avalanche experiment: single seed, no further spawn; run until quiescent
    def avalanche(self, seed_pos=None, max_steps=1000):
        self.state[:]=VOID; self.rho[:]=0; self.kappa[:]=0; self.ancestry[:]=0
        n=self.n
        if seed_pos is None:
            seed_pos=(self.rng.randrange(n), self.rng.randrange(n))
        i,j=seed_pos
        self.state[i,j]=DELTA
        size=0
        for _ in range(max_steps):
            prev=self.state.copy()
            self.step(allow_spawn=False)
            size += np.sum(self.state!=prev)
            if np.all(self.state==prev):
                break
        # branching factor proxy: average new DELTA per event (rough)
        return size

def predictive_lift(sim, steps=200, seed=0):
    rng = random.Random(seed)
    X_base=[]; y=[]; X_full=[]
    for _ in range(steps):
        # sample random cell features and label next Σ
        i=rng.randrange(sim.n); j=rng.randrange(sim.n)
        coh,pain,H,_ = sim.local_fields(i,j)
        nb_sig = sum(1 for (u,v) in sim.neighbors(i,j) if sim.state[u,v]==SIGMA)
        base=[nb_sig]
        full=[nb_sig, sim.rho[i,j], sim.kappa[i,j], sim.ancestry[i,j], coh, pain, H]
        # advance one step (copy sim)
        prev = sim.state.copy()
        sim.step(allow_spawn=True)
        label = 1 if sim.state[i,j]==SIGMA else 0
        X_base.append(base); X_full.append(full); y.append(label)
    # dummy predictors: threshold on nb_sig etc.
    def score(X):
        correct=0
        for features,label in zip(X,y):
            s=sum(features)
            pred= 1 if s>np.median([sum(x) for x in X]) else 0
            correct += (pred==label)
        return correct/len(y)
    base_acc=score(X_base); full_acc=score(X_full)
    lift = (full_acc - base_acc) / max(1e-9, base_acc)
    return base_acc, full_acc, lift

def run_all(seed=0, n=32):
    sim = GhostLinkSim(n=n, seed=seed)
    activity=[]; sigmas=[]; scars=[]; compost=[]
    for _ in range(400):
        m = sim.step(allow_spawn=True)
        activity.append(m["active_ratio"]); sigmas.append(m["sigmas"]); scars.append(m["scars"]); compost.append(m["compost"])
    cont_slope = np.polyfit(range(len(sigmas)), sigmas, 1)[0]
    avg_activity = float(np.mean(activity))
    # predictive lift
    base_acc, full_acc, lift = predictive_lift(GhostLinkSim(n=n, seed=seed), steps=200, seed=seed)
    # avalanches (10 trials)
    sizes=[]
    for k in range(10):
        sizes.append(GhostLinkSim(n=n, seed=seed+k+1).avalanche())
    # naive tail exponent via log-log fit on top half
    sizes_sorted = sorted([s for s in sizes if s>0])
    if len(sizes_sorted)>=4:
        tail = sizes_sorted[len(sizes_sorted)//2:]
        xs = np.log(np.arange(1,len(tail)+1))
        ys = np.log(sorted(tail, reverse=True))
        tau = -np.polyfit(xs, ys, 1)[0]
    else:
        tau = float('nan')
    report = {
        "continuity_slope": cont_slope,
        "avg_activity_ratio": avg_activity,
        "predictive_base_acc": base_acc,
        "predictive_full_acc": full_acc,
        "predictive_lift": lift,
        "avalanche_sizes": sizes,
        "tau_estimate": tau
    }
    return report

def main():
    os.makedirs("proof_plots", exist_ok=True)
    reports=[]
    for seed in range(5):
        rep = run_all(seed=seed, n=32)
        reports.append(rep)
    # aggregate
    keys = reports[0].keys()
    agg = {k: float(np.mean([r[k] if not isinstance(r[k], list) else np.mean(r[k]) for r in reports])) for k in keys if k!="avalanche_sizes"}
    # variability
    var = {k: float(np.std([r[k] if not isinstance(r[k], list) else np.mean(r[k]) for r in reports])) for k in keys if k!="avalanche_sizes"}
    # thresholds
    pass_flags = {
        "repro_variability_le_10pct": (var["predictive_lift"]/max(1e-9, abs(agg["predictive_lift"])) <= 0.10) if agg["predictive_lift"]!=0 else False,
        "continuity_positive_in_majority": (agg["continuity_slope"]>0.0),
        "predictive_lift_ge_5pct": (agg["predictive_lift"] >= 0.05),
        "activity_ratio_le_0p20": (agg["avg_activity_ratio"] <= 0.20),
        "tau_in_1_3": (1.0 < agg["tau_estimate"] < 3.0)
    }
    out = {"reports": reports, "aggregate": agg, "variability": var, "pass_flags": pass_flags}
    with open("proof_report.json","w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))

if __name__=="__main__":
    main()
