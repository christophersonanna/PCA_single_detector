#!/usr/bin/env python3
import argparse, os, datetime
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.optimize import curve_fit

import config, plotting
from load import load_and_transform, get_file_list
from aggregation import extract_event_features
from statistics import calculate_separation

def extract_batch(file_list, args):
    all_f, all_m = [], []
    for f_path in file_list:
        try:
            df = load_and_transform(f_path)
            feats, meta = extract_event_features(df)
            if feats is not None:
                all_f.append(feats); all_m.append(meta)
        except Exception as e: print(f"Error: {e}")
    return (np.vstack(all_f), all_m) if all_f else (None, None)

def balance_dataset(features, metadata, skip=False):
    p_idx = np.where([m['particle'] == config.PROTON_ID for m in metadata])[0]
    i_idx = np.where([m['particle'] == config.IRON_ID for m in metadata])[0]
    if skip or len(p_idx) == 0 or len(i_idx) == 0: return features, metadata
    target = min(len(p_idx), len(i_idx))
    np.random.seed(42); idx = np.concatenate([np.random.choice(p_idx, target, False), np.random.choice(i_idx, target, False)])
    np.random.shuffle(idx)
    return features[idx], [metadata[j] for j in idx]

def fit_pulse_decay(waveform):
    peak_idx = np.argmax(waveform); tail = waveform[peak_idx:]
    if len(tail) < 10: return 0, tail
    t = np.arange(len(tail))
    try:
        popt, _ = curve_fit(plotting.exponential_model, t, tail, p0=[tail[0], 0.1, 0], maxfev=1500)
        return abs(popt[1]), tail
    except: return 0, tail

def analyze_subset(features, metadata, label, out_dir, args):
    # 1. Map particles to 0 and 1 for correlation math
    # We use this both for indexing and for the Point-Biserial correlation
    numeric_labels = np.array([1 if m['particle'] == config.IRON_ID else 0 for m in metadata])
    p_idx = np.where(numeric_labels == 0)[0]
    i_idx = np.where(numeric_labels == 1)[0]
    
    if (len(p_idx) + len(i_idx)) < 10: 
        return 0, len(p_idx), len(i_idx), 0, 0, 0, 0

    if args.norm: 
        features = StandardScaler().fit_transform(features)
    
    safe_label = label.replace(" ", "_").replace(".", "p")
    
    # 2. Fit PCA using the user-defined n_pcs
    pca = PCA(n_components=args.n_pcs)#.fit(features)
    trans = pca.fit_transform(features)
    recon = pca.inverse_transform(trans)
    
    # 3. Physics Analysis (Averages and Decay)
    p_avg, i_avg = np.mean(recon[p_idx], axis=0), np.mean(recon[i_idx], axis=0)
    p_lam, p_tail = fit_pulse_decay(p_avg)
    i_lam, i_tail = fit_pulse_decay(i_avg)
    
    # 4. Statistical Metrics
    sep_val = calculate_separation(trans[p_idx], trans[i_idx])['sep']
    var_exp = np.sum(pca.explained_variance_ratio_)

    # 5. Restored Plotting Suite
    if args.plot_laplace or args.all: 
        plotting.plot_decay_fit(p_tail, i_tail, p_lam, i_lam, f"{out_dir}/decay_{safe_label}.png")
        
    if args.plot_fft or args.all: 
        plotting.plot_frequency_analysis(p_avg, i_avg, f"{out_dir}/fft_{safe_label}.png")
        
    if args.plot_wave or args.all: 
        plotting.plot_mean_std(features[p_idx], features[i_idx], label, f"{out_dir}/wave_{safe_label}.png")
        
    if args.plot_3d or args.all:
        cvs = np.array([m[args.color_by] for m in metadata]) if args.color_by else None
        # This now calls the 2x2 Grid with 3D projection
        plotting.plot_3d_variance_grid(trans[p_idx], trans[i_idx], len(p_idx), len(i_idx), 
                                       f"{out_dir}/3d_{safe_label}.png", cvs, args.color_by)
    
    if args.plot_pcs or args.all:
        plotting.plot_scree(pca, f"{out_dir}/scree_{safe_label}.png")
        # UPDATED: Passes trans and numeric_labels for the correlation text on the grid
        plotting.plot_pca_components(pca, trans, numeric_labels, args.n_pcs, f"{out_dir}/comp_{safe_label}.png")
        
    if args.plot_recon or args.all:
        ps, ismp = recon[np.random.choice(p_idx)], recon[np.random.choice(i_idx)]
        plotting.plot_reconstruction_comparison(p_avg, i_avg, ps, ismp, label, f"{out_dir}/recon_{safe_label}.png")

    return sep_val, len(p_idx), len(i_idx), var_exp, 0, p_lam, i_lam

