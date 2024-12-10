from dataclasses import dataclass
from io import TextIOWrapper
import sys
import time
from typing import Optional


@dataclass
class DiskBlock:
    id: int
    allocated_space: int
    free_space: int
    prev_block: Optional["DiskBlock"]
    next_block: Optional["DiskBlock"]

    def __str__(self) -> str:
        return ", ".join(
            (
                f"id({self.id})",
                f"allocated({self.allocated_space})",
                f"free({self.free_space})",
                f"previous({self.prev_block.id if self.prev_block else None})",
                f"next({self.next_block.id if self.next_block else None})",
            )
        )


def parse_disk_map(input: TextIOWrapper) -> tuple[DiskBlock, DiskBlock]:
    map_iter = iter(input.readline().strip())

    initial_block = DiskBlock(-1, 0, 0, None, None)  # Empty block
    prev_block = initial_block
    id = 0

    while file_size := next(map_iter, None):
        file_size = int(file_size)
        free_space = int(next(map_iter, 0))
        cur_block = DiskBlock(id, file_size, free_space, prev_block, None)

        prev_block.next_block = cur_block
        prev_block = cur_block
        id += 1

    return initial_block, prev_block


def calculate_checksum(initial_block: DiskBlock) -> int:
    cur_block = initial_block
    disk_position = 0
    result = 0

    while cur_block := cur_block.next_block:
        # Optimization: We could use the summation formula
        for _ in range(cur_block.allocated_space):
            result += cur_block.id * disk_position
            disk_position += 1
        
        disk_position += cur_block.free_space

    return result

def part1(input: TextIOWrapper) -> int:
    initial_block, final_block = parse_disk_map(input)
    cur_block = initial_block

    while cur_block := cur_block.next_block:
        if not cur_block.free_space or not cur_block.next_block:
            continue
        elif cur_block.free_space < final_block.allocated_space:
            new_block = DiskBlock(
                id=final_block.id,
                allocated_space=cur_block.free_space,
                free_space=0,
                prev_block=cur_block,
                next_block=cur_block.next_block,
            )

            cur_block.free_space = 0
            cur_block.next_block = new_block

            if block_after_new := new_block.next_block:
                block_after_new.prev_block = new_block
            
            final_block.allocated_space -= new_block.allocated_space
        else:
            assert(block_before_final := final_block.prev_block) is not None
            block_before_final.free_space += final_block.allocated_space + final_block.free_space 
            block_before_final.next_block = None

            new_block = final_block
            final_block = block_before_final

            new_block.free_space = cur_block.free_space - new_block.allocated_space
            new_block.prev_block = cur_block
            new_block.next_block = cur_block.next_block

            cur_block.next_block = new_block
            cur_block.free_space = 0

            if block_after_new := new_block.next_block:
                block_after_new.prev_block = new_block

    
    return calculate_checksum(initial_block)


def part2(input: TextIOWrapper) -> int:
    initial_block, block_of_importance = parse_disk_map(input)

    while block_of_importance.id != 0:
        # Find the next block of importance as the right bound of search
        next_block_of_importance = block_of_importance.prev_block

        while next_block_of_importance.id != (block_of_importance.id - 1):
            next_block_of_importance = next_block_of_importance.prev_block

        # Starting from the beginning of the disk, check for free space that can fit
        # the block of importance. If there is one, move it there. Otherwise, leave it
        # be.
        #
        # Optimization: we could keep track of the first block with free space and start
        # there
        cur_block = initial_block

        while cur_block.id != block_of_importance.id:
            if cur_block.free_space < block_of_importance.allocated_space:
                cur_block = cur_block.next_block
                continue

            assert(block_before_important := block_of_importance.prev_block) is not None
            block_before_important.free_space += block_of_importance.allocated_space + block_of_importance.free_space 
            block_before_important.next_block = block_of_importance.next_block

            new_block = block_of_importance
            new_block.free_space = cur_block.free_space - new_block.allocated_space
            new_block.prev_block = cur_block
            new_block.next_block = cur_block.next_block

            cur_block.next_block = new_block
            cur_block.free_space = 0

            if block_after_new := new_block.next_block:
                block_after_new.prev_block = new_block

            break
        
        # Set the next block of importance
        block_of_importance = next_block_of_importance
    
    return calculate_checksum(initial_block)


if __name__ == "__main__":
    assert (file_path := next(iter(sys.argv[1:]), "")), "Missing file path argument"

    with open(file_path) as file:
        print(part1(file))

    with open(file_path) as file:
        print(part2(file))
