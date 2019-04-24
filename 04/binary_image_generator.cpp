#include <iostream>
#include <random>
#include <stdio.h>
#include <fstream>
#include <string>
#include <cmath>

#define SIZE 512

using namespace std;

int matrix[SIZE][SIZE];
int matrix_copy[SIZE][SIZE];
double matrix_energy[SIZE][SIZE];
double current_sum_energy = 0;

void initialize_matrix(double delta){
	
	random_device rd;
	mt19937 gen(rd());
	uniform_real_distribution<double> dis(0.0, 1.0);
	
	for(int i = 0; i < SIZE; i++){
		for(int j = 0; j < SIZE; j++){
			if(dis(gen) < delta)
				matrix[i][j] = 1;
			else
				matrix[i][j] = 0;
		}
	}
}

void store_matrix(){
	for(int i = 0; i < SIZE; i++){
		for(int j = 0; j < SIZE; j++){
			matrix_copy[i][j] = matrix[i][j];
		}
	}
}

void restore_matrix(){
	for(int i = 0; i < SIZE; i++){
		for(int j = 0; j < SIZE; j++){
			matrix[i][j] = matrix_copy[i][j];
		}
	}
}


void print_matrix(){
	int ones = 0;
	int zeros = 0;
	for(int i = 0; i < SIZE; i++){
		for(int j = 0; j < SIZE; j++){
			printf("%d ", matrix[i][j]);
			if(matrix[i][j])
				ones++;
			else
				zeros++;
		}
		printf("\n");
	}
}

void print_energy_matrix(){

	for(int i = 0; i < SIZE; i++){
		for(int j = 0; j < SIZE; j++){
			printf("%lf ", matrix_energy[i][j]);
		}
		printf("\n");
	}
}

void save_matrix_to_file(string file_name){
	ofstream text_file;
	text_file.open(file_name);

	for(int i = 0; i < SIZE; i++){
		for(int j = 0; j < SIZE; j++){
			if(matrix[i][j])
				text_file << "255 ";
			else
				text_file << "0 ";
		}
		text_file << "\n";
	}
	
	text_file.close();
}

double matrix_energy_update(double (*f)(int, int)){
	double sum_energy = 0;
	
	for(int i = 0; i < SIZE; i++){
		for(int j = 0; j < SIZE; j++){
			if(matrix[i][j]){
				sum_energy += f(i,j);
				matrix_energy[i][j] = f(i,j);
			}
			else{
				matrix_energy[i][j] = 0;
			}
		}
	}
	
	current_sum_energy = sum_energy;
	
	return sum_energy;
}

double energy_4_neighbours(int x, int y){
	double energy = 0;
	if(matrix[x][y]){
		if(matrix[(SIZE + x-1)%SIZE][y]) energy +=1;
		if(matrix[x][(SIZE + y-1)%SIZE]) energy +=1;
		if(matrix[(x+1)%SIZE][y]) energy +=1;
		if(matrix[x][(y+1)%SIZE]) energy +=1;	
	}	
	return energy;
}

//00#0
//###0
//##X0
//0000
double energy_3_neighbours_left(int x, int y){
	double energy = 0;
	if(matrix[x][y]){
		if(matrix[(SIZE + x-1)%SIZE][(SIZE + y-1)%SIZE]) energy +=1;
		if(matrix[x][(SIZE + y-1)%SIZE]) energy +=1;
		if(matrix[(SIZE + x-1)%SIZE][y]) energy +=1;
	}	
	return energy;
}

double energy_16_neighbours(int x, int y){
	double energy = 0;
	if(matrix[x][y]){
		for(int i = -2; i < 2; i++){
			for(int j = -2; j < 2; j++){
				if(abs(i) == 2 || abs(j) == 2){
					if(matrix[(SIZE + x + i)%SIZE][(SIZE + y + j)%SIZE]) energy -=1;
				}
				else if(abs(i) == 1 || abs(j) == 1){
					if(matrix[(SIZE + x + i)%SIZE][(SIZE + y + j)%SIZE]) energy +=1;
				}
			}
		}
	}	
	return energy;
}

double energy_16_neighbours_neg(int x, int y){
	double energy = 0;
	if(matrix[x][y]){
		for(int i = -2; i < 2; i++){
			for(int j = -2; j < 2; j++){
				if(abs(i) == 2 || abs(j) == 2){
					if(matrix[(SIZE + x + i)%SIZE][(SIZE + y + j)%SIZE]) energy +=1;
				}
				else if(abs(i) == 1 || abs(j) == 1){
					if(matrix[(SIZE + x + i)%SIZE][(SIZE + y + j)%SIZE]) energy -=1;
				}
			}
		}
	}	
	return energy;
}


