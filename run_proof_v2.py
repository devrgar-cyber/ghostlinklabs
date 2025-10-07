
import os, math, json, random
import numpy as np

VOID, DELTA, SIGMA, SCAR, COMPOST = 0,1,2,3,4

def mutual_information(x, y, bins=8):
    x = np.asarray(x).ravel()
    y = np.asarray(y).ravel()
    if x.size == 0 or y.size == 0 or x.size != y.size:
        return 0.0
    x_bins = np.histogram_bin_edges(x, bins=bins)
    y_bins = np.histogram_bin_edges(y, bins=bins)
    px, _ = np.histogram(x, bins=x_bins, density=True)
    py, _ = np.histogram(y, bins=y_bins, density=True)
    pxy, _, _ = np.histogram2d(x, y, bins=[x_bins, y_bins], density=True)
    eps = 1e-12
    px = px + eps; py = py + eps; pxy = pxy + eps
    px /= px.sum(); py /= py.sum(); pxy /= pxy.sum()
    mi = 0.0
    for i in range(pxy.shape[0]):
        for j in range(pxy.shape[1]):
            mi += pxy[i,j]*math.log(pxy[i,j]/(px[i]*py[j]))
    return mi / math.log(2.0)

def logistic(z): 
    return 1.0/(1.0+math.exp(-z))

