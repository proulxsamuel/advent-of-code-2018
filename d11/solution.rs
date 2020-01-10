use std::fs;

fn main() {
    let serial_number: i32 = fs::read_to_string("input.txt").unwrap().parse().unwrap();
    const WIDTH: i32 = 300;
    const HEIGHT: i32 = 300;
    let mut powers = [[0; HEIGHT as usize]; WIDTH as usize];
    for x in 0..WIDTH {
        for y in 0..HEIGHT {
            let rack_id = (x + 1) + 10;
            let mut power = ((rack_id * (y + 1)) + serial_number) * rack_id;
            power = (power / 100) - (power / 1000 * 10) - 5;
            powers[x as usize][y as usize] = power;
        }
    }

    // part 1
    let mut best_configuration = (0, 0);
    let mut best_total = 0;
    for x in 0..=(WIDTH - 3) {
        for y in 0..=(HEIGHT - 3) {
            let mut total = 0;
            for i in x..(x + 3) {
                for j in y..(y + 3) {
                    total += powers[i as usize][j as usize];
                }
                if total > best_total {
                    best_configuration = (x, y);
                    best_total = total;
                }
            }
        }
    }
    let (x, y) = best_configuration;
    println!("{},{}", x + 1, y + 1);

    // part 2
    let mut best_configuration = (0, 0, 0);
    let mut best_total = 0;
    for x in 0..WIDTH {
        for y in 0..HEIGHT {
            let mut total = 0;
            for size in 3..=std::cmp::min(WIDTH - x, HEIGHT - y) {
                for i in x..(x + size) {
                    total += powers[i as usize][(y + size - 1) as usize];
                }
                for i in y..(y + size - 1) {
                    total += powers[(x + size - 1) as usize][i as usize];
                }
                if total > best_total {
                    best_configuration = (x, y, size);
                    best_total = total;
                }
            }
        }
    }
    let (x, y, size) = best_configuration;
    println!("{},{},{}", x + 1, y + 1, size);
}