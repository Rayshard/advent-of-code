package main

import (
	"bufio"
	"log"
	"math"
	"os"
	"strconv"
)

func main() {
	// open file
	f, err := os.Open("../input.txt")
	if err != nil {
		log.Fatal(err)
	}
	// close the file at the end of the program
	defer f.Close()

	// read the file line by line using scanner
	scanner := bufio.NewScanner(f)
	lastDepth, depthIncreases := -1, -1
	lastSummedDepth, rollingWindow, rwIncreases := -1, []int{0, 0}, -3

	for scanner.Scan() {
		depth, _ := strconv.Atoi(scanner.Text())

		// puzzle 1
		if depth > lastDepth {
			depthIncreases++
		}

		lastDepth = depth

		// puzzle 2
		rollingWindow = append(rollingWindow, depth)
		summedDepth := rollingWindow[0] + rollingWindow[1] + rollingWindow[2]

		if summedDepth > lastSummedDepth {
			rwIncreases++
		}

		lastSummedDepth = summedDepth
		rollingWindow = rollingWindow[1:]
	}

	rwIncreases = int(math.Max(float64(rwIncreases), 0))

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	log.Println(depthIncreases, rwIncreases)
}
