#include <stdio.h>
#include <stdlib.h>
// const float one_sixth  = 0x1.555556p-3f; // float 1/6
// const double one_sixth = 0x1.5555555555555p-3; // double 1/6
float RK4(float f, float x, float dt, float(*dfdx)(float,float)){
	const float one_sixth = 0x1.555556p-3f;
	float k1 = dfdx(x,f);
	float k2 = dfdx(x+0.5*dt,f+0.5*dt*k1);
	float k3 = dfdx(x+0.5*dt,f+0.5*dt*k2);
	float k4 = dfdx(x+dt,f+dt*k3);
	return one_sixth*(k1+2*k2+2*k3+k4);
}

float dxdt(float t, float x){
	return -1e-3*x;
}

float dvdt(float t, float x){
	return 0.0;
}


/* --- 1D Functions ---
                                                                                          
   ▄▄▄     ▄▄▄▄▄                                                                          
  █▀██     ██▀▀▀██                                             ██                         
    ██     ██    ██            ▄▄█████▄  ▀██  ███  ▄▄█████▄  ███████    ▄████▄   ████▄██▄ 
    ██     ██    ██            ██▄▄▄▄ ▀   ██▄ ██   ██▄▄▄▄ ▀    ██      ██▄▄▄▄██  ██ ██ ██ 
    ██     ██    ██             ▀▀▀▀██▄    ████▀    ▀▀▀▀██▄    ██      ██▀▀▀▀▀▀  ██ ██ ██ 
 ▄▄▄██▄▄▄  ██▄▄▄██             █▄▄▄▄▄██     ███    █▄▄▄▄▄██    ██▄▄▄   ▀██▄▄▄▄█  ██ ██ ██ 
 ▀▀▀▀▀▀▀▀  ▀▀▀▀▀                ▀▀▀▀▀▀      ██      ▀▀▀▀▀▀      ▀▀▀▀     ▀▀▀▀▀   ▀▀ ▀▀ ▀▀ 
                                          ███                                             
                                                                                          
 */
void RK4_1D(float* x, float* v, float* dx, float* dv, float t, float dt,
	    float(*dfdx)(float*,float*,float*,float*,float,size_t), size_t N){
	/* RK4 Implementation in 1D
	 * x = position array
	 * v = velocity array
	 * dx = derivative of position array
	 * dv = derivative of velocity array
	 * t = current time
	 * dt = time step
	 * dfdx = function that computes derivatives
	 * arguments of dfdx: (x, v, dx, dv, t, N)
	 * N = number of elements
	 */

	// Temporary arrays	
	const float one_sixth = 0x1.555556p-3f;
	size_t size = N * sizeof(float);
	float* tmp_x = malloc(size);
	float* tmp_v = malloc(size);

	// k1, k2, k3, k4 arrays for position and velocity
	float* k1_dx = malloc(size); float* k1_dv = malloc(size);
	float* k2_dx = malloc(size); float* k2_dv = malloc(size);
	float* k3_dx = malloc(size); float* k3_dv = malloc(size);
	float* k4_dx = malloc(size); float* k4_dv = malloc(size);

	// Calculate k1, k2, k3, k4
	dfdx(x,v,k1_dx,k1_dv,t,N);
	for(size_t i=0U; i<N; ++i){
		tmp_x[i] = x[i] + 0.5f * dt * k1_dx[i];
		tmp_v[i] = v[i] + 0.5f * dt * k1_dv[i];
	}
	dfdx(tmp_x,tmp_v,k2_dx,k2_dv,t+0.5f*dt,N);
	for(size_t i=0U; i<N; ++i){
		tmp_x[i] = x[i] + 0.5f * dt * k2_dx[i];
		tmp_v[i] = v[i] + 0.5f * dt * k2_dv[i];
	}
	dfdx(tmp_x,tmp_v,k3_dx,k3_dv,t+0.5f*dt,N);
	for(size_t i=0U; i<N; ++i){
		tmp_x[i] = x[i] + dt * k3_dx[i];
		tmp_v[i] = v[i] + dt * k3_dv[i];
	}
	dfdx(tmp_x,tmp_v,k4_dx,k4_dv,t+dt,N);

	// Combine to get final dx and dv
	for(size_t i=0U; i<N; ++i){
		dx[i] = one_sixth * (k1_dx[i] + 2.0f * k2_dx[i] + 2.0f * k3_dx[i] + k4_dx[i]);
		dv[i] = one_sixth * (k1_dv[i] + 2.0f * k2_dv[i] + 2.0f * k3_dv[i] + k4_dv[i]);
	}

	// Cleanup
	free(tmp_x); free(tmp_v);
	free(k1_dx); free(k1_dv);
	free(k2_dx); free(k2_dv);
	free(k3_dx); free(k3_dv);
	free(k4_dx); free(k4_dv);
	return;
}

