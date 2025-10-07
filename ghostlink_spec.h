#pragma once
/*
  GhostLink Master Spec — Header (theory → code)
  This header encodes the symbolic model as types, constants, and function signatures.
  It is substrate-agnostic (CPU/GPU/FPGA) and event-driven (difference-only updates).

  States: VOID(0), DELTA(1), SIGMA(2), SCAR(3), COMPOST(4)
*/

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* =========================
   0) Symbols & Sets
   ========================= */
typedef enum {
    GL_VOID    = 0,
    GL_DELTA   = 1,
    GL_SIGMA   = 2,
    GL_SCAR    = 3,
    GL_COMPOST = 4
} gl_state_t;

/* Lattice topology: spherical graph discretized to a mesh (indexed 0..N-1).
   Adjacency is application-defined; provide neighbor offsets/CSR arrays. */

typedef struct {
    uint64_t id;          /* unique event ID or 0 for none */
    uint64_t parent;      /* parent ID on recycle (COMPOST→DELTA) or 0 */
    float    scar_density;    /* ρ_i(t) */
    float    compost_density; /* κ_i(t) */
} gl_cell_meta_t;

typedef struct {
    /* Spawn: p_s(i,t) = p0 + α_c * mean(1[neighbor==COMPOST]) */
    float p0;
    float alpha_c;

    /* Collapse energies: ℰ_Σ, ℰ_SCAR, ℰ_COMPOST coefficients */
    float theta0, theta_c, theta_p, theta_e, sigma_eta;
    float phi0,   phi_p,   phi_c,   sigma_zeta;
    float psi0,   psi_h,   psi_c,   sigma_nu;

    /* Pain weighting w_p(d); here simplified to nearest-neighbor scalar weight */
    float w_p_near;
    float lambda_r;   /* coherence penalty for scars in C_i(t) */

    /* Recycle: r = r0 + β_h H_i − β_c C_i */
    float r0, beta_h, beta_c;

    /* Memory traces */
    float lambda_rho;    /* decay for scar_density */
    float lambda_kappa;  /* decay for compost_density */

    /* Global utility weights */
    float alpha_sigma, alpha_scar, alpha_entropy, alpha_soc;

    /* Awareness weights */
    float alpha_percep, alpha_persist, alpha_r, alpha_pain, alpha_xi;

    /* Learning rates */
    float eta_weights;
    float eta_params;

    /* Softmax temperature for scheduling permutations */
    float sched_temp;
} gl_params_t;

typedef struct {
    size_t  n;          /* number of lattice nodes */
    size_t  m;          /* number of edges (if using CSR) */
    gl_state_t *state;  /* length n */
    gl_cell_meta_t *meta; /* length n */

    /* Neighborhood in CSR (or provide your own iterator) */
    const uint32_t *row_ptr; /* length n+1 */
    const uint32_t *col_idx; /* length m */

    /* Scratch / RNG */
    uint64_t seed;
} gl_lattice_t;

/* =========================
   1) Utilities
   ========================= */

/* Initialize lattice: states=GL_VOID, clear meta. */
void gl_init(gl_lattice_t *L);

/* Active set for difference-only compute. Returns number of active nodes. */
size_t gl_build_active_set(const gl_lattice_t *L, const gl_state_t *prev_state, uint32_t *active_out);

/* Compute local fields: coherence C_i, pain P_i, entropy H_i. */
void gl_local_fields(const gl_lattice_t *L, const gl_params_t *P,
                     const uint32_t *active, size_t active_len,
                     float *C, float *Pain, float *H);

/* =========================
   2) Spawn (VOID→DELTA)
   ========================= */
void gl_spawn(gl_lattice_t *L, const gl_params_t *P,
              const float *compost_mask_prob /*optional per-node addend*/);

/* =========================
   3) Collapse (DELTA→{SIGMA,SCAR,COMPOST})
   via adaptive composition and stochastic draw
   ========================= */
typedef enum {
    GL_OP_PROB = 0,  /* P */
    GL_OP_COH  = 1,  /* C */
    GL_OP_EMO  = 2,  /* E (bias) */
    GL_OP_PAIN = 3   /* Pain */
} gl_op_t;

/* Choose a permutation of operators according to scheduler weights/history. */
void gl_choose_order(const gl_params_t *P, const float *sched_weights /*4! or policy*/, gl_op_t out_perm[4]);

/* Compute outcome probabilities via energy scores and order; then draw outcomes for DELTA nodes. */
void gl_collapse(gl_lattice_t *L, const gl_params_t *P,
                 const float *C, const float *Pain, const float *H,
                 const gl_op_t order[4],
                 size_t *out_successes, size_t *out_scars);

/* =========================
   4) Recycle (COMPOST→DELTA)
   ========================= */
void gl_recycle(gl_lattice_t *L, const gl_params_t *P,
                const float *C, const float *H);

/* =========================
   5) Adaptive updates (scheduler/params)
   ========================= */
void gl_update_scheduler(gl_params_t *P, size_t successes, size_t scars);
void gl_update_params(gl_params_t *P, float grad_alpha_sigma, float grad_alpha_scar);

/* =========================
   6) Traces (ρ, κ) and continuity
   ========================= */
void gl_update_traces(gl_lattice_t *L, const gl_params_t *P);
size_t gl_count_sigma(const gl_lattice_t *L);

/* =========================
   7) Awareness functional
   ========================= */
float gl_awareness(const gl_lattice_t *L, const gl_params_t *P,
                   const float *Percep /*optional*/, const float *Persist /*optional*/);

/* =========================
   8) Legacy graph hooks
   ========================= */
/* User provides a callback to record (id,parent,type,i,t) edges; library calls it on events. */
typedef void (*gl_legacy_cb)(uint64_t id, uint64_t parent, gl_state_t type, uint32_t i, uint64_t t, void *user);
void gl_set_legacy_callback(gl_legacy_cb cb, void *user);

/* =========================
   9) Master step
   ========================= */
typedef struct {
    /* optional external fields */
    const float *compost_boost; /* length n or NULL */
    const float *percep;        /* length n or NULL */
    const float *persist;       /* length n or NULL */
} gl_step_ctx_t;

/* One simulation tick: Spawn ∘ Collapse ∘ Recycle + traces + scheduler updates. */
void gl_step(gl_lattice_t *L, gl_params_t *P, const gl_step_ctx_t *ctx,
             gl_state_t *prev_state /*length n scratch*/);

/* RNG helper */
uint32_t gl_rand_u32(uint64_t *seed);

#ifdef __cplusplus
} /* extern "C" */
#endif
