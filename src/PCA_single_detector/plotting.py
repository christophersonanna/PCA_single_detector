import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.fft import fft, fftfreq
from scipy.optimize import curve_fit
import math
from scipy.stats import pointbiserialr

def _check_show(save_path=None):
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        print(f"Saved: {save_path}")
    else:
        plt.show()
    plt.close()

def exponential_model(t, a, l, c):
    return a * np.exp(-l * t) + c

def plot_decay_fit(p_tail, i_tail, p_lambda, i_lambda, save_path=None):
    plt.figure(figsize=(10, 6))
    t_p, t_i = np.arange(len(p_tail)), np.arange(len(i_tail))
    plt.plot(t_p, p_tail, 'r.', alpha=0.2, label='Proton Data')
    if p_lambda > 0:
        plt.plot(t_p, exponential_model(t_p, p_tail[0], p_lambda, 0), 'r-', lw=2, label=f'Proton $\lambda$={p_lambda:.4f}')
    plt.plot(t_i, i_tail, 'b.', alpha=0.2, label='Iron Data')
    if i_lambda > 0:
        plt.plot(t_i, exponential_model(t_i, i_tail[0], i_lambda, 0), 'b-', lw=2, label=f'Iron $\lambda$={i_lambda:.4f}')
    plt.yscale('log')
    plt.title("Tail Decay Analysis")
    plt.legend()
    _check_show(save_path)