/*
 * Calculates the next 1D coordinates and velocities
 */
void next_1D(float* coord, float* vel, float* new_coord, float* new_vel, float dt, size_t N){
	/* Calculating new coordinates */
	for(size_t i=0U; i<N; ++i){
		new_coord[i] = coord[i] + RK4(coord[i],vel[i],dt,&dvdt);
		new_vel[i] = vel[i] + RK4(coord[i],vel[i],dt,&dvdt);
	}
	return;
}


/* --- 2D Structures and Functions ---
                                                                                          
  ▄▄▄▄▄    ▄▄▄▄▄                                                                          
 █▀▀▀▀██▄  ██▀▀▀██                                             ██                         
       ██  ██    ██            ▄▄█████▄  ▀██  ███  ▄▄█████▄  ███████    ▄████▄   ████▄██▄ 
     ▄█▀   ██    ██            ██▄▄▄▄ ▀   ██▄ ██   ██▄▄▄▄ ▀    ██      ██▄▄▄▄██  ██ ██ ██ 
   ▄█▀     ██    ██             ▀▀▀▀██▄    ████▀    ▀▀▀▀██▄    ██      ██▀▀▀▀▀▀  ██ ██ ██ 
 ▄██▄▄▄▄▄  ██▄▄▄██             █▄▄▄▄▄██     ███    █▄▄▄▄▄██    ██▄▄▄   ▀██▄▄▄▄█  ██ ██ ██ 
 ▀▀▀▀▀▀▀▀  ▀▀▀▀▀                ▀▀▀▀▀▀      ██      ▀▀▀▀▀▀      ▀▀▀▀     ▀▀▀▀▀   ▀▀ ▀▀ ▀▀ 
                                          ███                                             
                                                                                          
*/
typedef struct {
	float x;
	float y;
} Vector2D;

void RK4_2D(Vector2D* x, Vector2D* v, Vector2D* dx, Vector2D* dv, float t, float dt, float(*dfdx)(Vector2D*,Vector2D*,Vector2D*,Vector2D*,float,size_t), size_t N){
	/* RK4 Implementation in 1D
	 * x = position array
	 * v = velocity array
	 * dx = derivative of position array
	 * dv = derivative of velocity array
	 * t = current time
	 * dt = time step
	 * dfdx = function that computes derivatives
	 * arguments of dfdx: (x, v, dx, dv, t, N)
	 * N = number of elements
	 */

	// Temporary arrays
	const float one_sixth = 0x1.555556p-3f;
	size_t size = N * sizeof(Vector2D);
	Vector2D* tmp_x = malloc(size);
	Vector2D* tmp_v = malloc(size);

	// k1, k2, k3, k4 arrays for position and velocity
	Vector2D* k1_dx = malloc(size); Vector2D* k1_dv = malloc(size);
	Vector2D* k2_dx = malloc(size); Vector2D* k2_dv = malloc(size);
	Vector2D* k3_dx = malloc(size); Vector2D* k3_dv = malloc(size);
	Vector2D* k4_dx = malloc(size); Vector2D* k4_dv = malloc(size);

	// Calculate k1, k2, k3, k4
	dfdx(x,v,k1_dx,k1_dv,t,N);
	for(size_t i=0U; i<N; ++i){
		tmp_x[i].x = x[i].x + 0.5f * dt * k1_dx[i].x;
		tmp_x[i].y = x[i].y + 0.5f * dt * k1_dx[i].y;
		tmp_v[i].x = v[i].x + 0.5f * dt * k1_dv[i].x;
		tmp_v[i].y = v[i].y + 0.5f * dt * k1_dv[i].y;
	}
	dfdx(tmp_x,tmp_v,k2_dx,k2_dv,t+0.5f*dt,N);
	for(size_t i=0U; i<N; ++i){
		tmp_x[i].x = x[i].x + 0.5f * dt * k2_dx[i].x;
		tmp_x[i].y = x[i].y + 0.5f * dt * k2_dx[i].y;
		tmp_v[i].x = v[i].x + 0.5f * dt * k2_dv[i].x;
		tmp_v[i].y = v[i].y + 0.5f * dt * k2_dv[i].y;
	}
	dfdx(tmp_x,tmp_v,k3_dx,k3_dv,t+0.5f*dt,N);
	for(size_t i=0U; i<N; ++i){
		tmp_x[i].x = x[i].x + dt * k3_dx[i].x;
		tmp_x[i].y = x[i].y + dt * k3_dx[i].y;
		tmp_v[i].x = v[i].x + dt * k3_dv[i].x;
		tmp_v[i].y = v[i].y + dt * k3_dv[i].y;
	}
	dfdx(tmp_x,tmp_v,k4_dx,k4_dv,t+dt,N);

	// Combine to get final dx and dv
	for(size_t i=0U; i<N; ++i){
		dx[i].x = one_sixth * (k1_dx[i].x + 2.0f * k2_dx[i].x + 2.0f * k3_dx[i].x + k4_dx[i].x);
		dx[i].y = one_sixth * (k1_dx[i].y + 2.0f * k2_dx[i].y + 2.0f * k3_dx[i].y + k4_dx[i].y);
		dv[i].x = one_sixth * (k1_dv[i].x + 2.0f * k2_dv[i].x + 2.0f * k3_dv[i].x + k4_dv[i].x);
		dv[i].y = one_sixth * (k1_dv[i].y + 2.0f * k2_dv[i].y + 2.0f * k3_dv[i].y + k4_dv[i].y);
	}

	// Cleanup
	free(tmp_x); free(tmp_v);
	free(k1_dx); free(k1_dv);
	free(k2_dx); free(k2_dv);
	free(k3_dx); free(k3_dv);
	free(k4_dx); free(k4_dv);
	return;
}