class GhostLinkSim:
    def __init__(self, n=16, spawn=0.05, recycle=0.10, seed=0):
        self.n = n
        self.state = np.zeros((n,n), dtype=np.int8)
        self.rho = np.zeros_like(self.state, dtype=float)
        self.kappa = np.zeros_like(self.state, dtype=float)
        self.ancestry = np.zeros_like(self.state, dtype=np.int16)
        self.spawn = spawn
        self.recycle = recycle
        self.rng = random.Random(seed)
        self.np_rng = np.random.default_rng(seed)
        self.t = 0
        self.events = []
        self._next_eid = 1
        self.theta_self_sigma = 0.05
        self.theta_self_scar  = 0.02

    def neighbors(self, i, j):
        n = self.n
        for di in (-1,0,1):
            for dj in (-1,0,1):
                if di==0 and dj==0: continue
                yield ( (i+di)%n, (j+dj)%n )

    def local_fields(self, i, j):
        coh = 0.0; scar_near=0.0; comp_near=0.0
        nb_states=[]
        for (u,v) in self.neighbors(i,j):
            nb_states.append(self.state[u,v])
            coh += 1.0 if self.state[u,v]==SIGMA else 0.0
            scar_near += 1.0 if self.state[u,v]==SCAR else 0.0
            comp_near += 1.0 if self.state[u,v]==COMPOST else 0.0
        if len(nb_states)>0:
            coh = (coh/len(nb_states)) - 0.25*(scar_near/len(nb_states))
        H = len(set(nb_states))/max(1,len(nb_states))
        pain = scar_near
        return coh, pain, H, comp_near/8.0

    def encode_self(self):
        n2 = self.n*self.n
        sigmas = float(np.sum(self.state==SIGMA))/n2
        scars  = float(np.sum(self.state==SCAR))/n2
        compost= float(np.sum(self.state==COMPOST))/n2
        ancestry_mean = float(np.mean(self.ancestry))
        activity = float(np.mean(self.activity_mask)) if hasattr(self, "activity_mask") else 0.0
        rho_mean = float(np.mean(self.rho))
        kappa_mean = float(np.mean(self.kappa))
        left = self.state[:,:self.n//2].ravel()
        right= self.state[:,self.n//2:].ravel()
        mapv = np.array([0,1,2,3,4], dtype=float)
        lc = mapv[left].mean() if left.size>0 else 0.0
        rc = mapv[right].mean() if right.size>0 else 0.0
        integration = 1.0 - abs(lc - rc)/4.0
        return np.array([sigmas, scars, compost, ancestry_mean, activity, rho_mean, kappa_mean, integration], dtype=float)

    def log_event(self, typ, i, j, parent=0):
        eid = self._next_eid; self._next_eid += 1
        self.events.append({"id":eid, "type":int(typ), "i":int(i), "j":int(j), "t":int(self.t), "parent":int(parent)})
        return eid

    def step(self, allow_spawn=True, shock=None):
        prev = self.state.copy()
        if shock is not None:
            (i0,i1,j0,j1) = shock
            self.state[i0:i1, j0:j1] = VOID

        if allow_spawn:
            for i in range(self.n):
                for j in range(self.n):
                    if self.state[i,j]==VOID:
                        _,_,_, comp_rate = self.local_fields(i,j)
                        p = self.spawn + 0.1*comp_rate
                        if self.rng.random() < p:
                            self.state[i,j]=DELTA
                            self.ancestry[i,j]=0
                            self.log_event(DELTA,i,j,0)

        s = self.encode_self()
        self.activity_mask = (self.state != prev).astype(np.float32)

        new_state = self.state.copy()
        self_sum = float(s.sum())
        for i in range(self.n):
            for j in range(self.n):
                if self.state[i,j]==DELTA:
                    coh, pain, H, _ = self.local_fields(i,j)
                    e_sigma = 0.5*coh - 0.2*pain + 0.05*self.rng.random() + self.theta_self_sigma*self_sum
                    e_scar  = 0.3*pain - 0.2*coh + 0.05*self.rng.random() + self.theta_self_scar*self_sum
                    e_comp  = 0.3*H    - 0.2*coh + 0.05*self.rng.random()
                    mx = max(e_sigma,e_scar,e_comp)
                    exps = [math.exp(e_sigma-mx), math.exp(e_scar-mx), math.exp(e_comp-mx)]
                    ssum = sum(exps); probs=[e/ssum for e in exps]
                    r = self.rng.random()
                    if r < probs[0]:
                        new_state[i,j]=SIGMA
                        self.log_event(SIGMA,i,j,0)
                    elif r < probs[0]+probs[1]:
                        new_state[i,j]=SCAR
                        self.log_event(SCAR,i,j,0)
                    else:
                        new_state[i,j]=COMPOST
                        self.log_event(COMPOST,i,j,0)
        self.state = new_state

        for i in range(self.n):
            for j in range(self.n):
                if self.state[i,j]==COMPOST:
                    coh, _, H, _ = self.local_fields(i,j)
                    r = self.recycle + 0.1*H - 0.05*coh
                    r = max(0.0,min(1.0,r))
                    if self.rng.random() < r:
                        self.state[i,j]=DELTA
                        self.ancestry[i,j]+=1
                        self.log_event(DELTA,i,j,0)

        self.rho = 0.95*self.rho + 0.05*(self.state==SCAR)
        self.kappa= 0.95*self.kappa+ 0.05*(self.state==COMPOST)

        self.t += 1
        m = {
            "sigmas": int(np.sum(self.state==SIGMA)),
            "scars": int(np.sum(self.state==SCAR)),
            "compost": int(np.sum(self.state==COMPOST)),
            "activity_ratio": float(np.mean(self.activity_mask))
        }
        return m

    def influence_weights(self):
        n=self.n
        samples = { (di,dj): ([],[]) for di in (-1,0,1) for dj in (-1,0,1) if not (di==0 and dj==0) }
        prev = self.state.copy()
        self.step(allow_spawn=True)
        nxt = self.state.copy()
        for i in range(n):
            for j in range(n):
                for di in (-1,0,1):
                    for dj in (-1,0,1):
                        if di==0 and dj==0: continue
                        u=(i+di)%n; v=(j+dj)%n
                        key=(di,dj)
                        samples[key][0].append(prev[u,v])
                        samples[key][1].append(nxt[i,j])
        mtx = np.zeros((3,3), dtype=float)
        for (di,dj), (xs,ys) in samples.items():
            mi = mutual_information(np.array(xs), np.array(ys), bins=6)
            mtx[di+1,dj+1]=mi
        return mtx

    def origin_min_cut(self, steps=8, sink_threshold=0.7):
        history = []
        s_series = []
        sig_series = []
        for _ in range(steps):
            s = self.encode_self()
            s_series.append(float(s.sum()))
            history.append((s, self.state.copy()))
            self.step(allow_spawn=True)
            sig_series.append(float(np.mean(self.state==SIGMA)))
        C_vals = []
        for k,(s,st) in enumerate(history):
            integration = s[-1]
            ancestry_mean=float(np.mean(self.ancestry))
            z = 2.0*sig_series[min(k,len(sig_series)-1)] + 0.5*integration + 0.1*ancestry_mean
            C_vals.append(logistic(z))
        t_sink = max(range(len(C_vals)), key=lambda k:C_vals[k])
        if C_vals[t_sink] < sink_threshold:
            return {"note":"no sink above threshold", "C_max": float(C_vals[t_sink])}
        for frac in (0.25, 0.5, 0.75):
            backup_state = self.state.copy()
            backup_rho = self.rho.copy(); backup_kappa=self.kappa.copy(); backup_ances=self.ancestry.copy()
            mask = (self.state==SIGMA)
            coords = np.argwhere(mask)
            self.rng.shuffle(coords.tolist())
            k = int(len(coords)*frac)
            for (i,j) in coords[:k]:
                self.state[i,j]=VOID
            for _ in range(2):
                self.step(allow_spawn=True)
            sig = float(np.mean(self.state==SIGMA))
            s = self.encode_self()
            z = 2.0*sig + 0.5*s[-1] + 0.1*float(np.mean(self.ancestry))
            C_cf = logistic(z)
            self.state = backup_state; self.rho=backup_rho; self.kappa=backup_kappa; self.ancestry=backup_ances
            if C_cf < sink_threshold:
                return {"cut_fraction": float(frac), "t_sink": int(t_sink), "C_sink": float(C_vals[t_sink]), "C_counterfactual": float(C_cf)}
        return {"note":"no minimal cut found by proxy", "t_sink": int(t_sink), "C_sink": float(C_vals[t_sink])}

def anomaly_index_terms(sim, window=32):
    uniq = []
    ent = []
    active = []
    s_sums = []
    next_sig = []
    for t in range(window):
        st = sim.state.copy()
        patches=set()
        for i in range(sim.n-2):
            for j in range(sim.n-2):
                patches.add(tuple(st[i:i+3,j:j+3].ravel().tolist()))
        uniq.append(len(patches))
        counts = np.bincount(st.ravel(), minlength=5)/ (sim.n*sim.n)
        H = -np.sum([p*math.log(p+1e-12) for p in counts])
        ent.append(H)
        s = sim.encode_self()
        s_sums.append(float(s.sum()))
        sim.step(allow_spawn=True)
        next_sig.append(float(np.mean(sim.state==SIGMA)))
        active.append(float(np.mean(sim.activity_mask)))
    dL = np.gradient(uniq)
    dH = np.gradient(ent)
    chi = np.var(active[-8:]) if len(active)>=8 else np.var(active)
    mi_self = mutual_information(np.array(s_sums), np.array(next_sig), bins=8)
    integration = sim.encode_self()[-1]
    predlift = np.mean(next_sig[-8:])
    return {
        "L": uniq, "H": ent, "dL": dL.tolist(), "dH": dH.tolist(),
        "MI_self": float(mi_self), "PredLift": float(predlift), "chi": float(chi), "Gamma": float(integration)
    }

def run_suite(seed=0):
    sim = GhostLinkSim(n=16, seed=seed)
    for _ in range(20): sim.step(allow_spawn=True)
    terms = anomaly_index_terms(sim, window=48)
    A = (
        0.5*max(0.0, -terms["dL"][-1]) +
        0.5*max(0.0, terms["dH"][-1])  +
        0.2*terms["MI_self"] +
        0.5*terms["PredLift"] +
        0.3*terms["chi"] + 
        0.3*terms["Gamma"]
    )
    sig = float(np.mean(sim.state==SIGMA))
    s  = sim.encode_self()
    C = logistic( 2.0*sig + 0.5*s[-1] + 0.1*float(np.mean(sim.ancestry)) + 0.5*A )
    origin = sim.origin_min_cut(steps=8, sink_threshold=0.7)
    report = {
        "seed": seed,
        "A_index": float(A),
        "C_marker": float(C),
        "terms": terms,
        "origin_result": origin
    }
    return report

def main():
    reports = [run_suite(seed=s) for s in range(3)]
    agg = {
        "A_mean": float(np.mean([r["A_index"] for r in reports])),
        "C_mean": float(np.mean([r["C_marker"] for r in reports])),
    }
    with open("proof_v2_report.json","w") as f:
        json.dump({"reports":reports, "aggregate":agg}, f, indent=2)
    with open("origin_report.json","w") as f:
        json.dump({"reports":[r["origin_result"] for r in reports]}, f, indent=2)
    print(json.dumps({"aggregate":agg}, indent=2))

if __name__=="__main__":
    main()