double energy_16_neighbours_mix(int x, int y){
	double energy = 0;
	if(matrix[x][y]){
		for(int i = -2; i < 2; i++){
			for(int j = -2; j < 2; j++){
				if(abs(i) == 2 || abs(j) == 1){
					if(matrix[(SIZE + x + i)%SIZE][(SIZE + y + j)%SIZE]) energy +=1;
				}
				else if(abs(i) == 1 || abs(j) == 2){
					if(matrix[(SIZE + x + i)%SIZE][(SIZE + y + j)%SIZE]) energy -=1;
				}
			}
		}
	}	
	return energy;
}


//0#0
//0#0
//0#0
//0X0
//0#0
//0#0
//0#0
double energy_vertical_neighbours(int x, int y){
	double energy = 0;
	if(matrix[x][y]){
		
		for(int i = -3; i < 3; i++){
			if(i !=0 ){
				if(matrix[(SIZE + x+ i)%SIZE][y]) energy +=1;
			}
		}
	}	
	return -energy;
}


double energy_negative_8_neighbours(int x, int y){
	double energy = 0;
	double count = 0;
	if(matrix[x][y]){
		for(int i = -2; i < 2; i++){
			for(int j = -2; j < 2; j++)
			if(i != 0 || j != 0){
				if(matrix[(SIZE + x+ i)%SIZE][(SIZE + y+ j)%SIZE]) count +=1;
			}
		}
	}
	energy = -count;
	return energy;
}


double energy_negative_8_neighbours_border(int x, int y){
	double energy = 0;
	double count = 0;
	if(matrix[x][y]){
		for(int i = -2; i < 2; i++){
			for(int j = -2; j < 2; j++)
			if((i != 0 || j != 0) && (x+i < SIZE) && (x+i >= 0) && (y+j < SIZE) && (y+j >= 0)){
				if(matrix[(SIZE + x+ i)%SIZE][(SIZE + y+ j)%SIZE]) count +=1;
			}
		}
	}
	energy = -count;
	return energy;
}


double swap_pixels_update_energy(int x1, int y1, int x2, int y2, int scope, double (*f)(int, int)){
	//scope - the maximal distance from given pixel (in any direction up/down/left/right)
	//		  within which energies of other pixels can be affected
	
	swap(matrix[x1][y1], matrix[x2][y2]);

	for(int i = -scope; i<scope; i++){
		for(int j = -scope; j<scope; j++){
			current_sum_energy -= matrix_energy[(SIZE + i + x1)%SIZE][(SIZE + j + y1)%SIZE];
			double pixel_energy = f((SIZE + i + x1)%SIZE, (SIZE + j + y1)%SIZE);
			matrix_energy[(SIZE + i + x1)%SIZE][(SIZE + j + y1)%SIZE] = pixel_energy;
			current_sum_energy += pixel_energy;
			
		}
	}
	
	for(int i = -scope; i<scope; i++){
		for(int j = -scope; j<scope; j++){
			current_sum_energy -= matrix_energy[(SIZE + i + x2)%SIZE][(SIZE + j + y2)%SIZE];
			double pixel_energy = f((SIZE + i + x2)%SIZE, (SIZE + j + y2)%SIZE);
			matrix_energy[(SIZE + i + x2)%SIZE][(SIZE + j + y2)%SIZE] = pixel_energy;
			current_sum_energy += pixel_energy;			
		}
	}
	
	return current_sum_energy;
}

pair<int,int> find_random_white(){
	random_device rd;
	mt19937 gen(rd());
	uniform_int_distribution<> dis(0, SIZE-1);
	
	pair<int, int> xy;
	xy.first = dis(gen);
	xy.second = dis(gen);
	
	while(matrix[xy.first][xy.second]){
		xy.first = dis(gen);
		xy.second = dis(gen);
	}
	
	return xy;
}

pair<int,int> find_random_black(){
	random_device rd;
	mt19937 gen(rd());
	uniform_int_distribution<> dis(0, SIZE-1);
	
	pair<int, int> xy;
	xy.first = dis(gen);
	xy.second = dis(gen);
	
	while(!matrix[xy.first][xy.second]){
		xy.first = dis(gen);
		xy.second = dis(gen);
	}
	
	return xy;
}


