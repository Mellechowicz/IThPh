#include <stdio.h>
#include <stdlib.h>

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

float dvdt(float t, float v){
	return 0.0;
}

// --- 1D Functions ---

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

// --- 2D Structures and Functions ---

typedef struct {
  float x;
  float y;
} Vector2D;

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

// --- 3D Structures and Functions ---

typedef struct {
  float x;
  float y;
  float z;
} Vector3D;

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