/*
 * Calculates the next 2D coordinates and velocities
 */

void next_2D(Vector2D* coord, Vector2D* vel, Vector2D* new_coord, Vector2D* new_vel, float dt, size_t N){
	/* Calculating new coordinates */
	for(size_t i=0U; i<N; ++i){
		new_coord[i].x = coord[i].x + RK4(coord[i].x,vel[i].x,dt,&dxdt);
		new_coord[i].y = coord[i].y + RK4(coord[i].y,vel[i].y,dt,&dxdt);

		new_vel[i].x = vel[i].x + RK4(coord[i].x,vel[i].x,dt,&dvdt);
		new_vel[i].y = vel[i].y + RK4(coord[i].y,vel[i].y,dt,&dvdt);
	}
	return;
}

/* --- 3D Structures and Functions ---
                                                                                          
  ▄▄▄▄▄    ▄▄▄▄▄                                                                          
 █▀▀▀▀██▄  ██▀▀▀██                                             ██                         
      ▄██  ██    ██            ▄▄█████▄  ▀██  ███  ▄▄█████▄  ███████    ▄████▄   ████▄██▄ 
   █████   ██    ██            ██▄▄▄▄ ▀   ██▄ ██   ██▄▄▄▄ ▀    ██      ██▄▄▄▄██  ██ ██ ██ 
      ▀██  ██    ██             ▀▀▀▀██▄    ████▀    ▀▀▀▀██▄    ██      ██▀▀▀▀▀▀  ██ ██ ██ 
 █▄▄▄▄██▀  ██▄▄▄██             █▄▄▄▄▄██     ███    █▄▄▄▄▄██    ██▄▄▄   ▀██▄▄▄▄█  ██ ██ ██ 
  ▀▀▀▀▀    ▀▀▀▀▀                ▀▀▀▀▀▀      ██      ▀▀▀▀▀▀      ▀▀▀▀     ▀▀▀▀▀   ▀▀ ▀▀ ▀▀ 
                                          ███                                             
*/

typedef struct {
	float x;
	float y;
	float z;
} Vector3D;


