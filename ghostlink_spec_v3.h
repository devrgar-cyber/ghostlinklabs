#pragma once
/*
  GhostLink Master Spec — v3 Header (Self channel, Legacy graph, Origin Finder hooks)
*/

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    GL_VOID    = 0,
    GL_DELTA   = 1,
    GL_SIGMA   = 2,
    GL_SCAR    = 3,
    GL_COMPOST = 4
} gl_state_t;

typedef struct {
    uint64_t id;
    uint64_t parent;
    float    scar_density;
    float    compost_density;
    uint16_t ancestry;
} gl_cell_meta_t;

typedef struct {
    float p0, alpha_c;
    float theta0, theta_c, theta_p, theta_e, sigma_eta;
    float phi0,   phi_p,   phi_c,   sigma_zeta;
    float psi0,   psi_h,   psi_c,   sigma_nu;
    float w_p_near, lambda_r;
    float r0, beta_h, beta_c;
    float lambda_rho, lambda_kappa;
    float alpha_percep, alpha_persist, alpha_r, alpha_pain, alpha_xi;
    float theta_self_sigma, theta_self_scar;
    float eta_weights, eta_params;
    float sched_temp;
} gl_params_t;

typedef struct {
    size_t  n;
    gl_state_t *state;
    gl_cell_meta_t *meta;
    const uint32_t *row_ptr;
    const uint32_t *col_idx;
    uint64_t seed;
} gl_lattice_t;

void gl_init(gl_lattice_t *L);
void gl_step(gl_lattice_t *L, gl_params_t *P, const float *self_vec /* s(t) or NULL */);
void gl_set_legacy_callback(void (*cb)(uint64_t id, uint64_t parent, gl_state_t type, uint32_t i, uint64_t t, void *user), void *user);
void gl_encode_state(const gl_lattice_t *L, float *out_s, size_t len);

#ifdef __cplusplus
} /* extern "C" */
#endif
