#include "Board.h"
#include "Block.h"
#include "Type.cpp"
#include <stdexcept>
#include <regex>
#include <string>
#include <cstring>
#include <cstdlib>
#include <regex>
#include <istream>

/**
 * @author ThePPK
 * @file
 */

namespace sgt::pattern {
	/**
	 * @class Board
	 * @brief	Parse GameID and store @ref Block "Blocks"
	 * @details
	 * Class store all @ref Block "Blocks" and all sessions of Black @ref Block "Blocks".
	 * Contain too @ref Board::parseGameID "method" parsing GameID to @ref Board.
	 */

	/**
	 * @brief	Constructor for @ref Board class
	 * @param width @copydoc Board::width
	 * @param height @copydoc Board::height
	 * @throw	std::invalid_argument When @p width or @p height equal zero
	 */
	Board::Board(unsigned char width, unsigned char height) : width(width), height(height) {
		if (width <= 0 || height <= 0) {
			throw std::invalid_argument("Width and/or Height can't be lower or equal zero!");
		}
		for (unsigned char y=0; y<height; y++) {
			this->_allocatedBlock.second.push_back(std::vector<unsigned char>());
			this->_map.push_back(std::vector<Block>());
			for (unsigned char x=0; x<width; x++) {
				this->_map[y].push_back(Block(x, y, Type::Empty));
			}
		}
		for (unsigned char x=0; x<width; x++) {
			this->_allocatedBlock.first.push_back(std::vector<unsigned char>());
		}
	};

	/**
	 * @brief	Method recive @ref Block address
	 * @param x @copydoc Block::x
	 * @param y @copydoc Block::y
	 * @throw std::invalid_argument When @p x is higher or equal @ref Board::width
	 * @throw std::invalid_argument When @p y is higher or equal @ref Board::height
	 */
	Block& Board::getBlock(unsigned char x, unsigned char y) {
		if (x >= this->width) {
			throw std::invalid_argument("X coordinate is too large! Expected value to "+std::to_string(this->width)+"!");
		}
		if (y >= this->height) {
			throw std::invalid_argument("Y coordinate is too large! Expected value to "+std::to_string(this->height)+"!");
		}
		return this->_map[y][x];
	};

	/**
	 * @brief	Parse game ID to @ref Board object
	 * @param gameID GameID (regex: '[0-9]+x[0-9]+:([0-9]*\/)+[0-9]*')
	 * @throw std::invalid_argument When @p gameID is invalid
	 * Example:
	 * @code
	 * Board newBoard = Board::parseGameID("4x4:2/1/2/3/1/1.1/3/2");
	 * @endcode
	 * @todo	Write clean code :)) and optimize if it's possible
	 */
	Board Board::parseGameID(char* gameID) {
		std::regex gameIDStructure("^([0-9]+)x([0-9]+):(([0-9]?\\.?\\/?)+)$");
		std::cmatch result;
		if (std::regex_search(gameID, result, gameIDStructure)) {
			Board board(std::stoi(result[1]), std::stoi(result[2]));
			std::string blockSessions = result[3].str();
			if (board.width+board.height-1 == std::count(blockSessions.begin(), blockSessions.end(), '/')) {
				std::replace(blockSessions.begin(), blockSessions.end(), '/', ' ');
				std::stringstream sessions(blockSessions);
				std::string accStr = "";
				for (size_t x=0; x<board.width+board.height; x++) {
					sessions >> accStr;
					std::replace(accStr.begin(), accStr.end(), '.', ' ');
					std::stringstream accNums(accStr);
					while (accNums >> accStr) {
						if (x < board.width) {
							board._allocatedBlock.first[x].push_back(std::stoi(accStr));
						} else {
							board._allocatedBlock.second[x-board.width].push_back(std::stoi(accStr));
						}
					}
				}
				return board;
			}
		}
		throw std::invalid_argument("Invalid GameID!");
	};

	/**
	 * @brief	Method return sessions of black @ref Block "blocks" in columns
	 * @param column Sequence number for sessions in column starting from left
	 * @throw	std::invalid_argument When @p column is higher or equal @ref Board::width "width" of @ref Board
	 * @return	Vector with its representing count of black @ref Block "blocks" in one session
	 */
	std::vector<unsigned char> Board::getSessionsInColumn(unsigned char column) {
		if (column >= this->width) {
			throw std::invalid_argument("Column number cannot be greater than Board width, current width: "+std::to_string(this->width)+"!");
		}
		return this->_allocatedBlock.first[column];
	};

	/**
	 * @brief	Method return sessions of black @ref Block "blocks" in rows
	 * @param row Sequence number for sessions in row starting from top
	 * @throw	std::invalid_argument When @p row is higher or equal @ref Board::height "height" of @ref Board
	 * @return	Vector with its representing count of black @ref Block "blocks" in one session
	 */
	std::vector<unsigned char> Board::getSessionsInRow(unsigned char row) {
		if (row >= this->height) {
			throw std::invalid_argument("Row number cannot be greater than Board height, current height: "+std::to_string(this->height)+"!");
		}
		return this->_allocatedBlock.second[row];
	};

