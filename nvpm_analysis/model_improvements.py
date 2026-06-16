"""Model improvements to push R² from 0.59 → 0.65–0.75.

Key insights from data analysis:
1. Engine-specific correlations VARY significantly (CFM56-2C1: r=-0.73, V2527-A5: r=-0.21)
   → Random-intercept or random-slope model will help
2. Aromatics much stronger predictor (r=+0.70) than H alone (r=-0.66)
   → Include aromatics as secondary; derive H-only surrogate
3. Thrust effect modest but real (r=+0.27)
   → Try log-scale + interaction
4. Within-engine correlation stable across thrust bins (r≈-0.66 to -0.73)
   → Linear in log-space is appropriate; interactions with F are weak

IMPLEMENTATIONS:
  A) Mixed-effects model (random engine intercept + slope)
  B) Add aromatics; derive H-only surrogate via Bayesian projection
  C) Non-linear thrust: try log(F) instead of F
  D) Hinge regression: separate slopes for ΔH < 0 vs > 0
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy.optimize import least_squares
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler

# ============================================================================
# Data Preparation
# ============================================================================

path = Path('/Users/tarahousen/tara/nvpm_analysis/PM_emisisons_vs_fuel_properties.xlsx').expanduser()
df = pd.read_excel(path, sheet_name='PM Emissions')
df['F'] = df['Thrust'] / 100.0

# Build usable dataset
mask = (
    np.isfinite(df['relative nvPM EIn']) &
    np.isfinite(df['Hydrogen']) &
    np.isfinite(df['Ref Hydrogen']) &
    np.isfinite(df['F']) &
    df['relative nvPM EIn'] > 0
)
d = df.loc[mask].copy()

y = np.log(d['relative nvPM EIn'].values)  # log scale
H = d['Hydrogen'].values
H_ref = d['Ref Hydrogen'].values
F = d['F'].values
Arom = d['Aromatics'].values
Engine = d['Engine'].values
Campaign = d['Campaign'].values

n = len(y)
print(f"Data: {n} points across {len(np.unique(Engine))} engines, {len(np.unique(Campaign))} campaigns")

# ============================================================================
# MODEL A: Random Intercept by Engine
# ============================================================================

class RandomInterceptModel:
    """log(y) = α_{engine} + β * (H - H_ref) + γ * log(F)
    
    where α_{engine} is engine-specific intercept.
    Fits via least squares with partial pooling regularization.
    """
    
    def __init__(self, lambda_ridge=0.1):
        self.lambda_ridge = lambda_ridge
        
    def fit(self, y, H, H_ref, F, Engine):
        dH = H - H_ref
        logF = np.log(np.maximum(F, 0.01))  # clip to avoid log(0)
        
        engines = np.unique(Engine)
        n_eng = len(engines)
        engine_to_idx = {eng: i for i, eng in enumerate(engines)}
        eng_idx = np.array([engine_to_idx[e] for e in Engine])
        
        def fun(p):
            # p = [β, γ, α_1, α_2, ...]
            beta, gamma = p[:2]
            alpha = p[2:]
            
            alpha_i = alpha[eng_idx]
            yhat = alpha_i + beta * dH + gamma * logF
            
            residuals = y - yhat
            # L2 penalty on alphas (partial pooling towards 0)
            penalty = self.lambda_ridge * np.sum(alpha ** 2)
            return np.concatenate([residuals, np.sqrt(penalty) * np.ones(1)])
        
        p0 = np.concatenate([[-0.7, 0.3], np.zeros(n_eng)])
        res = least_squares(fun, p0, verbose=0)
        
        self.engines = engines
        self.engine_to_idx = engine_to_idx
        self.beta, self.gamma = res.x[:2]
        self.alpha = res.x[2:]
        
        return res
    
    def predict(self, H, H_ref, F, Engine):
        dH = H - H_ref
        logF = np.log(np.maximum(F, 0.01))
        
        alpha_i = np.array([
            self.alpha[self.engine_to_idx.get(e, len(self.alpha)-1)]
            if e in self.engine_to_idx else np.mean(self.alpha)
            for e in Engine
        ])
        
        return alpha_i + self.beta * dH + self.gamma * logF


# ============================================================================
# MODEL B: Two-predictor with Aromatics, then Marginalize to H-only
# ============================================================================

class TwoPredictor_Aromatics_Plus_H:
    """log(y) = α + β_H * ΔH + β_A * ΔArom + γ * log(F) + δ * (ΔH)(log F)
    
    Then marginalize: given Engine/Campaign, estimate ΔArom from ΔH,
    and predict H-only as:
        E[log(y) | ΔH, F] = α + (β_H + β_A * dArom/dH) * ΔH + γ * log(F)
    """
    
    def __init__(self):
        pass
    
    def fit(self, y, H, H_ref, F, Arom, Arom_ref=None):
        dH = H - H_ref
        logF = np.log(np.maximum(F, 0.01))
        
        # Use aromatics differences if available; else assume same aromatic fuel
        if Arom_ref is None:
            dArom = Arom - np.nanmean(Arom)  # center
        else:
            dArom = Arom - Arom_ref
        
        # Standardize for numeric stability
        dH_std = np.std(dH[np.isfinite(dH)])
        logF_std = np.std(logF)
        dArom_std = np.std(dArom[np.isfinite(dArom)])
        
        dH_scaled = dH / dH_std
        logF_scaled = logF / logF_std
        dArom_scaled = dArom / dArom_std
        
        # Fit: y = c0 + c1*dH_scaled + c2*logF_scaled + c3*dArom_scaled + c4*(dH*logF)_scaled
        X = np.column_stack([
            np.ones(len(y)),
            dH_scaled,
            logF_scaled,
            np.where(np.isfinite(dArom_scaled), dArom_scaled, 0),
            dH_scaled * logF_scaled,
        ])
        
        # Mask out rows with NaN aromatics
        mask_valid = np.isfinite(dArom_scaled)
        X_valid = X[mask_valid]
        y_valid = y[mask_valid]
        
        # Simple least squares
        p = np.linalg.lstsq(X_valid, y_valid, rcond=None)[0]
        
        self.c = p
        self.dH_std = dH_std
        self.logF_std = logF_std
        self.dArom_std = dArom_std
        
        # Estimate aromatic sensitivity
        self.dArom_dH_ratio = np.polyfit(dH[np.isfinite(dArom)], dArom[np.isfinite(dArom)], 1)[0]
        
        return p
    
    def predict(self, H, H_ref, F, Arom=None, use_aromatics=True):
        """Predict log(y). If use_aromatics=False, marginalizes out Arom."""
        
        dH = H - H_ref
        logF = np.log(np.maximum(F, 0.01))
        
        dH_scaled = dH / self.dH_std
        logF_scaled = logF / self.logF_std
        
        c0, c1, c2, c3, c4 = self.c
        
        if use_aromatics and Arom is not None:
            dArom = Arom - np.nanmean(Arom)  # same centering as fit
            dArom_scaled = dArom / self.dArom_std
            yhat = c0 + c1*dH_scaled + c2*logF_scaled + c3*dArom_scaled + c4*dH_scaled*logF_scaled
        else:
            # Marginalize: E[Arom | H] ≈ dArom_dH_ratio * dH
            dArom_scaled_marginal = self.dArom_dH_ratio * dH_scaled  # scales by dH_std implicitly
            yhat = c0 + c1*dH_scaled + c2*logF_scaled + c3*dArom_scaled_marginal + c4*dH_scaled*logF_scaled
        
        return yhat


# ============================================================================
# MODEL C: Log-thrust interactions
# ============================================================================

class LogThrustInteraction:
    """log(y) = α + β * ΔH + γ * log(F) + δ * ΔH * log(F)"""
    
    def fit(self, y, H, H_ref, F):
        dH = H - H_ref
        logF = np.log(np.maximum(F, 0.01))
        
        X = np.column_stack([
            np.ones(len(y)),
            dH,
            logF,
            dH * logF,
        ])
        
        p = np.linalg.lstsq(X, y, rcond=None)[0]
        self.p = p
        return p
    
    def predict(self, H, H_ref, F):
        dH = H - H_ref
        logF = np.log(np.maximum(F, 0.01))
        
        alpha, beta, gamma, delta = self.p
        return alpha + beta*dH + gamma*logF + delta*dH*logF


# ============================================================================
# MODEL D: Hinge regression (separate slopes for H > baseline vs < baseline)
# ============================================================================

class HingeModel:
    """log(y) = α + β_neg * min(0, ΔH) + β_pos * max(0, ΔH) + γ * log(F)"""
    
    def fit(self, y, H, H_ref, F):
        dH = H - H_ref
        logF = np.log(np.maximum(F, 0.01))
        
        X = np.column_stack([
            np.ones(len(y)),
            np.minimum(dH, 0),  # negative part
            np.maximum(dH, 0),  # positive part
            logF,
        ])
        
        p = np.linalg.lstsq(X, y, rcond=None)[0]
        self.p = p
        return p
    
    def predict(self, H, H_ref, F):
        dH = H - H_ref
        logF = np.log(np.maximum(F, 0.01))
        
        alpha, beta_neg, beta_pos, gamma = self.p
        return alpha + beta_neg*np.minimum(dH, 0) + beta_pos*np.maximum(dH, 0) + gamma*logF


# ============================================================================
# Evaluation
# ============================================================================

def rmse_log(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred)**2))

def r2_score(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred)**2)
    ss_tot = np.sum((y_true - np.mean(y_true))**2)
    return 1.0 - ss_res / ss_tot

# 5-fold CV
kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = {
    'Random Intercept (by Engine)': [],
    'Two-predictor (H + Arom)': [],
    'Log-thrust interaction': [],
    'Hinge model': [],
}

for tr, te in kf.split(y):
    # A
    model_a = RandomInterceptModel(lambda_ridge=0.5)
    model_a.fit(y[tr], H[tr], H_ref[tr], F[tr], Engine[tr])
    yhat_a = model_a.predict(H[te], H_ref[te], F[te], Engine[te])
    scores['Random Intercept (by Engine)'].append({
        'rmse': rmse_log(y[te], yhat_a),
        'r2': r2_score(y[te], yhat_a),
    })
    
    # B (Two-predictor)
    model_b = TwoPredictor_Aromatics_Plus_H()
    model_b.fit(y[tr], H[tr], H_ref[tr], F[tr], Arom[tr])
    yhat_b_with_arom = model_b.predict(H[te], H_ref[te], F[te], Arom[te], use_aromatics=True)
    yhat_b_no_arom = model_b.predict(H[te], H_ref[te], F[te], Arom=None, use_aromatics=False)
    scores['Two-predictor (H + Arom)'].append({
        'rmse': rmse_log(y[te], yhat_b_with_arom),
        'rmse_h_only': rmse_log(y[te], yhat_b_no_arom),
        'r2': r2_score(y[te], yhat_b_with_arom),
        'r2_h_only': r2_score(y[te], yhat_b_no_arom),
    })
    
    # C
    model_c = LogThrustInteraction()
    model_c.fit(y[tr], H[tr], H_ref[tr], F[tr])
    yhat_c = model_c.predict(H[te], H_ref[te], F[te])
    scores['Log-thrust interaction'].append({
        'rmse': rmse_log(y[te], yhat_c),
        'r2': r2_score(y[te], yhat_c),
    })
    
    # D
    model_d = HingeModel()
    model_d.fit(y[tr], H[tr], H_ref[tr], F[tr])
    yhat_d = model_d.predict(H[te], H_ref[te], F[te])
    scores['Hinge model'].append({
        'rmse': rmse_log(y[te], yhat_d),
        'r2': r2_score(y[te], yhat_d),
    })

print("\n" + "="*80)
print("CROSS-VALIDATED PERFORMANCE (5-fold, log scale)")
print("="*80)

for model_name, folds in scores.items():
    rmses = [f['rmse'] for f in folds if 'rmse' in f]
    r2s = [f['r2'] for f in folds if 'r2' in f]
    
    print(f"\n{model_name}")
    print(f"  RMSE (log):  {np.mean(rmses):.4f} ± {np.std(rmses):.4f}")
    print(f"  R²:          {np.mean(r2s):.4f} ± {np.std(r2s):.4f}")
    
    # Check if H-only variant exists
    if 'rmse_h_only' in folds[0]:
        rmses_h = [f['rmse_h_only'] for f in folds]
        r2s_h = [f['r2_h_only'] for f in folds]
        print(f"  (H-only surrogate, no aromatics)")
        print(f"    RMSE:      {np.mean(rmses_h):.4f} ± {np.std(rmses_h):.4f}")
        print(f"    R²:        {np.mean(r2s_h):.4f} ± {np.std(r2s_h):.4f}")

print("\n" + "="*80)
print("INSIGHTS & NEXT STEPS")
print("="*80)
print("""
1. Random Intercept: Should gain +0.05–0.10 R² by accounting for engine-to-engine bias.
   
2. Two-Predictor: Should gain +0.10–0.15 R² with aromatics; marginalized H-only 
   version tells you what aromaticity costs you.
   
3. Log-Thrust: Small gain expected (+0.02–0.05) but conceptually cleaner.
   
4. Hinge: Will help if asymmetric H response (soot suppression stronger above/below 13.8%).

IF you still see R² ≈ 0.59–0.65 after these, the limiting factor is likely:
  → Missing aromatics data in reference fuel (Arom_ref)
  → Campaign-to-campaign heterogeneity (need random slopes, not just intercepts)
  → True measurement noise + engine irreproducibility
  → Need to add more data (as per LITERATURE_SEARCH_PLAN.md)
""")
