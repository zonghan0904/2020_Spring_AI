#include "STcpClient.h"
#include <stdlib.h>
#include <iostream>
#include <climits>

#define WIDTH 8
#define HEIGHT 8
#define DEPTH 3


bool Terminal_Test(std::vector<std::vector<int>>& board);

int Utility(std::vector<std::vector<int>>& board, bool is_black);

std::vector<std::vector<int>> Actions(std::vector<std::vector<int>>& board);

int Max_value(std::vector<std::vector<int>>& board, bool is_black, int depth, std::vector<int>& next_pos);

void Make_move(std::vector<std::vector<int>>& board, std::vector<int>& pos, bool is_black);

bool Check_surround(std::vector<std::vector<int>>& board, int x, int y, bool is_black);


/*
	輪到此程式移動棋子
	board : 棋盤狀態(vector of vector), board[i][j] = i row, j column 棋盤狀態(i, j 從 0 開始)
			0 = 空、1 = 黑、2 = 白、-1 = 四個角落
	is_black : True 表示本程式是黑子、False 表示為白子

	return Step
	Step : vector, Step = {r, c}
			r, c 表示要下棋子的座標位置 (row, column) (zero-base)
*/
std::vector<int> GetStep(std::vector<std::vector<int>>& board, bool is_black) {
	/*
	Example:*/
	// TODO
	std::vector<int> step;
	step.resize(2);

	int val = 0;

	std::vector<std::vector<int>> temp(board);
	val = Max_value(temp, is_black, DEPTH, step);

	return step;
}

int main() {
	int id_package;
	std::vector<std::vector<int>> board;
	std::vector<int> step;

	bool is_black;
	while (true) {
		if (GetBoard(id_package, board, is_black))
			break;

		step = GetStep(board, is_black);
		SendStep(id_package, step);
	}
}


bool Terminal_Test(std::vector<std::vector<int>>& board) {
	bool end = true;
	for (std::vector<int> v : board) {
		for (int n : v) {
			if (n == 0) {
				end = false;
				break;
			}
		}
		if (!end) break;
	}
	return end;
}

int Utility(std::vector<std::vector<int>>& board, bool is_black) {
	int black = 0, white = 0;
	for (std::vector<int> v : board) {
		for (int n : v) {
			if (n == 1) black += 1;
			else if (n == 2) white += 1;
		}
	}
	if (is_black) return (black - white);
	else return (white - black);
}

std::vector<std::vector<int>> Actions(std::vector<std::vector<int>>& board, bool is_black) {
	std::vector<std::vector<int>> actions;
	std::vector<int> position;
	position.resize(2);
	bool flip = false;

	for (int i = 0; i < HEIGHT; i++) {
		for (int j = 0; j < WIDTH; j++) {
			if (i == 0 && j == 0) continue;
			if (i == 0 && j == 7) continue;
			if (i == 7 && j == 0) continue;
			if (i == 7 && j == 7) continue;

			if (i < 1 || i > 6 || j < 1 || j > 6) {
				if (board[i][j] == 0) {
					flip = Check_surround(board, j, i, is_black);
					if (flip) {
						position[0] = i;
						position[1] = j;
						actions.push_back(position);
					}
				}
			}
			else if (board[i][j] == 0) {
				position[0] = i;
				position[1] = j;
				actions.push_back(position);
			}
		}

	}

	return actions;
}

int Max_value(std::vector<std::vector<int>>& board, bool is_black, int depth, std::vector<int>& next_pos) {
	if (!depth) return Utility(board, is_black);
	int value = 0;
	int max = INT_MIN;
	std::vector<int> op_pos;
	op_pos.resize(2);

	std::vector<std::vector<int>> actions = Actions(board, is_black);
	for (std::vector<int> pos : actions) {
		std::vector<std::vector<int>> temp(board);
		Make_move(temp, pos, is_black);
		value = -Max_value(temp, !is_black, depth-1, op_pos);
		if (value > max) {
			max = value;
			next_pos = pos;
		}
	}
	return max;
}