def plot_frequency_analysis(p_wave, i_wave, save_path=None):
    plt.figure(figsize=(10, 5))
    n = len(p_wave)
    p_fft, i_fft = np.abs(fft(p_wave))[:n//2], np.abs(fft(i_wave))[:n//2]
    freqs = fftfreq(n, d=1.0)[:n//2]
    plt.plot(freqs, p_fft, 'r-', label='Proton')
    plt.plot(freqs, i_fft, 'b-', label='Iron')
    plt.yscale('log')
    plt.title("Frequency Domain (FFT)")
    plt.legend()
    _check_show(save_path)

def plot_pca_components(pca, transformed, labels, n_pcs, save_path=None):
    """
    Plots the requested number of PCs in a grid.
    Includes the Correlation Coefficient (r) with the Particle ID.
    """
    cols = 2
    rows = math.ceil(n_pcs / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(12, 3.5 * rows), sharex=True)
    axes = axes.flatten()
    
    t = np.arange(pca.components_.shape[1])
    
    for i in range(n_pcs):
        if i < len(pca.components_):
            # Calculate Correlation between PC scores and Particle ID
            # labels should be 0 for Proton, 1 for Iron
            r_val, _ = pointbiserialr(labels, transformed[:, i])
            var_pct = pca.explained_variance_ratio_[i] * 100
            
            axes[i].plot(t, pca.components_[i], color='teal', lw=1.5)
            # Bold the title if correlation is high (> 0.3 or < -0.3)
            weight = 'bold' if abs(r_val) > 0.3 else 'normal'
            axes[i].set_title(f"PC {i+1} ({var_pct:.1f}% Var)\nCorr with ID: r = {r_val:.3f}", 
                              fontweight=weight, fontsize=10)
            axes[i].grid(True, alpha=0.2)
        else:
            axes[i].axis('off')

    for j in range(i + 1, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    _check_show(save_path)

def plot_3d_variance_grid(p_trans, i_trans, p_n, i_n, save_path=None, color_vals=None, color_label=None):
    """
    Plots PC1/2, PC1/3, PC2/3, and the 3D projection in a 2x2 grid.
    """
    fig = plt.figure(figsize=(14, 10))
    
    # Subplot coords: (PC_x, PC_y, Grid_Pos)
    configs = [(0, 1, 1), (0, 2, 2), (1, 2, 3)]
    titles = ['PC1 vs PC2', 'PC1 vs PC3', 'PC2 vs PC3']
    
    for x_idx, y_idx, pos in configs:
        ax = fig.add_subplot(2, 2, pos)
        if color_vals is not None:
            comb = np.vstack([p_trans, i_trans])
            sc = ax.scatter(comb[:, x_idx], comb[:, y_idx], c=color_vals, cmap='viridis', s=8, alpha=0.5)
        else:
            ax.scatter(p_trans[:, x_idx], p_trans[:, y_idx], c='red', s=8, alpha=0.4, label='Proton')
            ax.scatter(i_trans[:, x_idx], i_trans[:, y_idx], c='blue', s=8, alpha=0.4, label='Iron')
        ax.set_title(titles[pos-1])
        ax.set_xlabel(f'PC{x_idx+1}'); ax.set_ylabel(f'PC{y_idx+1}')

    # 4th Plot: 3D Projection
    ax3d = fig.add_subplot(2, 2, 4, projection='3d')
    if color_vals is not None:
        comb = np.vstack([p_trans, i_trans])
        sc = ax3d.scatter(comb[:,0], comb[:,1], comb[:,2], c=color_vals, cmap='viridis', s=10, alpha=0.6)
        plt.colorbar(sc, ax=ax3d, label=color_label, pad=0.1)
    else:
        ax3d.scatter(p_trans[:,0], p_trans[:,1], p_trans[:,2], c='red', alpha=0.5)
        ax3d.scatter(i_trans[:,0], i_trans[:,1], i_trans[:,2], c='blue', alpha=0.5)
    
    ax3d.set_title("3D PC Space (1, 2, 3)")
    plt.tight_layout()
    _check_show(save_path)

def plot_scree(pca, save_path=None):
    plt.figure(figsize=(8, 4))
    var = pca.explained_variance_ratio_
    plt.bar(range(1, len(var)+1), var, alpha=0.7, label='Individual')
    plt.step(range(1, len(var)+1), np.cumsum(var), where='mid', label='Cumulative')
    plt.ylabel('Explained Variance Ratio')
    plt.xlabel('PC Index')
    plt.legend()
    _check_show(save_path)

def plot_mean_std(p_feats, i_feats, label, save_path=None):
    plt.figure(figsize=(10, 5))
    t = np.arange(p_feats.shape[1])
    for data, color, name in [(p_feats, 'red', 'Proton'), (i_feats, 'blue', 'Iron')]:
        if len(data) == 0: continue
        mu, std = np.mean(data, axis=0), np.std(data, axis=0)
        plt.plot(t, mu, color=color, label=f'{name} Avg', lw=2)
        plt.fill_between(t, mu-std, mu+std, color=color, alpha=0.15)
    plt.title(f"Average Input Waveforms: {label}")
    plt.xlabel("Time Bin"); plt.ylabel("Amplitude (Normalized)")
    plt.legend()
    _check_show(save_path)

def plot_reconstruction_comparison(p_avg, i_avg, p_samp, i_samp, label, save_path=None):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    t = np.arange(len(p_avg))
    ax1.plot(t, p_avg, 'r-', label='Proton Avg'); ax1.plot(t, i_avg, 'b-', label='Iron Avg')
    ax1.set_title("Average Reconstruction")
    ax2.plot(t, p_samp, 'r--', alpha=0.6, label='Proton Sample'); ax2.plot(t, i_samp, 'b--', alpha=0.6, label='Iron Sample')
    ax2.set_title("Single Event Reconstruction")
    plt.legend()
    _check_show(save_path)

def plot_fidelity_metrics(results, var_name, save_path=None):
    plt.figure(figsize=(10, 6))
    x = [r['bin'] for r in results]
    var = [r['variance'] for r in results]
    plt.plot(x, var, 'g-s', lw=2, label='Explained Variance')
    plt.title(f"PCA Fidelity across {var_name}")
    plt.ylabel("Total Explained Variance Ratio")
    plt.ylim(0, 1.05)
    _check_show(save_path)

def plot_sweep_summary(results, var_name, out_dir):
    # 1. Separation
    plt.figure(figsize=(10, 6))
    x, y = [r['bin'] for r in results], [r['sep'] for r in results]
    plt.plot(x, y, 'ko-', lw=2)
    plt.title(f"Separation vs {var_name}")
    plt.xlabel(var_name.capitalize()); plt.ylabel("Separation Score")
    _check_show(f"{out_dir}/sweep_sep.png")

    # 2. Physics correlation
    x, sep = [r['bin'] for r in results], [r['sep'] for r in results]
    delta_lam = [abs(r['p_lam'] - r['i_lam']) for r in results]
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(x, sep, 'r-o', label='Separation'); ax1.set_ylabel('Separation', color='r')
    ax2 = ax1.twinx(); ax2.plot(x, delta_lam, 'b--s', label='Delta Lambda'); ax2.set_ylabel('Delta Lambda', color='b')
    plt.title("Separation vs Physics Correlation")
    _check_show(f"{out_dir}/sep_vs_decay.png")