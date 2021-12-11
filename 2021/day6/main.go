package main

import (
	"bufio"
	"log"
	"os"
	"strconv"
	"strings"
)

func calculate(laternfish [9]uint64, iterations int) uint64 {
	for i := 0; i <= iterations; i++ {
		var nextGeneration [9]uint64

		for i, count := range laternfish {
			if i == 0 {
				nextGeneration[6] += count
				nextGeneration[8] += count
			} else {
				nextGeneration[i-1] += count
			}
		}

		laternfish = nextGeneration
	}

	var count uint64
	for _, c := range laternfish {
		count += c
	}

	return count
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
	var laternfish [9]uint64

	if scanner.Scan() {
		strInitial := strings.Split(scanner.Text(), ",")

		for _, elem := range strInitial {
			value, _ := strconv.Atoi(elem)
			laternfish[value+1]++
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	log.Println(calculate(laternfish, 80))
	log.Println(calculate(laternfish, 256))
}
