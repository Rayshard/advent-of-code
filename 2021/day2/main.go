package main

import (
	"bufio"
	"log"
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
	hPos, p1_depth, p2_depth, aim := 0, 0, 0, 0

	// aim is the same as p1_depth
	for scanner.Scan() {
		command := strings.Split(scanner.Text(), " ")
		amt, _ := strconv.Atoi(command[1])

		switch command[0] {
		case "forward":
			hPos += amt
			p2_depth += amt * aim
		case "down":
			p1_depth += amt
			aim = p1_depth
		case "up":
			p1_depth -= amt
			aim = p1_depth
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	log.Println(hPos*p1_depth, hPos*p2_depth)
}
