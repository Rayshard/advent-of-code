package main

import (
	"bufio"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

type Coord struct {
	x int
	y int
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
	coords := make(map[Coord]int)

	for scanner.Scan() {
		strCoords := strings.Split(scanner.Text(), " -> ")
		strEP1, strEP2 := strings.Split(strCoords[0], ","), strings.Split(strCoords[1], ",")
		x1, _ := strconv.Atoi(strEP1[0])
		y1, _ := strconv.Atoi(strEP1[1])
		x2, _ := strconv.Atoi(strEP2[0])
		y2, _ := strconv.Atoi(strEP2[1])

		if x1 == x2 {
			if y1 < y2 {
				for i := y1; i <= y2; i++ {
					coords[Coord{x1, i}]++
				}
			} else if y2 < y1 {
				for i := y2; i <= y1; i++ {
					coords[Coord{x1, i}]++
				}
			}
		} else if y1 == y2 {
			if x1 < x2 {
				for i := x1; i <= x2; i++ {
					coords[Coord{i, y1}]++
				}
			} else if x2 < x1 {
				for i := x2; i <= x1; i++ {
					coords[Coord{i, y1}]++
				}
			}
		} else if math.Abs((float64(y2)-float64(y1))/(float64(x2)-float64(x1))) == 1 {
			if x1 < x2 {
				if y1 < y2 {
					for {
						coords[Coord{x1, y1}]++
						if x1 == x2 || y1 == y2 {
							break
						}

						x1++
						y1++
					}
				} else if y2 < y1 {
					for {
						coords[Coord{x1, y1}]++
						if x1 == x2 || y1 == y2 {
							break
						}

						x1++
						y1--
					}
				}
			} else if x2 < x1 {
				if y1 < y2 {
					for {
						coords[Coord{x1, y1}]++
						if x1 == x2 || y1 == y2 {
							break
						}

						x1--
						y1++
					}
				} else if y2 < y1 {
					for {
						coords[Coord{x1, y1}]++
						if x1 == x2 || y1 == y2 {
							break
						}

						x1--
						y1--
					}
				}
			}
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	count := 0

	for _, value := range coords {
		if value >= 2 {
			count++
		}
	}

	log.Println(count)
}