def main():
    parser = argparse.ArgumentParser(description="TA PCA Analysis")
    parser.add_argument("-i", "--input", nargs='+')
    #better file selection (still need to add in)
    parser.add_argument("-n", type=float, help="Selects every nth file in selected directories")
    parser.add_argument("--force", action='store_true')
    #working to add there cuts to code
    parser.add_argument("-R", "--radius", type=float, help="Radius cut (km)")
    parser.add_argument("-E", "--energy", type=float, help="Energy cut (log10 eV)")
    parser.add_argument("-X", "--xmax", type=float, help="Xmax cut (g/cm^2)")
    parser.add_argument("--is_good,",type=float, help="Good Detector cut (1=not part of cluster, 2=part of space cluster, 3=passed rought time pattern recon, 4=part of event, 5=saturated counter")
    #
    parser.add_argument("--cache")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--norm", action="store_true")
    parser.add_argument("--no-balance", action="store_true")
    parser.add_argument("--sweep", action="store_true")
    parser.add_argument("--plot-3d", action="store_true")
    parser.add_argument("--plot-pcs", action="store_true")
    parser.add_argument("--plot-wave", action="store_true")
    parser.add_argument("--plot-recon", action="store_true")
    parser.add_argument("--plot-fft", action="store_true")
    parser.add_argument("--plot-laplace", action="store_true")
    parser.add_argument("--plot-fidelity", action="store_true")
    parser.add_argument("--n-pcs", type=int, default=12)
    parser.add_argument("--sweep-var", choices=['radius', 'energy', 'theta'], default='radius')
    parser.add_argument("--color-by", type=str)
    args = parser.parse_args()

    out_dir = f"results_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}"; os.makedirs(out_dir, exist_ok=True)
    if args.cache and os.path.exists(args.cache):
        data = np.load(args.cache, allow_pickle=True); f, m = data['features'], data['metadata'].tolist()
    else:
        f, m = extract_batch(get_file_list(args.input), args)
        if args.cache and f is not None: np.savez_compressed(args.cache, features=f, metadata=m)

    if f is None: return
    f, m = balance_dataset(f, m, skip=args.no_balance)
    log_data = []
    
    ''' 
    # Aggregate Events
    all_events = []
    for d in data:
        try:
            loaded = load_and_transform(d)
            all_events.extend(loaded)
        except Exception as e:
            print(f"Failed to load {d}: {e}")
   
    print(f"Total Combined Events: {len(all_events)}")   
    
    
    #Apply Cuts
    events = all_events
    if args.energy:
        events = [e for e in events if abs(e.energy - args.energy) < config.ENERGY_WINDOW]
        print(f"Energy cut applied: {args.energy}")
    if args.xmax:
        events = [e for e in events if abs(e.xmax - args.xmax) < 50.0]
        print(f"Xmax cut applied: {args.xmax}")
        '''
    #Run analysis
    if args.sweep or args.all:
        mapping = {'radius': (config.RADIUS_BINS, config.RADIUS_WINDOW, 'radius'),
                   'energy': (config.ENERGY_BINS, config.ENERGY_WINDOW, 'energy'),
                   'theta':  (config.THETA_BINS, config.THETA_WINDOW, 'theta')}
        bins, win, key = mapping[args.sweep_var]
        for b in bins:
            idx = [i for i, x in enumerate(m) if abs(x[key] - b) < win]
            sep, pn, inc, var, fld, pl, il = analyze_subset(f[idx], [m[j] for j in idx], f"{key}_{b}", out_dir, args)
            log_data.append({'bin': b, 'sep': sep, 'p_count': pn, 'i_count': inc, 'variance': var, 'p_lam': pl, 'i_lam': il})
        
        plotting.plot_sweep_summary(log_data, args.sweep_var, out_dir)
        if args.plot_fidelity or args.all: plotting.plot_fidelity_metrics(log_data, args.sweep_var, f"{out_dir}/fidelity.png")
    else:
        analyze_subset(f, m, "FullSet", out_dir, args)

    pd.DataFrame(log_data).to_csv(f"{out_dir}/log.csv", index=False)

if __name__ == "__main__": main()