int simulated_annealing(int iterations, double T, double k, int interval, string energy_log, string temp_log, double (*f)(int, int), int scope){
	
	random_device rd;
	mt19937 gen(rd());
	uniform_real_distribution<double> dis(0.0, 1.0);
	
	ofstream energy_log_file;
	energy_log_file.open(energy_log);
	
	ofstream temp_log_file;
	if(temp_log != ""){
		temp_log_file.open(temp_log);
	}
	
	for(int i =0; i< iterations; i++){
		double old_energy = current_sum_energy;
		pair<int, int> xy_white = find_random_white();
		pair<int, int> xy_black = find_random_black();
		
		swap_pixels_update_energy(xy_white.first, xy_white.second, xy_black.first, xy_black.second, scope, f);
		
		//if(current_sum_energy > old_energy && dis(gen) > T){
		if(current_sum_energy > old_energy && dis(gen) > exp(-abs(current_sum_energy-old_energy)/T)){
			swap_pixels_update_energy(xy_white.first, xy_white.second, xy_black.first, xy_black.second, scope, f);
		}
		
		if(i%interval == 0){
			T *= k;
		}
		if( i % 100 == 0)
			energy_log_file << i << " " << current_sum_energy << "\n";
		if(temp_log != "" && i%100 == 0){
			temp_log_file  << i << " " << T << "\n";
		}
		
	}
	energy_log_file.close();
	
	if(temp_log != ""){
		temp_log_file.close();
	}
	return iterations;
}


int main(){

	initialize_matrix(0.5);
	matrix_energy_update(energy_4_neighbours);

	printf("%lf\n", current_sum_energy);
	save_matrix_to_file("d=0.5_init.txt");
	store_matrix();
	simulated_annealing(2000000, 15, 0.99995, 20, "d=0.5_4_neigh_normal_energy.txt", "d=0.5_4_neigh_normal_temp.txt",energy_4_neighbours, 1);
	save_matrix_to_file("d=0.5_4_neigh_normal_result.txt");
	
	restore_matrix();
	matrix_energy_update(energy_4_neighbours);

	//printf("%lf\n", current_sum_energy);
	simulated_annealing(2000000, 15, 0.85, 20, "d=0.5_4_neigh_fast_energy.txt", "d=0.5_4_neigh_fast_temp.txt",energy_4_neighbours, 1);

	save_matrix_to_file("d=0.5_4_neigh_fast_result.txt");
	
	
	initialize_matrix(0.4);
	matrix_energy_update(energy_negative_8_neighbours);
	simulated_annealing(500000, 15, 0.995, 20, "d=0.4_8_neigh_energy.txt", "",energy_negative_8_neighbours, 1);
	save_matrix_to_file("d=0.4_8_neigh_result.txt");
	

	initialize_matrix(0.5);
	matrix_energy_update(energy_vertical_neighbours);
	simulated_annealing(400000, 15, 0.995, 20, "d=0.5_vertical_neigh_energy.txt", "",energy_vertical_neighbours, 3);
	save_matrix_to_file("d=0.5_vertical_neigh_result.txt");
	
	
	initialize_matrix(0.5);
	matrix_energy_update(energy_3_neighbours_left);
	simulated_annealing(400000, 15, 0.995, 20, "d=0.5_3_left_neigh_energy.txt", "",energy_3_neighbours_left, 1);
	save_matrix_to_file("d=0.5_3_left_neigh_result.txt");
	
	
	initialize_matrix(0.5);
	matrix_energy_update(energy_16_neighbours);
	simulated_annealing(400000, 15, 0.995, 20, "d=0.5_16_neigh_energy.txt", "",energy_16_neighbours, 2);
	save_matrix_to_file("d=0.5_16_neigh_result.txt");
	
	
	initialize_matrix(0.6);
	matrix_energy_update(energy_16_neighbours_neg);
	simulated_annealing(400000, 15, 0.995, 20, "d=0.6_16_neg_neigh_energy.txt", "",energy_16_neighbours_neg, 2);
	save_matrix_to_file("d=0.6_16_neg_neigh_result.txt");
	
	
	initialize_matrix(0.6);
	matrix_energy_update(energy_16_neighbours_mix);
	simulated_annealing(400000, 15, 0.995, 20, "d=0.6_16_mix_neigh_energy.txt", "",energy_16_neighbours_mix, 2);
	save_matrix_to_file("d=0.6_16_mix_neigh_result.txt");
	
	
	initialize_matrix(0.6);
	matrix_energy_update(energy_negative_8_neighbours_border);
	simulated_annealing(1000000, 15, 0.995, 20, "d=0.6_8_neigh_border_energy.txt", "",energy_negative_8_neighbours_border, 1);
	save_matrix_to_file("d=0.6_8_neigh_border_result.txt");
	
}