void RK4_3D(Vector3D* x, Vector3D* v, Vector3D* dx, Vector3D* dv, float t, float dt, float(*dfdx)(Vector3D*,Vector3D*,Vector3D*,Vector3D*,float,size_t), size_t N){
	/* RK4 Implementation in 1D
	 * x = position array
	 * v = velocity array
	 * dx = derivative of position array
	 * dv = derivative of velocity array
	 * t = current time
	 * dt = time step
	 * dfdx = function that computes derivatives
	 * arguments of dfdx: (x, v, dx, dv, t, N)
	 * N = number of elements
	 */

	// Temporary arrays
	const float one_sixth = 0x1.555556p-3f;
	size_t size = N * sizeof(Vector3D);
	Vector3D* tmp_x = malloc(size);
	Vector3D* tmp_v = malloc(size);

	// k1, k2, k3, k4 arrays for position and velocity
	Vector3D* k1_dx = malloc(size); Vector3D* k1_dv = malloc(size);
	Vector3D* k2_dx = malloc(size); Vector3D* k2_dv = malloc(size);
	Vector3D* k3_dx = malloc(size); Vector3D* k3_dv = malloc(size);
	Vector3D* k4_dx = malloc(size); Vector3D* k4_dv = malloc(size);

	// Calculate k1, k2, k3, k4
	dfdx(x,v,k1_dx,k1_dv,t,N);
	for(size_t i=0U; i<N; ++i){
		tmp_x[i].x = x[i].x + 0.5f * dt * k1_dx[i].x;
		tmp_x[i].y = x[i].y + 0.5f * dt * k1_dx[i].y;
		tmp_x[i].z = x[i].z + 0.5f * dt * k1_dx[i].z;
		tmp_v[i].x = v[i].x + 0.5f * dt * k1_dv[i].x;
		tmp_v[i].y = v[i].y + 0.5f * dt * k1_dv[i].y;
		tmp_v[i].z = v[i].z + 0.5f * dt * k1_dv[i].z;
	}
	dfdx(tmp_x,tmp_v,k2_dx,k2_dv,t+0.5f*dt,N);
	for(size_t i=0U; i<N; ++i){
		tmp_x[i].x = x[i].x + 0.5f * dt * k2_dx[i].x;
		tmp_x[i].y = x[i].y + 0.5f * dt * k2_dx[i].y;
		tmp_x[i].z = x[i].z + 0.5f * dt * k2_dx[i].z;
		tmp_v[i].x = v[i].x + 0.5f * dt * k2_dv[i].x;
		tmp_v[i].y = v[i].y + 0.5f * dt * k2_dv[i].y;
		tmp_v[i].z = v[i].z + 0.5f * dt * k2_dv[i].z;
	}
	dfdx(tmp_x,tmp_v,k3_dx,k3_dv,t+0.5f*dt,N);
	for(size_t i=0U; i<N; ++i){
		tmp_x[i].x = x[i].x + dt * k3_dx[i].x;
		tmp_x[i].y = x[i].y + dt * k3_dx[i].y;
		tmp_x[i].z = x[i].z + dt * k3_dx[i].z;
		tmp_v[i].x = v[i].x + dt * k3_dv[i].x;
		tmp_v[i].y = v[i].y + dt * k3_dv[i].y;
		tmp_v[i].z = v[i].z + dt * k3_dv[i].z;
	}
	dfdx(tmp_x,tmp_v,k4_dx,k4_dv,t+dt,N);

	// Combine to get final dx and dv
	for(size_t i=0U; i<N; ++i){
		dx[i].x = one_sixth * (k1_dx[i].x + 2.0f * k2_dx[i].x + 2.0f * k3_dx[i].x + k4_dx[i].x);
		dx[i].y = one_sixth * (k1_dx[i].y + 2.0f * k2_dx[i].y + 2.0f * k3_dx[i].y + k4_dx[i].y);
		dx[i].z = one_sixth * (k1_dx[i].z + 2.0f * k2_dx[i].z + 2.0f * k3_dx[i].z + k4_dx[i].z);
		dv[i].x = one_sixth * (k1_dv[i].x + 2.0f * k2_dv[i].x + 2.0f * k3_dv[i].x + k4_dv[i].x);
		dv[i].y = one_sixth * (k1_dv[i].y + 2.0f * k2_dv[i].y + 2.0f * k3_dv[i].y + k4_dv[i].y);
		dv[i].z = one_sixth * (k1_dv[i].z + 2.0f * k2_dv[i].z + 2.0f * k3_dv[i].z + k4_dv[i].z);
	}

	// Cleanup
	free(tmp_x); free(tmp_v);
	free(k1_dx); free(k1_dv);
	free(k2_dx); free(k2_dv);
	free(k3_dx); free(k3_dv);
	free(k4_dx); free(k4_dv);
	return;
}


/*
 * Calculates the next 2D coordinates and velocities
 */

void next_3D(Vector3D* coord, Vector3D* vel, Vector3D* new_coord, Vector3D* new_vel, float dt, size_t N){
	/* Calculating new coordinates */
	for(size_t i=0U; i<N; ++i){
		new_coord[i].x = coord[i].x + RK4(coord[i].x,vel[i].x,dt,&dxdt);
		new_coord[i].y = coord[i].y + RK4(coord[i].y,vel[i].y,dt,&dxdt);
		new_coord[i].z = coord[i].z + RK4(coord[i].z,vel[i].z,dt,&dxdt);

		new_vel[i].x = vel[i].x + RK4(coord[i].x,vel[i].x,dt,&dvdt);
		new_vel[i].y = vel[i].y + RK4(coord[i].y,vel[i].y,dt,&dvdt);
		new_vel[i].z = vel[i].z + RK4(coord[i].z,vel[i].z,dt,&dvdt);
	}
	return;
}

