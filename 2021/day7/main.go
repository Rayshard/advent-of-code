package main

import (
	"bufio"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

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
	var positions []int

	if scanner.Scan() {
		str := strings.Split(scanner.Text(), ",")

		for _, elem := range str {
			value, _ := strconv.Atoi(elem)
			positions = append(positions, value)
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	minFuelPuzzle1, minFuelPuzzle2 := -1, -1

	for _, ref := range positions {
		fuelPuzzle1, fuelPuzzle2 := 0, 0

		for _, pos := range positions {
			n := int(math.Abs(float64(ref - pos)))
			fuelPuzzle1 += n
			fuelPuzzle2 += n * (n + 1) / 2
		}

		if minFuelPuzzle1 == -1 || fuelPuzzle1 < minFuelPuzzle1 {
			minFuelPuzzle1 = fuelPuzzle1
		}

		if minFuelPuzzle2 == -1 || fuelPuzzle2 < minFuelPuzzle2 {
			minFuelPuzzle2 = fuelPuzzle2
		}
	}

	log.Println(minFuelPuzzle1, minFuelPuzzle2)
}
