package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

type TieWinner int
type BitCriteria int

const (
	Zero TieWinner = iota
	One
	Neither
)

const (
	MostCommon BitCriteria = iota
	LeastCommon
)

func getFrequencies(strings []string, tieWinner TieWinner) []bool {
	frequencies := make([]int, len(strings[0]))

	for _, binary := range strings {
		for i, b := range binary {
			frequencies[i] += int(b-'0')*2 - 1
		}
	}

	var result []bool

	for i, f := range frequencies {
		if f < 0 {
			result = append(result, false)
		} else if f > 0 {
			result = append(result, true)
		} else {
			switch tieWinner {
			case Zero:
				result = append(result, false)
			case One:
				result = append(result, true)
			case Neither:
				log.Fatal("Equal number of 0s and 1s at position: " + fmt.Sprint(i))
			}
		}
	}

	return result
}

func puzzle1(lines []string) {
	frequencies := getFrequencies(lines, Neither)

	var g string
	var e string

	for _, f := range frequencies {
		if f {
			g += "1"
			e += "0"
		} else {
			g += "0"
			e += "1"
		}
	}

	gammaRate, _ := strconv.ParseInt(g, 2, 64)
	epsilonRate, _ := strconv.ParseInt(e, 2, 64)

	log.Println(gammaRate, epsilonRate, gammaRate*epsilonRate)
}

func filter(binaries []string, tieWinner TieWinner, bitCriteria BitCriteria) string {
	var result string

	reference := binaries

	for i := 0; i < len(binaries[0]); i++ {
		frequences := getFrequencies(reference, tieWinner)
		var expected rune

		switch bitCriteria {
		case MostCommon:
			if frequences[i] {
				expected = '1'
			} else {
				expected = '0'
			}
		case LeastCommon:
			if frequences[i] {
				expected = '0'
			} else {
				expected = '1'
			}
		}

		var running []string
		for _, binary := range reference {
			if []rune(binary)[i] == expected {
				running = append(running, binary)
			}
		}

		if len(running) == 0 {
			log.Fatal("No remaining binaries to filter")
		} else if len(running) == 1 {
			result = running[0]
			break
		} else {
			reference = running
		}
	}

	return result
}

func puzzle2(lines []string) {
	ogr, _ := strconv.ParseInt(filter(lines, One, MostCommon), 2, 64)
	csr, _ := strconv.ParseInt(filter(lines, One, LeastCommon), 2, 64)

	log.Println(ogr, csr, ogr*csr)
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

	var lines []string
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	puzzle1(lines)
	puzzle2(lines)
}
