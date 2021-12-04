package main

import (
	"bufio"
	"log"
	"os"
	"strconv"
	"strings"
)

type Tile struct {
	value  int
	marked bool
}

type Board struct {
	tiles  [25]Tile
	hasWin bool
}

func (board *Board) play(number int) bool {
	idx := -1

	for i, tile := range board.tiles {
		if tile.value == number {
			idx = i
			break
		}
	}

	if idx != -1 {
		board.tiles[idx].marked = true
		return true
	}

	return false
}

func (board *Board) checkForWin() bool {
	if board.hasWin {
		return true
	}

	rows := []bool{true, true, true, true, true}
	cols := []bool{true, true, true, true, true}

	for row := 0; row < 5; row++ {
		for col := 0; col < 5; col++ {
			tile := board.tiles[col+row*5]
			rows[row] = rows[row] && tile.marked
			cols[col] = cols[col] && tile.marked
		}
	}

	for i := 0; i < 5; i++ {
		if rows[i] || cols[i] {
			board.hasWin = true
			break
		}
	}

	return board.hasWin
}

func main() {
	// open file
	f, err := os.Open("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	// close the file at the end of the program
	defer f.Close()

	// read the file line by line using scanner
	scanner := bufio.NewScanner(f)

	var numbers []int
	var boards []*Board

	for scanner.Scan() {
		// get numbers
		for _, elem := range strings.Split(scanner.Text(), ",") {
			number, _ := strconv.Atoi(elem)
			numbers = append(numbers, number)
		}

		scanner.Scan() //skip newline

		// get boards
		for scanner.Scan() {
			var board Board

			for row := 0; row < 5; row++ {
				col := 0
				for _, elem := range strings.Split(scanner.Text(), " ") {
					value, err := strconv.Atoi(elem)

					if err == nil {
						board.tiles[col+row*5] = Tile{value, false}
						col++
					}
				}

				scanner.Scan()
			}

			boards = append(boards, &board)
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	puzzle1Score, puzzle2Score := -1, -1

	for _, number := range numbers {
		playedBoard := false

		for _, board := range boards {
			if !board.hasWin {
				board.play(number)
				playedBoard = true

				if board.checkForWin() {
					sum := 0

					for _, tile := range board.tiles {
						if !tile.marked {
							sum += tile.value
						}
					}

					puzzle2Score = sum * number

					if puzzle1Score == -1 {
						puzzle1Score = puzzle2Score
					}
				}
			}
		}

		if !playedBoard {
			break
		}
	}

	log.Println(puzzle1Score, puzzle2Score)
}