	/**
	 * @breif	Method export board in save format.
	 * @details
	 * Method pack all block data into save format ignoring sequence of changed blocks.
	 * @return	String representing save
	 */
	std::string Board::exportSave() {
		unsigned char x, y;
		Block* tempBlock;
		std::string size = std::to_string(this->width);
		size.append("x");
		size.append(std::to_string(this->height));
		std::string gameID = this->exportGameID();
		gameID = gameID.substr(gameID.find(':')+1);
		std::string moves = "";
		std::string tempMove = "";
		unsigned short countOfMoves = 0;
		std::string output = "SAVEFILE:41:Simon Tatham's Portable Puzzle Collection\nVERSION :1:1\nGAME    :7:Pattern\nPARAMS  :";
		output.append(std::to_string(size.size())+":"+size);
		output.append("\nCPARAMS :");
		output.append(std::to_string(size.size())+":"+size);
		output.append("\nDESC    :"+std::to_string(gameID.size())+":"+gameID+"\n");
		for (x=0; x<this->width; x++) {
			for (y=0; y<this->height; y++) {
				tempBlock = &(this->getBlock(x, y));
				if (tempBlock->getType() != Type::Empty) {
					tempMove = "";
					tempMove.append(tempBlock->getType() == Type::White ? "E" : "F");
					tempMove.append(std::to_string(tempBlock->x));
					tempMove.append(",");
					tempMove.append(std::to_string(tempBlock->y));
					tempMove.append(",1,1\n");
					moves.append("MOVE    :");
					moves.append(std::to_string(tempMove.size()-1)+":");
					moves.append(tempMove);
					countOfMoves++;
				}
			}
		}
		output.append("NSTATES :");
		output.append(std::to_string(std::to_string(countOfMoves).size())+":"+std::to_string(countOfMoves+1)+"\n");
		output.append("STATEPOS:");
		output.append(std::to_string(std::to_string(countOfMoves).size())+":"+std::to_string(countOfMoves+1)+"\n");
		output.append(moves);
		return output;
	};

	/**
	 * @brief	Method return game id.
	 * @details
	 * Method parse sessions of black blocks and create game id.
	 * @return	String with game id
	 */
	std::string Board::exportGameID() {
		std::string output = std::to_string(this->width)+"x"+std::to_string(this->height)+":";
		std::vector<unsigned char> tempSessions({});
		for (unsigned short q=0; q<this->width+this->height; q++) {
			if (q < this->width) {
				tempSessions = this->getSessionsInColumn(q);
			} else {
				tempSessions = this->getSessionsInRow(q%(this->width));
			}
			for (unsigned char p=0; p < tempSessions.size(); p++) {
				output.append(std::to_string(tempSessions[p]));
				output.append(".");
			}
			if (output.back() == '.') {
				output.pop_back();
			}
			output.push_back('/');
		}
		output.pop_back();
		return output;
	};

	/**
	 * @breif  Read save from stream
     * @details
     * Method read save data stream and create board.
     * @param saveStream Data stream
     * @throw std::invalid_argument When save data are incorrect
     * @return Builded @ref Board "board" object from recived data stream
	 * @todo Make parse for: DESC, NSTATES, STATESPOS and MOVEs analyzer
	 */
	Board Board::parseSave(std::istream& saveStream) {
		char buff[1024];
		char param[9];
		unsigned short streamSize;
		bool hasSaveFileHeader = false;
		bool alreadyMetaData = true;
		std::string description;
		unsigned char width, height;
		unsigned short nstates, statepos;
		std::cmatch buffMatch;
		
		std::regex paramsRegEx("^([0-9]+)x([0-9]+)$");
		auto getStreamSize = [&saveStream](){
			char buff2[8];
			saveStream.get(buff2, 2);
			saveStream.get(buff2, 8, ':');
			return std::atoi(buff2);
		};
		
		while (alreadyMetaData) {
			if (not hasSaveFileHeader) {
				saveStream.getline(buff, 1024);
				if (*buff == *"SAVEFILE:41:Simon Tatham's Portable Puzzle Collection") {
					hasSaveFileHeader = true;
					continue;
				} else {
					throw std::invalid_argument("Missing valid SAVEFILE param on first line!");
				}
			}
			saveStream.get(param, 9, ':');
			std::remove(param, param+sizeof(param), ' ');
			streamSize = getStreamSize();
			saveStream.get(buff, 2);
			saveStream.getline(buff, 1024);
			if (std::strlen(buff) != streamSize) {
				throw std::invalid_argument("Invalid parameter length!");
			}
			
			switch (*param) {
				case (*"GAME"):
					if (*buff != *"Pattern") {
						throw std::invalid_argument("Invalid game name!");
					}
					break;
				case (*"CPARAMS"):
				case (*"PARAMS"):
					if (std::regex_search(buff, buffMatch, paramsRegEx)) {
						width = std::stoi(buffMatch[1].str());
						height = std::stoi(buffMatch[2].str());
					} else {
						throw std::invalid_argument("Invalid format of CPARAMS or PARAMS!");
					}	
					break;
				case (*"MOVE"):
				case (*""):
					alreadyMetaData = false;
					break;
			}
		}
	};
}

