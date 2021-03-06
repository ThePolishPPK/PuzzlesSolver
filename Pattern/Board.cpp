#include "Board.h"
#include "Block.h"
#include "Type.cpp"
#include <stdexcept>
#include <regex>
#include <string>
#include <cstring>
#include <cstdlib>
#include <map>
#include <regex>
#include <functional>
#include <istream>
#include <sstream>

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
		if (width == 0 || height == 0) {
			throw std::invalid_argument("Width and/or Height can't equal zero!");
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
		std::string tempMove;
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
		std::vector<unsigned char> tempSessions;
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
	 */
	Board Board::parseSave(std::istream& saveStream) {
		char buff[2048];
		std::string param, data;
		char status = 0b00000000;
		unsigned short streamSize;
		bool hasSaveFileHeader = false;
		bool alreadyMetaData = true;
		bool firstMoveInMeta = false;
		std::string description;
		unsigned char width, height;
		unsigned short nstates, statepos;
		std::cmatch buffMatch;
		std::map<std::string, unsigned char> paramFlags = {
			{"GAME", 0b1}, {"PARAMS", 0b10}, {"DESC", 0b100},
			{"NSTATES", 0b1000}, {"STATEPOS", 0b10000}, {"CPARAMS", 0b100000}
		};
		
		std::regex lineRegEx("^([A-Z]+) *:([0-9]+):(.*)$");
		std::regex paramsRegEx("^([0-9]+)x([0-9]+)$");
		std::regex descRegEx("^(([0-9]\\.?\\/?)+)$");
		std::regex moveRegEx("^(E|F|U)([0-9]+),([0-9]+),([0-9]+),([0-9]+)$");
		
		auto readData = [&buff, &buffMatch, &param, &streamSize, &data, &saveStream, &lineRegEx](){
			saveStream.getline(buff, 2048);
			if (*buff == *"") {
				std::memcpy(buff, "END     :0:", 12);
			}
			if (not std::regex_search(buff, buffMatch, lineRegEx)) {
				throw std::invalid_argument("Invalid line format!");
			}
			param = buffMatch[1].str();
			streamSize = std::stoi(buffMatch[2].str());
			data = buffMatch[3].str();
			if (data.length() != streamSize) {
				throw std::invalid_argument("Invalid parameter length!");
			}
		};
		while (alreadyMetaData) {
			readData();
			if (not hasSaveFileHeader) {
				if (param == "SAVEFILE" && data == "Simon Tatham's Portable Puzzle Collection") {
					hasSaveFileHeader = true;
					continue;
				} else {
					throw std::invalid_argument("Missing valid SAVEFILE param on first line!");
				}
			}
			if (0 < paramFlags.count(param)) {
				if (status & paramFlags[param]) {
					throw std::invalid_argument("Cannot repeat parameter!");
				} else {
					status |= paramFlags[param];
				}
			}
			if (param == "GAME") {
				if (data != "Pattern") {
					throw std::invalid_argument("Invalid game name!");
				}
			} else if (param == "CPARAMS" || param == "PARAMS") {
				if (std::regex_search(data.c_str(), buffMatch, paramsRegEx)) {
					width = std::stoi(buffMatch[1].str());
					height = std::stoi(buffMatch[2].str());
				} else {
					throw std::invalid_argument("Invalid format of CPARAMS or PARAMS!");
				}
			} else if (param == "DESC") {
				if (std::regex_search(data, descRegEx)) {
					description = data;
				} else {
					throw std::invalid_argument("Invalid structure of DESC parameter!");
				}
			} else if (param == "NSTATES") {
				nstates = std::stoi(data);
				if (std::to_string(nstates) != data) {
					throw std::invalid_argument("Invalid NSTATES parameter type!");
				}
			} else if (param == "STATEPOS") {
					statepos = std::stoi(data);
					if (std::to_string(statepos) != data) {
						throw std::invalid_argument("Invalid STATEPOS parameter type!");
					}
			} else if (param == "END" | param == "MOVE") {
				if (param == "MOVE") {
					firstMoveInMeta = true;
				}
				alreadyMetaData = false;
				break;
			}
		}
		for (auto flag=paramFlags.begin(); flag != paramFlags.end(); flag++) {
			if (not (status & flag->second)) {
				throw std::invalid_argument("Missing parameter: "+flag->first+"!");
			}
		}
		if (std::count(description.begin(), description.end(), '/') != width+height-1) {
			throw std::invalid_argument("Invalid DESC parameter! Contain invalid count of parameters!");
		}
		if (nstates < statepos) {
			throw std::invalid_argument("Parameter STATEPOS can't be greater than NSTATES!");
		}
		std::string gameID("");
		unsigned short accStatepos = 0;
		unsigned short accNstates = 0;
		gameID.append(std::to_string(width));
		gameID.append("x");
		gameID.append(std::to_string(height));
		gameID.append(":");
		gameID.append(description);
		Board output = Board::parseGameID(const_cast<char*>(gameID.c_str()));
		std::map<std::string, Type> moveToType = {
			{"E", Type::White}, {"F", Type::Black}, {"U", Type::Empty}
		};
		while (accNstates < nstates) {
			if (not firstMoveInMeta) {
				readData();
			} else {
				firstMoveInMeta = false;
			}
			if (param == "END") {
				break;
			}
			if (not std::regex_search(data.c_str(), buffMatch, moveRegEx)) {
				throw std::invalid_argument("Invalid format of MOVE parameter!");
			}
			if  (accStatepos < statepos) {
				unsigned char x, y, w, h;
				Type moveType = moveToType[buffMatch[1].str()];
				x = std::stoi(buffMatch[2].str());
				y = std::stoi(buffMatch[3].str());
				w = std::stoi(buffMatch[4].str());
				h = std::stoi(buffMatch[5].str());
				if (x+w > width || y+h > height) {
					throw std::invalid_argument("Invalid MOVE parameter data! Location of block, out of range!");
				}
				for (char xpos=x; xpos<x+w; xpos++) {
					for (char ypos=y; ypos<y+h; ypos++) {
						output.getBlock(xpos, ypos).changeType(moveType);
					}
				}
				accStatepos++;
			}
			accNstates++;
		}
		if (accNstates > nstates) {
			throw std::invalid_argument("Invalid count of states (NSTATES param)");
		}
		return output;
	};
	Board Board::parseSave(std::string& save) {
		std::stringstream stream(save);
		return Board::parseSave(stream);
	};
}

