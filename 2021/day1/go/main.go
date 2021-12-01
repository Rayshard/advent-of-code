package main

import (
	"bufio"
	"log"
	"os"
	"strconv"
)

func puzzle1() {

}

func main() {
	// open file
	f, err := os.Open("../input.txt")
	if err != nil {
		log.Fatal(err)
	}
	// remember to close the file at the end of the program
	defer f.Close()

	// read the file line by line using scanner
	scanner := bufio.NewScanner(f)
	lastDepth, depthIncreases := -1, -1
	lastSummedDepth, rollingWindow, rwIncreases := -1, []int{}, -1

	for scanner.Scan() {
		depth, _ := strconv.Atoi(scanner.Text())
		rollingWindow = append(rollingWindow, depth)

		if depth > lastDepth {
			depthIncreases++
		}

		lastDepth = depth

		if len(rollingWindow) == 3 {
			summedDepth := rollingWindow[0] + rollingWindow[1] + rollingWindow[2]
			if summedDepth > lastSummedDepth {
				rwIncreases++
			}

			lastSummedDepth = summedDepth
			rollingWindow = rollingWindow[1:]
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	log.Println(depthIncreases, rwIncreases)
}
