#include "STcpClient.h"
#include <stdlib.h>
#include <iostream>
/*
	���즹�{�����ʴѤl
	board : �ѽL���A(vector of vector), board[i][j] = i row, j column �ѽL���A(i, j �q 0 �}�l)
			0 = �šB1 = �¡B2 = �աB-1 = �|�Ө���
	is_black : True ��ܥ��{���O�¤l�BFalse ��ܬ��դl

	return Step
	Step : vector, Step = {r, c}
			r, c ��ܭn�U�Ѥl���y�Ц�m (row, column) (zero-base)
*/
std::vector<int> GetStep(std::vector<std::vector<int>>& board, bool is_black) {
	/*
	Example:*/
	std::vector<int> step;
	step.resize(2);

	step[0] = rand() % (7 + 1 - 0) + 0;
	step[1] = rand() % (7 + 1 - 0) + 0;
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