void Make_move(std::vector<std::vector<int>>& board, std::vector<int>& pos, bool is_black) {
	bool flip = false;
	int displace;

	if (is_black) {
		board[pos[0]][pos[1]] = 1;

		// left flip
		for (displace = 1; displace < WIDTH; displace++) {
			if (pos[1] - displace < 0) break;
			if (board[pos[0]][pos[1] - displace] == 0 || board[pos[0]][pos[1] - displace] == -1) break;
			if (board[pos[0]][pos[1] - displace] == 1) {
				flip = true;
				break;
			}
		}
		if (flip == true) {
			for (int i = 1; i < displace; i++) {
				board[pos[0]][pos[1] - i] = 1;
			}
			flip = false;
		}

		// right flip
		for (displace = 1; displace < WIDTH; displace++) {
			if (pos[1] + displace > 7) break;
			if (board[pos[0]][pos[1] + displace] == 0 || board[pos[0]][pos[1] + displace] == -1) break;
			if (board[pos[0]][pos[1] + displace] == 1) {
				flip = true;
				break;
			}
		}
		if (flip == true) {
			for (int i = 1; i < displace; i++) {
				board[pos[0]][pos[1] + i] = 1;
			}
			flip = false;
		}

		// upward flip
		for (displace = 1; displace < HEIGHT; displace++) {
			if (pos[0] - displace < 0) break;
			if (board[pos[0] - displace][pos[1]] == 0 || board[pos[0] - displace][pos[1]] == -1) break;
			if (board[pos[0] - displace][pos[1]] == 1) {
				flip = true;
				break;
			}
		}
		if (flip == true) {
			for (int i = 1; i < displace; i++) {
				board[pos[0] - i][pos[1]] = 1;
			}
			flip = false;
		}

		// downward flip
		for (displace = 1; displace < HEIGHT; displace++) {
			if (pos[0] + displace > 7) break;
			if (board[pos[0] + displace][pos[1]] == 0 || board[pos[0] + displace][pos[1]] == -1) break;
			if (board[pos[0] + displace][pos[1]] == 1) {
				flip = true;
				break;
			}
		}
		if (flip == true) {
			for (int i = 1; i < displace; i++) {
				board[pos[0] + i][pos[1]] = 1;
			}
			flip = false;
		}

		// left-up flip
		for (displace = 1; displace < HEIGHT; displace++) {
			if (pos[0] - displace < 0 || pos[1] - displace < 0) break;
			if (board[pos[0] - displace][pos[1] - displace] == 0 || board[pos[0] - displace][pos[1] - displace] == -1) break;
			if (board[pos[0] - displace][pos[1] - displace] == 1) {
				flip = true;
				break;
			}
		}
		if (flip == true) {
			for (int i = 1; i < displace; i++) {
				board[pos[0] - i][pos[1] - i] = 1;
			}
			flip = false;
		}

		// left-down flip
		for (displace = 1; displace < HEIGHT; displace++) {
			if (pos[0] + displace > 7 || pos[1] - displace < 0) break;
			if (board[pos[0] + displace][pos[1] - displace] == 0 || board[pos[0] + displace][pos[1] - displace] == -1) break;
			if (board[pos[0] + displace][pos[1] - displace] == 1) {
				flip = true;
				break;
			}
		}
		if (flip == true) {
			for (int i = 1; i < displace; i++) {
				board[pos[0] + i][pos[1] - i] = 1;
			}
			flip = false;
		}

		// right-up flip
		for (displace = 1; displace < HEIGHT; displace++) {
			if (pos[0] - displace < 0 || pos[1] + displace > 7) break;
			if (board[pos[0] - displace][pos[1] + displace] == 0 || board[pos[0] - displace][pos[1] + displace] == -1) break;
			if (board[pos[0] - displace][pos[1] + displace] == 1) {
				flip = true;
				break;
			}
		}
		if (flip == true) {
			for (int i = 1; i < displace; i++) {
				board[pos[0] - i][pos[1] + i] = 1;
			}
			flip = false;
		}

		// right-down flip
		for (displace = 1; displace < HEIGHT; displace++) {
			if (pos[0] + displace > 7 || pos[1] + displace > 7) break;
			if (board[pos[0] + displace][pos[1] + displace] == 0 || board[pos[0] + displace][pos[1] + displace] == -1) break;
			if (board[pos[0] + displace][pos[1] + displace] == 1) {
				flip = true;
				break;
			}
		}
		if (flip == true) {
			for (int i = 1; i < displace; i++) {
				board[pos[0] + i][pos[1] + i] = 1;
			}
			flip = false;
		}
	}
	else {
		board[pos[0]][pos[1]] = 2;

		// left flip
		for (displace = 1; displace < WIDTH; displace++) {
			if (pos[1] - displace < 0) break;
			if (board[pos[0]][pos[1] - displace] == 0 || board[pos[0]][pos[1] - displace] == -1) break;
			if (board[pos[0]][pos[1] - displace] == 2) {
				flip = true;
				break;
			}
		}
		if (flip == true) {
			for (int i = 1; i < displace; i++) {
				board[pos[0]][pos[1] - i] = 2;
			}
			flip = false;
		}

		// right flip
		for (displace = 1; displace < WIDTH; displace++) {
			if (pos[1] + displace > 7) break;
			if (board[pos[0]][pos[1] + displace] == 0 || board[pos[0]][pos[1] + displace] == -1) break;
			if (board[pos[0]][pos[1] + displace] == 2) {
				flip = true;
				break;
			}
		}
		if (flip == true) {
			for (int i = 1; i < displace; i++) {
				board[pos[0]][pos[1] + i] = 2;
			}
			flip = false;
		}

		// upward flip
		for (displace = 1; displace < HEIGHT; displace++) {
			if (pos[0] - displace < 0) break;
			if (board[pos[0] - displace][pos[1]] == 0 || board[pos[0] - displace][pos[1]] == -1) break;
			if (board[pos[0] - displace][pos[1]] == 2) {
				flip = true;
				break;
			}
		}
		if (flip == true) {
			for (int i = 1; i < displace; i++) {
				board[pos[0] - i][pos[1]] = 2;
			}
			flip = false;
		}

		// downward flip
		for (displace = 1; displace < HEIGHT; displace++) {
			if (pos[0] + displace > 7) break;
			if (board[pos[0] + displace][pos[1]] == 0 || board[pos[0] + displace][pos[1]] == -1) break;
			if (board[pos[0] + displace][pos[1]] == 2) {
				flip = true;
				break;
			}
		}
		if (flip == true) {
			for (int i = 1; i < displace; i++) {
				board[pos[0] + i][pos[1]] = 2;
			}
			flip = false;
		}

		// left-up flip
		for (displace = 1; displace < HEIGHT; displace++) {
			if (pos[0] - displace < 0 || pos[1] - displace < 0) break;
			if (board[pos[0] - displace][pos[1] - displace] == 0 || board[pos[0] - displace][pos[1] - displace] == -1) break;
			if (board[pos[0] - displace][pos[1] - displace] == 2) {
				flip = true;
				break;
			}
		}
		if (flip == true) {
			for (int i = 1; i < displace; i++) {
				board[pos[0] - i][pos[1] - i] = 2;
			}
			flip = false;
		}

		// left-down flip
		for (displace = 1; displace < HEIGHT; displace++) {
			if (pos[0] + displace > 7 || pos[1] - displace < 0) break;
			if (board[pos[0] + displace][pos[1] - displace] == 0 || board[pos[0] + displace][pos[1] - displace] == -1) break;
			if (board[pos[0] + displace][pos[1] - displace] == 2) {
				flip = true;
				break;
			}
		}
		if (flip == true) {
			for (int i = 1; i < displace; i++) {
				board[pos[0] + i][pos[1] - i] = 2;
			}
			flip = false;
		}

		// right-up flip
		for (displace = 1; displace < HEIGHT; displace++) {
			if (pos[0] - displace < 0 || pos[1] + displace > 7) break;
			if (board[pos[0] - displace][pos[1] + displace] == 0 || board[pos[0] - displace][pos[1] + displace] == -1) break;
			if (board[pos[0] - displace][pos[1] + displace] == 2) {
				flip = true;
				break;
			}
		}
		if (flip == true) {
			for (int i = 1; i < displace; i++) {
				board[pos[0] - i][pos[1] + i] = 2;
			}
			flip = false;
		}

		// right-down flip
		for (displace = 1; displace < HEIGHT; displace++) {
			if (pos[0] + displace > 7 || pos[1] + displace > 7) break;
			if (board[pos[0] + displace][pos[1] + displace] == 0 || board[pos[0] + displace][pos[1] + displace] == -1) break;
			if (board[pos[0] + displace][pos[1] + displace] == 2) {
				flip = true;
				break;
			}
		}
		if (flip == true) {
			for (int i = 1; i < displace; i++) {
				board[pos[0] + i][pos[1] + i] = 2;
			}
			flip = false;
		}
	}
}

bool Check_surround(std::vector<std::vector<int>>& board, int x, int y, bool is_black) {
	for (int j = -1; j < 2; j++) {
		for (int i = -1; i < 2; i++) {
			if (j == 0 && i == 0) continue;
			if (y + j < 0 || y + j > 7) continue;
			if (x + i < 0 || x + i > 7) continue;
			
			if (is_black) {
				if (board[y + j][x + i] == 2) {
					for (int mul = 2; mul < WIDTH; mul++) {
						if (y + mul * j < 0 || y + mul * j > 7) break;
						if (x + mul * i < 0 || x + mul * i > 7) break;
						if (board[y + mul * j][x + mul * i] == 0) break;
						if (board[y + mul * j][x + mul * i] == 1) return true;
					}
				}
			}

			if (!is_black) {
				if (board[y + j][x + i] == 1) {
					for (int mul = 2; mul < WIDTH; mul++) {
						if (y + mul * j < 0 || y + mul *j > 7) break;
						if (x + mul * i < 0 || x + mul * i > 7) break;
						if (board[y + mul * j][x + mul * i] == 0) break;
						if (board[y + mul * j][x + mul * i] == 2) return true;
					}
				}
			}
		}
	}
	return false;
}


